from hmsMain import hms, ihms
from math import log10
import matplotlib.pyplot as plt
import numpy
import os
import compress


def plotPCDFromText(fileName,band,sf=1,title="",transpose=False,linear=False):
    """Plot percentile data from a decompressed hmsp file.

    Args:
        fileName (string): location of file to plot.
        band (tuple): lowest frequency and highest frequency to plot.
        sf (int, optional): starting figure number, if used in conjunction with another function. Defaults to 1.
        title (str, optional): title of the graph plotted. Defaults to "".
    """
    percentileData = numpy.loadtxt(fileName)
    p0 = (1,5,10,25,50,75,90,95,99)
    #Get the minimum and maximum.
    if not transpose:
        for i in range(len(p0)):
            print(percentileData[:,i])
            bin_space = [ihms(x)[1]+band[0] for x in range(len(percentileData[:,1]))]
            plt.plot(bin_space, percentileData[:,i], label='P'+str(p0[i]))
        if not linear:
            plt.xscale('log')
        else:
            plt.xscale('linear')
        plt.xlim([band[0],band[1]])
        #plt.xticks([10**(ihms(i)[1]) for i in range(0,round(log10(hms(band[1])))+1)])
        plt.title("Empirical Probability")
        plt.ylim([numpy.min(percentileData)-5,numpy.max(percentileData)+5])
        plt.ylabel("Sound Level (dB)")
        plt.xlabel("Frequency (Hz)")
    else:
        for i in range(len(p0)):
            print(percentileData[:,i])
            bin_space = [ihms(x)[1]+band[0] for x in range(len(percentileData[:,1]))]
            plt.plot(percentileData[:,i], bin_space, label='P'+str(p0[i]))
        if not linear:
            plt.yscale('log')
        else:
            plt.yscale('linear')
        plt.ylim([band[0],band[1]])
        #plt.xticks([10**(ihms(i)[1]) for i in range(0,round(log10(hms(band[1])))+1)])
        plt.xlim([numpy.min(percentileData)-5,numpy.max(percentileData)+5])
        plt.xlabel("Sound Level (dB)")
        plt.ylabel("Frequency (Hz)")
    plt.title(label=title)
    plt.legend()
    plt.show()

def plotHMSPData(fileName,band,pctls,sf=1,title="",transpose=False,linear=False):
    """Plot percentile data from an hmsp file.

    Args:
        fileName (string): location of file to plot.
        band (tuple): lowest frequency and highest frequency to plot.
        sf (int, optional): starting figure number, if used in conjunction with another function. Defaults to 1.
        title (str, optional): title of the graph plotted. Defaults to "".
    """
    plt.rcParams.update({'font.size': 300})
    compress.decompress(fileName,"plotNow.txt",pctls)
    plotPCDFromText("plotNow.txt",band,sf=sf,title=title,transpose=transpose,linear=linear)


def plotPCData(percentileData,band,sf=1,title=""):
    """Plot percentile data from NumPy array.

    Args:
        percentileData (numpy.ndarray): NumPy array of percentiles.
        band (tuple): lowest frequency and highest frequency to plot.
        sf (int, optional): starting figure number, if used in conjunction with another function. Defaults to 1.
        title (str, optional): title of the graph plotted. Defaults to "".
    """
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
    """Plot hybrid millidecade spectra as a spectrogram, next to percentile data.

    Args:
        hmsData (numpy.ndarray): NumPy array of hybrid millidecade spectra.
        percentileData (numpy.ndarray): NumPy array of percentiles.
        band (tuple): lowest frequency and highest frequency to plot.
        sf (int, optional): starting figure number, if used in conjunction with another function. Defaults to 1.
        title (str, optional): title of the graph plotted. Defaults to "".
    """
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

