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
import pandas as pd

# GuiPy imports
from guipy.plugins.data_table.formatters import BaseFormatter

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
        # Obtain the data in the data table
        data = data_table.model._data

        # Make a dictionary that contains the data of all columns
        data_dict = {"(%i, %r)" % (i, name): column.values
                     for i, (name, column) in enumerate(data.items())}

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

        # Create empty column dict and naming dict
        column_dict = {}
        name_dict = {}

        # Loop over all data arrays in data_dict and obtain their indices
        for i, (key, data) in enumerate(data_dict.items()):
            # Try to convert key to index and name
            try:
                index, name = literal_eval(key)

            # If that does not work, use default values
            except ValueError:
                index = i
                name = key

            # Add index, name and data to the proper dicts
            column_dict[index] = data
            name_dict[index] = name

        # Create a data frame
        data_frame = pd.DataFrame(column_dict)

        # Sort the columns on their indices
        data_frame.sort_index(1, inplace=True)

        # Rename the columns to their proper names
        data_frame.rename(columns=name_dict, inplace=True)

        # Return data_frame
        return(data_frame)
