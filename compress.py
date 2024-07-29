import numpy as np
import gzip
import os
import codecs
from hmsMain import hms, ihms
def compress(path,outputname):
    C = []
    O = []
    for fnlocal in os.listdir(path):
        filename = os.path.join(path,fnlocal).replace("\\","/")
        if os.path.isfile(filename):
            A = np.loadtxt(filename)
            s = ''
            for i in A:
                for j in i:
                    if j>127 and j<177:
                        s += "c2"+str(hex(int(j)+68))[2:]
                    else:
                        s += str(hex(int(j)))[2:]
            C.append(s)
            hexes = s.split("c2")
            FLAG = False
            for i in hexes:
                if i=="":
                     i = 'c2'    
                if not FLAG:
                    #print("hex " + i + " utf8 " + bytes.fromhex(i).decode("utf-8"))
                    O.append(bytes.fromhex(i).decode("utf-8"))
                    FLAG = True
                else:
                    try:
                        #print("hex " + i + " utf8 " + bytes.fromhex("c2"+i).decode("utf-8"))
                        O.append(bytes.fromhex("c2"+i).decode("utf-8"))
                    except UnicodeDecodeError:
                        t = (int(i[0:2],16))
                        while t > 191:
                            t -= 50
                        while t < 128:
                            t += 50
                        t = str(hex(t))[2:]
                        i = t + i[2:]
                        #print("hex " + i + " utf8 " + bytes.fromhex("c3"+i).decode("utf-8"))
                        O.append(bytes.fromhex("c3"+i).decode("utf-8"))
    with codecs.open(outputname,"w","utf-8-sig") as f:
        for i in O:
            f.write(str(i))
            #print(i)
    

def decompress(path,output, pctls, upper_frequency):
    ul = hms(upper_frequency)
    with open(path, 'r', encoding="utf-8") as f:
        encoded = f.readlines()[0]
    print(str(len(encoded))+" bytes read in.")
    decoded = ''
    newline_flag = 0
    for i in encoded[1:]:
        if newline_flag==9:
            newline_flag = 0
            decoded += "\n"
        hexrep = i.encode("utf-8").hex()
        if len(hexrep)==2:
            decoded += str(int(hexrep,16))+" "
        else:
            #length is 4. the character either begins with c2 or c3.
            #if it's c2, then subtract 50,
            #if it's c3, add 50.
            if decoded[1]=='3':
                decoded += str(int(hexrep[2:],16)-18) + " "
            else:
                decoded += str(int(hexrep[2:],16)-68) + " "
        newline_flag += 1
    with open(output, 'w') as o:
        o.write(decoded)
    print(str(len(decoded))+" bytes decompressed.")
            



compress("C:/Users/Joseph Ross/Documents/F_Github/datamisc/outputs","test_output2")

decompress("C:/Users/Joseph Ross/Documents/F_Github/pypam/pypam/test_output2","outFFF.txt",9,5000)

