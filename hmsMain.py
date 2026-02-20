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



from math import log10
from numpy import percentile, eye
import icListen
from acoustic_survey import ASA
import os, contextlib, wave

def _infer_fs_from_folder(folder):
    """Return sample rate of first WAV file in folder."""
    try:
        wavs = [f for f in os.listdir(folder) if f.lower().endswith('.wav')]
        if not wavs:
            return None
        first = os.path.join(folder, wavs[0])
        with contextlib.closing(wave.open(first, 'rb')) as wf:
            return wf.getframerate()
    except:
        return None

def calcHMS(path, band, binsize):
    """Calculate hybrid millidecade spectra with stable nfft and band clamping."""
    # --- Infer fs and clamp band to Nyquist ---
    fs = _infer_fs_from_folder(path)
    band_low, band_high = band[0], band[1]
    if fs is not None:
        nyq = fs / 2
        if band_high > nyq:
            band_high = int(nyq)
    band = [band_low, band_high]

    print(f"[HMS] Effective band used: {band}")

    # --- Stable and physically consistent nfft ---
    # After clamping, band_high == Nyquist → nfft = fs → 1 Hz FFT bins.
    nfft = int(band_high * 2)
    print(f"[HMS] nfft used: {nfft}")

    # --- Build icListen params (same as your original code) ---
    model = 'RB9-ETH'
    name = 'icListen'
    serial_number = 6310
    sensitivity = -177.9
    preamp_gain = 0
    vpp = 6
    string_format = "YYYYMMDD_hhmmss"
    path_to_cal = "./freq-sens.xlsx"

    hicListen = icListen.icListen(
        name=name, model=model, serial_number=serial_number,
        sensitivity=sensitivity, preamp_gain=preamp_gain,
        Vpp=vpp, string_format=string_format,
        calibration_file=path_to_cal
    )

    asa = ASA(
        hydrophone=hicListen,
        folder_path=path,
        binsize=binsize,
        nfft=nfft,
        timezone='UTC',
        include_dirs=False,
        zipped=False,
        dc_subtract=True
    )

    milli_psd = asa.hybrid_millidecade_bands(
        db=True, method='density',
        band=band,
        percentiles=None
    )
    return milli_psd['millidecade_bands']

        

def calcPercentilesFromHMS(band, hmsData):
    """
    Calculate percentiles (across time) for each HMS bin.

    Parameters
    ----------
    band : tuple/list
        (Kept for backward compatibility; not used to size the matrix.)
    hmsData : xarray.DataArray
        Output from calcHMS(...), typically asa.hybrid_millidecade_bands()['millidecade_bands']

    Returns
    -------
    (percentiles_list, [percentile_matrix])
        percentile_matrix has shape (n_hms_bins, len(percentiles_list))
    """
    import numpy as np

    # Ensure HMS bins are the first dimension (match original behavior)
    da = hmsData.transpose()

    # Robust sizing: take the number of HMS bins from the data itself
    n_bins = int(da.shape[0])

    # Percentiles to compute
    pct_list = [1, 5, 10, 25, 50, 75, 90, 95, 99]

    # Allocate result matrix
    M = np.empty((n_bins, len(pct_list)), dtype=float)

    # Fill matrix: for each HMS bin, compute percentiles across time
    for n in range(n_bins):
        row = da[n]
        for p, per in enumerate(pct_list):
            M[n, p] = percentile(row, per)

    # Keep return signature compatible with your caller
    return (pct_list, [M])
