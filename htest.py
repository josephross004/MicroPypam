import numpy as np
import os
import hmsMain
import re
import time
import gzip
import compress
import string
import random
path = "../in"
binsize = 10.0
band1 = [0,2500]
start_time = time.time()

g = open("timelog.txt","a")
for fnlocal in os.listdir(path):
	filename = os.path.join(path,fnlocal)
	os.system("mkdir tempdir")
	os.system("cp "+filename+" ./tempdir")
	tpath = "./tempdir"
	q = hmsMain.calcHMS(tpath,band1,binsize)
	print("FINISHED CALCULATING HMS FROM SIGNAL! CALCULATING PERCENTILES...")
	a = hmsMain.calcPercentilesFromHMS(band1,q)
	ul = hmsMain.hms(band1[1])-hmsMain.hms(band1[0])
	tmpfilesuffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
	with open("./tempdir/tmp"+tmpfilesuffix+".txt",'w') as f:
		for i in range(ul):
			s = str(a[1][0][i])
			s = ''.join(s.splitlines())
			f.write(s.replace("]",'').replace("[",'')+"\n")
	compress.compress("./tempdir/tmp"+tmpfilesuffix+".txt","./tempdir/HMDP.txt") 
	os.system("rm ./tempdir/tmp"+tmpfilesuffix+".txt")
	os.system("py7zr c output.7z ./")
	os.system("mv output.7z ../out/"+str(fnlocal)+".7z")

	'''
	with open('../datamisc/output'+shour+'.txt','w') as f:
	    for i in range(ul):
	        s = str(a[1][0][i])
	        s = ''.join(s.splitlines())
	        #print(s+"\n")
	        f.write(s+"\n")
	'''
	t = time.time() - start_time
	print("--------------------------------------------------------")
	print(" ---  Bin size = %s seconds   --- " % (binsize))
	print(" ---  Completed in %s seconds --- " % (t))
	print("--------------------------------------------------------")
	os.system("rm ./tempdir/*")
