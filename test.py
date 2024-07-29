from hmsMain import calcHMS, calcPercentilesFromHMS, hms, ihms
from math import log10
import matplotlib.pyplot as plt
import numpy
from scipy.io import wavfile
from scipy.fft import fft,ifft
from scipy.signal import butter,lfilter
from numpy import abs,linspace,transpose,vstack,append,zeros,complex128,array,float64,sum
from numpy import mean
import math 
from tqdm import tqdm
import compress


def butter_bandpass(lowcut, highcut, fs, order=5):
    return butter(order, [lowcut, highcut], fs=fs, btype='band')

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def freqRange(k):
    if k<0:
        return (0,0,0)
    elif k<434:
        return (k-0.5,k,k+0.5)
    G = 10**0.3
    return (435*(10**((k-435.5)/1000)),435*(10**((k-435)/(1000))),435*(10**((k-434.5)/(1000))))

def bandNumber(f):
    if f<0:
        return 0
    elif f<434:
        return f
    else:
        return round(1000 * math.log10(f/435) + 435)

def readIn(a):
    (fs, data) = wavfile.read(a)
    return (fs,data)

def getPowerSpectrumAt(fs,data,time,length):
    #calculate which index is the starting time. t is in seconds.
    startingIndex = math.floor(time*fs)
    endingIndex = math.ceil((time+length)*fs)
    dataSlice = data[startingIndex:endingIndex]
    #now that we have a slice of data, compute FFT
    dataSliceInFreqDomain = fft(dataSlice)
    if(len(dataSliceInFreqDomain) < fs*5):
        dataSliceInFreqDomain = append(dataSliceInFreqDomain, zeros(fs*5-len(dataSliceInFreqDomain),complex128))
    if(len(dataSliceInFreqDomain)>fs*5):
        dataSliceInFreqDomain = dataSliceInFreqDomain[0:fs*5]
    return abs(dataSliceInFreqDomain)

def getPowerLevelInBand(fs,data,band,time,length):
    #BAND: (start, center, end)
    ps = getPowerSpectrumAt(fs,data,time,length)
    psSlice = ps[math.floor(band[0])*10:math.ceil(band[2])*10]
    return sum(psSlice)*0.1

def getPowerLevelInBand2(fs,data,band,time,length):
    try:
        fData = butter_bandpass_filter(data, band[0],band[2],fs,order=3)
    except ValueError:
        return 0
    #The power of a signal is the sum of the absolute squares of 
    #its time-domain samples divided by the signal length, or, 
    #equivalently, the square of its RMS level. 
    return mean(fData**2)

def getPowerSpectrumInBands(fs,data,time,length):
    nyquist = fs//2
    #count the number of hms bands
    bands = bandNumber(nyquist)
    l = []
    for bn in range(bands):
        l.append(freqRange(bn))
    powerLevels = zeros(bands)
    for i in range(bands):
        powerLevels[i] = getPowerLevelInBand2(fs,data,l[i],time,length)
    return powerLevels

def getSlidingPowerSpectra(fs,data,windowLength,overlap=0):
    #calculate number of windows to calculate
    samples = len(data)
    #numberOfWindows = round((samples-(windowLength*fs*(1-overlap)))/(windowLength*fs*(1-overlap)))
    ##NOTE: I'm sure this will come back to bite me in the ass.
    numberOfWindows = round((samples/(fs*windowLength*(1-overlap)))+((overlap-1)/(1-overlap)))
    
    spectra = (getPowerSpectrumAt(fs,data,0,windowLength))

    #HACK: Index starts at 2 because the first has already been computed. 
    #      This results in less overhead/storage for the program.
    for window in tqdm(range(2, numberOfWindows+1)):
        windowStart = (window-1)*(1-overlap)*(windowLength)
        ps = getPowerSpectrumAt(fs,data,windowStart,windowLength)
        spectra = vstack((spectra, ps))
    #NOTE: spectra uses ROW VECTORS of EACH WINDOW!!
    return spectra

