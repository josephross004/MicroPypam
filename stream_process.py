import numpy as np
import os
import hmsMain
import time
import compress
import string
import random
import requests
import time

# -----Check Version!
try:
	V = requests.get("https://raw.githubusercontent.com/josephross004/MicroPypam/main/build.txt")
	with open("build.txt",'r') as ver:
		v = ver.read()
		if str(V.text)!=str(v):
			print("!!! NEW VERSION AVAILABLE !!!")
			print("If you have Git installed, please run the command")
			print("\t$ git pull origin main")
			print("to install it. Thank you!")
			print("!!! NEW VERSION AVAILABLE !!!")
			time.sleep(3)
except:
	pass
# -----End Check Version

win = False

if os.name == 'nt':
	win = True


# define input location
if not win:
	path = "../in"
else:
	path = "..\\in"
# define bin width. numbers above 23.2 have caused the embeddedTS to run out of memory.
binsize = 10.0
# define band to study. will autocorrect to fs/2 if the upper limit is too high.
band1 = [0,2500]
start_time = time.time()

for fnlocal in os.listdir(path):
	# define location of file to analyze
	filename = os.path.join(path,fnlocal)

	# make temporary directory
	if win:
		os.system("mkdir .\\tempdir")
		os.system("copy "+str(filename).replace("/","\\")+" .\\tempdir")
		tpath = ".\\tempdir"
	else:	
		os.system("mkdir tempdir")
		# copy the file to study
		os.system("cp "+str(filename)+" ./tempdir")
		tpath = "./tempdir"

	# calculate hybrid millidecade spectra
	q = hmsMain.calcHMS(tpath,band1,binsize)

	# calculate percentiles from the spectra
	a = hmsMain.calcPercentilesFromHMS(band1,q)
# --- Diagnostic: log HMS peak and labeled Hz ---
	try:
		percentiles = a[0]
		pmatrix = a[1][0]     # matrix: [n_bins x n_percentiles]
		import numpy as _np

		# Find column for 50th percentile (or nearest)
		if 50 in percentiles:
			pidx = list(percentiles).index(50)
		else:
			pidx = len(percentiles)//2

		col = pmatrix[:, pidx]
		k_offset = hmsMain.hms(band1[0])
		k_peak = int(_np.argmax(col)) + k_offset

		fL, fC, fH = hmsMain.ihms(k_peak)
		print(f"[HMS DIAG] peak_bin={k_peak}  approx_center_Hz={fC:.3f}")
	except Exception as _e:
		print(f"[HMS DIAG] skipped: {_e}")

	# random temporary file generation for writing np array compressing
	tmpfilesuffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
	if win:
		tmpfilename = ".\\tempdir\\tmp"+tmpfilesuffix+".txt"
	else:
		tmpfilename = "./tempdir/tmp"+tmpfilesuffix+".txt"
	
	
	
	# --- Determine number of HMS bins from the actual data, not from band1 ---
	pmatrix = a[1][0]                  # shape: [n_bins x n_percentiles]
	n_bins, n_pcts = pmatrix.shape

	# --- Write the entire percentile row per HMS bin (space-separated) ---
	with open(tmpfilename, 'w') as f:
		for i in range(n_bins):
			row = pmatrix[i, :]  # 1 x n_percentiles
			# Space-separated row, no brackets
			f.write(" ".join(f"{float(x)}" for x in row) + "\n")




	#delete the temporary directory
	if win:
		os.system("del /Q .\\tempdir\\"+str(fnlocal).replace("/","\\"))
		compress.compress(".\\tempdir","..\\out\\"+str(fnlocal).replace("/","\\")+".hmsp") 
	else:
		os.system("rm ./tempdir/"+str(fnlocal))
		compress.compress("./tempdir","../out/"+str(fnlocal)+".hmsp") 


	# UNCOMMENT THE NEXT THREE LINES TO COMPRESS (linux)
	#os.system("rm ./tempdir/tmp"+tmpfilesuffix+".txt")
	#os.system("py7zr c output.7z ./tempdir")
	#os.system("rm output.7z ../out/"+str(fnlocal)+".7z")

	t = time.time() - start_time

	#Statistics - feel free to comment these out.
	print("--------------------------------------------------------")
	print(" ---  Bin size = %s seconds   --- " % (binsize))
	print(" ---  Completed in %s seconds --- " % (t))
	print("--------------------------------------------------------")

	# remove any temporary files
	if win:
		os.system("del /Q .\\tempdir")
	else:
		os.system("rm -rf ./tempdir/*")

	#move the processed file into the "processed" folder
	if win:
		os.system("move " +filename.replace("/","\\") + " ..\\processed\\")
	else:
		os.system("mv "+filename+" ../processed/")
