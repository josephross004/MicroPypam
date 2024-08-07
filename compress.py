import numpy as np
import os
import codecs
from hmsMain import hms, ihms
def compress(path,outputname):
    """compress percentiles to a HMSP file using utf-8 and byte adjustment, to minimize space.

    Args:
        path (string): location of hybrid millidecade spectra percentiles
        outputname (string): destination for HMSP file.
    """
    C = []
    O = []
    for fnlocal in os.listdir(path):
        filename = os.path.join(path,fnlocal).replace("\\","/")
        if os.path.isfile(filename):
            A = np.loadtxt(filename)
            s = ''

            # Convert numpy array txt file to hexadecimal (COMPRESSION: 2:1)
            for i in A:
                for j in i:
                    if j < 158 and j >= 127:
                        s += "SPc2"+str(hex(int(j)+34))[2:]
                    elif j < 222 and j >= 158:
                        s += "SPc3"+str(hex(int(j)-30))[2:]
                    elif j >= 222:
                        s += "SPc4"+str(hex(int(j)-94))[2:]
                    elif j<=16:
                        s += "SPd0"+str(hex(int(j)+128))[2:]
                    elif j<=0:
                        s += "SPcfbf"
                    else:
                        s += "SP"+str(hex(int(j)))[2:]
            hexes = s.split("SP")
            FLAG = False
            hexes.pop(0)
            # decode hexadecmial, 2 numbers to 1 byte. (net COMPRESSION: 4:1)
            for i in hexes:   
                O.append(bytes.fromhex(i).decode("utf-8"))
    with codecs.open(outputname,"w","utf-8-sig") as f:
        for i in O:
            f.write(str(i))
    

def decompress(path,output,pctls):
    """decompress an HMSP file.

    Args:
        path (string): path to compressed HMSP file.
        output (string): destination for uncompressed file.
        pctls (int): number of percentile curves generated.
    """
    with open(path, 'r', encoding="utf-8") as f:
        encoded = f.readlines()[0]
    print(str(len(encoded))+" bytes read in.")
    decoded = ''
    newline_flag = 0
    for i in encoded[1:]:
        if newline_flag==pctls:
            newline_flag = 0
            decoded += "\n"
        hexrep = i.encode("utf-8").hex()
        if len(hexrep)==2:
            # length is 2. the character is easily convertible.
            decoded += str(int(hexrep,16))+" "
        else:
            # length is 4.
            if hexrep[1]=='2':
                # c2XX
                decoded += str(int(hexrep[2:],16)-34) + " "
            elif hexrep[1]=='3':
                # c3XX
                decoded += str(int(hexrep[2:],16)+30) + " "
            elif hexrep[1]=='0':
                decoded += str(int(hexrep[2:],16)-80) + " "
            elif hexrep=='cfbf':
                decoded += "0 "
            else:
                # c4XX
                decoded += str(int(hexrep[2:],16)+94) + " "
        newline_flag += 1
    with open(output, 'w') as o:
        o.write(decoded)
    print(str(len(decoded))+" bytes decompressed.")
            

def decompressOld(path,output,pctls):
    """decompress an HMSP file.

    Args:
        path (string): path to compressed HMSP file.
        output (string): destination for uncompressed file.
        pctls (int): number of percentile curves generated.
    """
    with open(path, 'r', encoding="utf-8") as f:
        encoded = f.readlines()[0]
    print(str(len(encoded))+" bytes read in.")
    decoded = ''
    newline_flag = 0
    for i in encoded[1:]:
        if newline_flag==pctls:
            newline_flag = 0
            decoded += "\n"
        hexrep = i.encode("utf-8").hex()
        if len(hexrep)==2:
            decoded += str(int(hexrep,16))+" "
        else:
            #length is 4. the character either begins with c2 or c3.
            #if it's c2, then subtract 68,
            #if it's c3, then subtract 18.
            if hexrep[1]=='3':
                decoded += str(int(hexrep[2:],16)-18) + " "
            else:
                decoded += str(int(hexrep[2:],16)-68) + " "
        newline_flag += 1
    with open(output, 'w') as o:
        o.write(decoded)
    print(str(len(decoded))+" bytes decompressed.")
            

#compress("C:/Users/Joseph Ross/Documents/F_Github/datamisc/outputs","test_output2")

#decompress("C:/Users/Joseph Ross/Documents/F_Github/pypam/pypam/test_output2","outFFF.txt",9,5000)


