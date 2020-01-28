# -*- coding: utf-8 -*-

"""
CSV Formatter
=============

"""


# %% IMPORTS
# Package imports
import pandas as pd

# GuiPy imports
from guipy.plugins.data_table.formatters import BaseFormatter
from guipy.widgets import QW_QMessageBox

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
        # Ask the user if this file has a header
        use_header = QW_QMessageBox.question(
            parent.parent(), "Data import: %s" % (filepath),
            "Use first row as the table header?",
            QW_QMessageBox.Yes | QW_QMessageBox.No, QW_QMessageBox.Yes)

        # Read in the CSV-file as a data frame accordingly
        if(use_header == QW_QMessageBox.Yes):
            data_frame = pd.read_csv(filepath, skipinitialspace=True)
        else:
            data_frame = pd.read_csv(filepath, skipinitialspace=True,
                                     header=None)

        # Return data_frame
        return(data_frame)