def getSlidingPowerSpectraInHMSBands(fs,data,windowLength,overlap=0):
    #calculate number of windows to calculate
    samples = len(data)
    #numberOfWindows = round((samples-(windowLength*fs*(1-overlap)))/(windowLength*fs*(1-overlap)))
    ##NOTE: I'm sure this will come back to bite me in the ass.
    numberOfWindows = round((samples/(fs*windowLength*(1-overlap)))+((overlap-1)/(1-overlap)))
    
    spectra = (getPowerSpectrumInBands(fs,data,0,windowLength))
    print("WINDOW: 1")

    #HACK: Index starts at 2 because the first has already been computed. 
    #      This results in less overhead/storage for the program.
    for window in range(2, numberOfWindows+1):
        windowStart = (window-1)*(1-overlap)*(windowLength)
        ps = getPowerSpectrumInBands(fs,data,windowStart,windowLength)
        spectra = vstack((spectra, ps))
        print("WINDOW: "+str(window))
    #NOTE: spectra uses ROW VECTORS of EACH WINDOW!!
    return spectra


band = [0,2500]

def plotPCDFromText(fileName,band,sf=1,title=""):
    percentileData = numpy.loadtxt(fileName)
    p0 = (1,5,10,25,50,75,90,95,99)
    for i in range(len(p0)):
        print(percentileData[:,i])
        bin_space = [ihms(x)[1]+band[0] for x in range(len(percentileData[:,1]))]
        plt.plot(bin_space, percentileData[:,i], label='P'+str(p0[i]))
    plt.xscale('log')
    plt.xlim([band[0],band[1]])
    #plt.xticks([10**(ihms(i)[1]) for i in range(0,round(log10(hms(band[1])))+1)])
    plt.title("Empirical Probability")
    plt.ylim([50,200])
    plt.ylabel("Sound Level (dB)")
    plt.xlabel("Frequency (Hz)")
    plt.title(label=title)
    plt.legend()
    plt.show()

def plotPCData(percentileData,band,sf=1,title=""):
    for i in range(len(percentileData[0])):
        print(percentileData[1][0][:,i])
        bin_space = [ihms(x+hms(band[0]))[1] for x in range(len(percentileData[1][0][:,1]))]
        plt.plot(bin_space, percentileData[1][0][:,i], label='P'+str(percentileData[0][i]))
    
    plt.xscale('log')
    plt.xlim([band[0],band[1]])
    plt.title("Empirical Probability")
    plt.ylim([50,200])
    plt.ylabel("Sound Level (dB)")
    plt.xlabel("Frequency (Hz)")
    plt.title(label=title)
    plt.legend()
    plt.show()
    
def plotHMSData(hmsData,percentileData,band,sf=1,title=""):
    hmsData = hmsData.transpose()
    #NOTE: hmsData **IS** in terms of dB.
    plt.figure(sf)
    plt.pcolormesh(hmsData)
    plt.xlabel("Time (minutes)")
    #plt.xticks(labels=[x*binsize/60 for x in range(0,binsize*len(hmsData.transpose()[0]))])
    plt.ylabel("Frequency (bin no.)")
    plt.yscale('log')
    plt.ylim([0,hms(band[1])])
    plt.yticks([10**(ihms(i)[1]) for i in range(0,round(log10(hms(band[1])))+1)])
    #REMOVED for conversion to log: ticks = [round(ihms(x)[1]) for x in range(0,hms(band[1]),100)]
    #REMOVED for conversion to log: plt.yticks(ticks=range(0,800,100), labels=ticks)
    plt.grid(None)
    plt.colorbar().set_label("Sound Level (dB)")


    plt.figure(sf+1)

    for i in range(len(percentileData[0])):
        print(percentileData[1][0][:,i])
        plt.plot(percentileData[1][0][:,i], label='P'+str(percentileData[0][i]))
    
    plt.xscale('log')
    plt.xlim([hms(band[0]),hms(band[1])])
    plt.xticks([10**(ihms(i)[1]) for i in range(0,round(log10(hms(band[1])))+1)])
    plt.title("Empirical Probability")
    plt.ylim([50,160])
    plt.ylabel("Sound Level (dB)")
    plt.xlabel("Frequency (bin no.)")
    plt.title(label=title)
    plt.legend()
    plt.show()


'''sr,data = readIn("E:/I_Misc/D40SurRidge-D113-191125-000000.x.wav")
print(sr,len(data))
specgram = getSlidingPowerSpectra(sr,data,5,0)
plt.imshow(transpose(specgram), aspect='auto')
plt.xlabel("Window Number")
plt.ylabel("Frequency (Hz)")
plt.legend()
ax = plt.gca()
plt.ylim([0,2500])

plt.figure(2)'''

compress.decompress("C:\\Users\\Joseph Ross\\Documents\\F_GitHub\\microPypam\\out\\5k_SurRidge-D113-191125-000000.x.wav\\tempdir\\HMDP.txt",'outputtttt.txt',9,5000)
plotPCDFromText('outputtttt.txt',band,sf=2)