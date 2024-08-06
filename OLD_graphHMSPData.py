import plot_hmsp

from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw()

filename = askopenfilename()

plot_hmsp.plotHMSPData(filename, [0,2500],9,sf=3,title=filename[str(filename).rfind("/")+1:],old=True)



