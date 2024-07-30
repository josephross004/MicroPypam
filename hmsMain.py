from math import log10
from numpy import percentile, eye
import icListen
from acoustic_survey import ASA

#HMS calculators
def ihms(k):
    """inverse hybrid millidecade bin. calculate the boundaries of a bin, given a bin number.

    Args:
        k (int): bin number to calculate the boundaries of.

    Returns:
        tuple: (low frequency, center frequency, high frequency)
    """
    #input: Band number, output: Frequency range as tuple (low, center, high)
    if k<0:
        return (0,0,0)
    elif k<434:
        return (k-0.5,k,k+0.5)
    G = 10**0.3
    return (435*(10**((k-435.5)/1000)),435*(10**((k-435)/(1000))),435*(10**((k-434.5)/(1000))))

def hms(f):
    """calculate the hybrid millidecade bin number, given a frequency.

    Args:
        f (int): frequency to find bin number of.

    Returns:
        int: bin number.
    """
    #input: frequency, output: band number
    if f<0:
        return 0
    elif f<434:
        return f
    else:
        return round(1000 * log10(f/435) + 435)


def calcHMS(path,band,binsize):
    """calculate hybrid millidecade spectra using icListen parameters using PyPam's acoustic survey method.

    Args:
        path (string): location of file.
        band (tuple): lowest and highest frequency to study.
        binsize (int): length of each PSD window to calculate.

    Returns:
        numpy.ndarray: hybrid millidecade spectra of the input file.
    """
    #WRONG, IGNORE: ex. Soundtrap. icListen is not in the pyhydrophone library so this is something on the to do list.
    model = 'RB9-ETH'
    name = 'icListen'
    serial_number = 6310
    sensitivity = -177.9
    preamp_gain = 0
    vpp = 6
    string_format = "YYYYMMDD_hhmmss"
    path_to_cal= "./freq-sens.xlsx"
    hicListen = icListen.icListen(name=name,model=model,serial_number=serial_number,sensitivity=sensitivity,preamp_gain=preamp_gain,
                                  Vpp=vpp,string_format=string_format,calibration_file=path_to_cal)

    # %%
    # Set the study parameters

    # First, decide band to study. The top frequency should not be higher than the nyquist frequency (sampling rate/2)
    



    # Then, set the nfft to double the sampling rate. If you want to pass None to your band, that is also an option, but
    # then you need to know the sampling frequency to choose the nfft.
    nfft = band[1] * 2  # or nfft = 8000

    # %%
    # Acoustic Survey Object (pypam)
    include_dirs = False
    zipped_files = False
    dc_subtract = True
    asa = ASA(hydrophone=hicListen, folder_path=path, binsize=binsize, nfft=nfft,
                    timezone='UTC', include_dirs=include_dirs, zipped=zipped_files, dc_subtract=dc_subtract)
    # Compute the hybrid millidecade bands
    # You can choose 'density' or 'spectrum' as a method
    milli_psd = asa.hybrid_millidecade_bands(db=True, method='density',
                                            band=band,
                                            percentiles=None)
    return milli_psd['millidecade_bands']
        
def calcPercentilesFromHMS(band,hmsData):
    """Calculate percentiles, usually streamed in from calcHMS().

    Args:
        band (tuple): lowest and highest frequency to study.
        hmsData (numpy.ndarray): hybrid millidecade spectra from calcHMS().

    Returns:
        numpy.ndarray: percentile data of hybrid millidecade spectra.
    """
    hmsData = hmsData.transpose()
    #Percentiles, hardcoded lol
    percentiles = [1,5,10,25,50,75,90,95,99]

    #Instantiate array 
    percentileMatrix = []

    #Percentile vectors
    percentileMatrix.append(eye(hms(band[1])-hms(band[0]),len(percentiles)))
    for n in range(hms(band[1])-hms(band[0])):
        for p in range(len(percentiles)):
            percentileMatrix[0][n,p] = percentile(hmsData[n],percentiles[p])

    return (percentiles,percentileMatrix)

