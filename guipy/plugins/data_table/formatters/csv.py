# -*- coding: utf-8 -*-

"""
CSV Formatter
=============

"""


# %% IMPORTS
# Package imports
import numpy as np
import pandas as pd

# GuiPy imports
from guipy.plugins.data_table.formatters import BaseFormatter

# All declaration
__all__ = ['CSVFormatter']


# %% CLASS DEFINITIONS
# Define Formatter for .csv-files
class CSVFormatter(BaseFormatter):
    # Class attributes
    TYPE = "Comma-Separated Values"
    EXTS = ['.csv']

    # Define the export to csv function
    def exporter(self, data_table, filepath):
        # Obtain the data in the data table
        data = data_table.model._data

        # Export it as a CSV-file
        data.to_csv(filepath, index=False)

    # Define the import from csv function
    def importer(self, filepath, parent=None):
        # Read in the first 2 lines of the CSV-file twice
        df_header = pd.read_csv(filepath, skipinitialspace=True, nrows=2)
        df_no_header = pd.read_csv(filepath, skipinitialspace=True, nrows=2,
                                   header=None)

        # Read in the CSV-file as a data frame depending on if it has a header
        if np.all(df_header.dtypes.values == df_no_header.dtypes.values):
            # If corresponding columns share dtypes, then it has no header
            data_frame = pd.read_csv(filepath, skipinitialspace=True,
                                     header=None)
        else:
            # Else, it must have a header
            data_frame = pd.read_csv(filepath, skipinitialspace=True)

        # Return data_frame
        return(data_frame)
