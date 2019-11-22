# -*- coding: utf-8 -*-

"""
NPZ Formatter
=============

"""


# %% IMPORTS
# Built-in imports
from ast import literal_eval

# Package imports
import numpy as np

# GuiPy imports
from guipy.plugins.data_table.formatters.base import BaseFormatter
from guipy.plugins.data_table.widgets import DataTableColumn


# All declaration
__all__ = []


# %% CLASS DEFINITIONS
# Define Formatter for .npz-files
class Formatter(BaseFormatter):
    # Class attributes
    TYPE = "NumPy Binary Archive"
    EXTS = ['.npz']

    # Define the export to npz function
    def exporter(self, data_table, filepath):
        # Obtain the list of all data columns
        columns = data_table.model.column_list

        # Make a dictionary that contains the data of all columns
        data_dict = {"(%i, %r)" % (column._index, column._name): column._data
                     for column in columns}

        # Save data table as NumPy Binary Archive
        np.savez(filepath, **data_dict)

    # Define the import from npz function
    def importer(self, filepath, parent=None):
        # Load the archive
        archive = np.load(filepath)

        # Convert the loaded archive to a dict
        data_dict = dict(archive)

        # Close the archive
        archive.close()

        # Create empty list of data columns
        data_columns = []

        # Loop over all data arrays in data_dict and convert to columns
        for key, data in data_dict.items():
            # Convert key to index and name
            index, name = literal_eval(key)

            # Create data column
            column = DataTableColumn(len(data), data, index, parent)
            column._name = name

            # Add created data column to the list
            data_columns.insert(index, column)

        # Return data_columns
        return(data_columns)
