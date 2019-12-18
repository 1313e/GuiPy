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
from guipy.plugins.data_table.formatters import BaseFormatter
from guipy.plugins.data_table.widgets import DataTableColumn


# All declaration
__all__ = ['NPZFormatter']


# %% CLASS DEFINITIONS
# Define Formatter for .npz-files
class NPZFormatter(BaseFormatter):
    # Class attributes
    TYPE = "NumPy Binary Archive"
    EXTS = ['.npz']

    # Define the export to npz function
    def exporter(self, data_table, filepath):
        # Obtain the list of all data columns
        columns = data_table.model.column_list

        # Make a dictionary that contains the data of all columns
        # TODO: Find out how to preserve the mask
        # Maybe use column._data[~column._data.mask]?
        data_dict = {"(%i, %r)" % (column._index, column._name):
                     column._data.data for column in columns}

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

        # Determine the length of the biggest data column
        length = max(map(len, data_dict.values()))

        # Loop over all data arrays in data_dict and convert to columns
        for i, (key, data) in enumerate(data_dict.items()):
            # Try to convert key to index and name
            try:
                index, name = literal_eval(key)

            # If that does not work, use default values
            except ValueError:
                index = i
                name = key

            # Create data column
            column = DataTableColumn(length, data, index, parent)
            column._name = name

            # Add created data column to the list
            data_columns.insert(index, column)

        # Return data_columns
        return(data_columns)
