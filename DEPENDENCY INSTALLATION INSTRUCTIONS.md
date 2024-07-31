# IMPORTANT: WHEEL SOURCE 
### (FOR TS-7553, RASPBERRY PI, ARM ARCHITECTURE)
Please add the following two lines to your `/etc/pip.conf` file:

```
[global]
extra-index-url=https://piwheels.org/simple
```

# CONSTRUCT VENV
`$ mkdir ~/MicroPypam && cd ~/MicroPypam`

make venv

`$ virtualenv env`

verify python=3.11

`$ ls env/lib`
> python3.11

# activate venv
`$ source env/bin/activate`

the following packages should all be included with this installation of python:
math, xml, datetime, operator, os, patlib, zipfile, re, functools

`$ python`

`>>>import math, xml, datetime, operator, os, pathlib, zipfile, re, functools`

should have no errors.

#  INSTALLING PACKAGES

This process may take a while.

`$ pip install scipy`

These next packages have to be installed in separate commands, or the computer runs out of memory.

`$ pip install meson`

`$ pip install meson-python`

`$ pip install Cython`

`$ pip install packaging`

`$ pip install pyproject-metadata`

the installer doesn't select the right wheel to install scikit-learn. download the wheel directly, then install. 

`$ wget https://www.piwheels.org/simple/scikit-learn/scikit_learn-1.4.2-cp311-cp311-linux_armv7l.whl`

`$ pip install scikit_learn-1.4.2-cp311-cp311-linux_armv7l.whl`

INSTALLING LLVMLITE: This is the *problem* with pypam on this machine. The installer for llvmlite expects 64-bit architecture so it results in lots of problems. Here's what you do to install it from source.

`$ sudo apt install llvm`

`$ sudo apt install cmake`

`$ wget https://github.com/numba/llvmlite/archive/refs/tags/v0.43.0.tar.gz`

`$ tar -xf v0.43.0.tar.gz`

`$ cd llvmlite-0.43.0`

`$ python setup.py build`

If you get a c++ process killed error, just run this again, it'll pick right back up. This process can take a long time.

`$ python runtests.py`

>Ran 381 tests in 25.620s
>OK (skipped=20)

`$ python setup.py install`

`$ cd ..`

`$ python`

`>>> import llvmlite`

`>>> ^D `

(pressed Ctrl+D to exit python)
If there is a ModuleNotFoundError then something went wrong.

`$ pip install numba`

`$ pip install librosa`

`$ pip install noisereduce==2.0.1`

`$ pip install pvlib`
 
__NOTE__: This file is around ~29MB and if you have slow internet the hashes
won't match up. So you can get this file from pypl e.g. 
wget https://files.pythonhosted.org/packages/e7/5c/f4c088c7a04f5b7c0a532fe264de21b840d65aee619eee0d11dcc62e8b8f/pvlib-0.11.0-py3-none-any.whl 
and then `$ pip install pvlib-0.11.0-py3-none-any.whl`

`$ pip install dask`

`$ pip install seaborn`

`$ pip install xarray`

`$ pip install openpyxl`

`$ pip install py7zr`

now, reinstall the correct NumPy

`$ pip uninstall numpy`

`$ pip install numpy==1.26.4`

# INSTALLING MicroPypam

This is a custom rebuild of PyPam (https://github.com/lifewatch/pypam) designed for this computer specifically.

`$ git clone https://github.com/josephross004/microPypam`

Run tests to ensure that it works.
`$ cd microPypam`

`$ python itest.py`
