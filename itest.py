import os
import acoustic_survey
print("acoustic_survey: passed")
import hydrophone
print("hydrophone: passed")
import acoustic_file
print("acoustic file: passed")
import ssignal
print("signal: passed")
import units
print("units: passed")
import utils
print("utils: passed")
import plots
print("plots: passed")
import compress
print("compress: passed")
if os.name == "nt":
  os.system("mkdir ..\\in")
  os.system("mkdir ..\\out")
  os.system("mkdir ..\\processed")
else:
  os.system("mkdir ../in")
  os.system("mkdir ../out")
  os.system("mkdir ../processed")
print("Done. To run this program, place .wav files in ../in and run stream_process.py")
