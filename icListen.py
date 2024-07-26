#!/usr/bin/python
from hydrophone import Hydrophone

from datetime import datetime

try:
    import matplotlib.pyplot as plt
    import pandas as pd
except ModuleNotFoundError:
    pass


class icListen(Hydrophone):
    """
    Init an instance of icListen

    Parameters
    ----------
    name: str
        Name of the acoustic recorder
    model: str or int
        Model of the acoustic recorder
    serial_number : str or int
        Serial number of the acoustic recorder
    sensitivity : float
        Sensitivity of the acoustic recorder in db
    preamp_gain : float
        Gain of the preamplifier in dB
    Vpp : float
        Voltage peak to peak in volts
    string_format : string
        Format of the datetime string present in the filename
    calibration_file : string or Path
        File where the frequency dependent sensitivity values for the calibration are
    """
    def __init__(self, name, model, serial_number, sensitivity, preamp_gain, Vpp, string_format="%Y%m%d_%H%M%S",
                 calibration_file=None, **kwargs):
        super().__init__(name, model, serial_number, sensitivity, preamp_gain, Vpp, string_format, calibration_file,
                         **kwargs)

    def get_name_datetime(self, file_name):
        """
        Get the data and time of recording from the name of the file

        Parameters
        ----------
        file_name : string
            File name (not path) of the file
        """
        name = file_name.split('.')[0]
        start_timestamp = name.find('_') + 1
        date_string = name[start_timestamp::]
        date = super().get_name_datetime(date_string)
        return date

    def get_new_name(self, filename, new_date):
        """
        Replace the datetime with the appropriate one

        Parameters
        ----------
        filename : string
            File name (not path) of the file
        new_date : datetime object
            New datetime to be replaced in the filename
        """
        old_date = self.get_name_datetime(filename)
        old_date_name = datetime.strftime(old_date, self.string_format)
        new_date_name = datetime.strftime(new_date, self.string_format)
        new_filename = filename.replace(old_date_name, new_date_name)

        return new_filename
