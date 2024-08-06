import plot_hmsp
import sys

try:
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
except ModuleNotFoundError:
    print("Please install TkInter with the command \n \t $ pip install tkinter \n in your virtual environment.")

Tk().withdraw()

filename = askopenfilename()

transpose = False
linear = False
b1 = 2500

if "-t" in sys.argv or "/t" in sys.argv:
    transpose = True
if "-l" in sys.argv or "/l" in sys.argv:
    linear = True
if "-r" in sys.argv or "/r" in sys.argv:
    b1 = int(sys.argv[sys.argv.index("-r")+1])

plot_hmsp.plotHMSPData(filename, [0,b1],9,sf=3,title=filename[str(filename).rfind("/")+1:],transpose=transpose,linear=linear)



