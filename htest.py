import numpy as np
import os
import hmsMain
import re
import time
import gzip
path = "/home/engineer/microHMS-0.2.0/J40D"
binsize = 10.0
band1 = [0,2500]
start_time = time.time()

g = open("timelog.txt","a")

for hour in range(1):
	os.system("mkdir tempdir")
	if hour<10:
		shour = "0"+str(hour)
	else:
		shour = str(hour)
	os.system("cp ../J40D/5k_SurRidge-D113-191125-"+shour+"0000.x.wav ./tempdir")
	path = "./tempdir"
	q = hmsMain.calcHMS(path,band1,binsize)
	print("FINISHED CALCULATING HMS FROM SIGNAL! CALCULATING PERCENTILES...")
	a = hmsMain.calcPercentilesFromHMS(band1,q)
	ul = hmsMain.hms(band1[1])-hmsMain.hms(band1[0])
	f = gzip.GzipFile("output"+shour+".npy.gz","w")
	np.save(file=f,arr=a[1][0])
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
