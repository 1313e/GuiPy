# -*- coding: utf-8 -*-

"""
Base Formatters
===============


"""


# %% IMPORTS
# Built-in imports
from ast import literal_eval

# Package imports
import numpy as np
from qtpy import QtWidgets as QW

# GuiPy imports
from guipy.plugins.data_table.widgets import DataTableColumn


# All declaration
__all__ = ['export_to_npz', 'import_from_npz']


# %% GLOBALS


# %% CLASS DEFINITIONS


# %% FUNCTION DEFINITIONS
# Define the export to npz function
def export_to_npz(data_table, filepath):
    """
    Exports the provided `data_table` to a .npz-file.

    Parameters
    ----------
    data_table : :obj:`~guipy.plugins.data_table.widgets.DataTableWidget`\
        object
        The data table that must be exported.
    filepath : str
        The path to the file to be created.

    """

    # Obtain the list of all data columns
    columns = data_table.model.column_list

    # Make a dictionary that contains the data of all columns
    data_dict = {"(%i, %r)" % (column._index, column._name): column._data
                 for column in columns}

    # Save data table as NumPy Binary Archive
    np.savez(filepath, **data_dict)


# Define the import from npz function
def import_from_npz(filepath, parent=None):
    """
    Imports a .npz-file with the provided `filepath` as a list of data columns.

    Parameters
    ----------
    filepath : str
        The path to the .npz-file.

    Optional
    --------
    parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
        The parent to use for the created
        :obj:`~guipy.plugins.data_table.widgets.DataTableColumn` objects.
        If *None*, no parent will be used.

    Returns
    -------
    column_list : list of \
        :obj:`~guipy.plugins.data_table.widgets.DataTableColumn` objects
        List containing all data columns necessary for recreating the data
        table.

    """

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
