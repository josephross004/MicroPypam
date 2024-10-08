# MicroPypam: Stripped PyPam for use on embedded 32-bit system

## !!This package is still under development and may not function as intended!!

## ACKNOWLEDGEMENTS
The [PyPam](https://github.com/lifewatch/pypam), [PyHydrophone](https://github.com/lifewatch-pyhydrophone) projects contributed greatly to this effort. 

## USAGE
Once cloned/installed, run `itest.py` to ensure that the program has been installed correctly.

Place a `.wav` file in the `../in` folder and then run `stream_process.py` to run the HMSP computing algorithm. HMSP files will be in the `../out` file. 

To see a matplotlib pyplot of the percentile curves, run the command:

` python graphHMSPData.py `
Arguments: 

`[-t]` Transpose the graph; frequency on the y-axis and dB on the x-axis.

`[-r] [#]` Set the upper limit of the graph.

`[-l]` Plot frequency on a linear scale instead of a log scale.

## REFERENCES
> Martin, S. B., Gaudet, B. J., Klinck, H., Dugan, P. J., Miksis-Olds, J. L., Mellinger, D. K., Mann, D. A., Boebel, O., Wilson, C. C., Ponirakis, D. W., and Moors-Murphy, H. (2021). “Hybrid millidecade spectra: A practical format for exchange of long-term ambient sound data,” JASA Express Lett. 1(1), 011203.

> ---. (2021). "Erratum: Hybrid millidecade spectra: A practical format for exchange of longterm ambient sound data," JASA Express Lett. 1(8), 081201.

> Nathan D. Merchant, Tim R. Barton, Paul M. Thompson, Enrico Pirotta, D. Tom Dakin, John Dorocicz; Spectral probability density as a tool for ambient noise analysis. J. Acoust. Soc. Am. 1 April 2013; 133 (4): EL262–EL267. https://doi.org/10.1121/1.4794934

> Parcerisas, C. (2023). PyPAM: a package to process long-term underwater acoustics data in chunks (0.3.0). Zenodo. https://doi.org/10.5281/zenodo.10037826
## INSTALLATION

Python Version Compatibility: 3.11.2

See DEPENDENCY INSTALLATION INSTRUCTIONS for procedure to build the program.

