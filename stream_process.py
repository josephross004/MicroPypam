import numpy as np
import os
import hmsMain
import time
import compress
import string
import random

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

	# calculate the total number of bins
	ul = hmsMain.hms(band1[1])-hmsMain.hms(band1[0])

	# random temporary file generation for writing np array compressing
	tmpfilesuffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
	if win:
		tmpfilename = ".\\tempdir\\tmp"+tmpfilesuffix+".txt"
	else:
		tmpfilename = "./tempdir/tmp"+tmpfilesuffix+".txt"
	with open(tmpfilename,'w') as f:
		# write numpy array to compressible format
		for i in range(ul):
			s = str(a[1][0][i])
			s = ''.join(s.splitlines())
			f.write(s.replace("]",'').replace("[",'')+"\n")

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
