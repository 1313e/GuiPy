# -*- coding: utf-8 -*-

"""
Data Table Model
================

"""


# %% IMPORTS
# Built-in imports
import string

# Package imports
import numpy as np
from PyQt5 import QtCore as QC, QtWidgets as QW

# GuiPy imports

# All declaration
__all__ = ['DataTableModel']


# %% GLOBALS
base_26 = list(string.ascii_uppercase)


# %% CLASS DEFINITIONS
# Define model for the DataTable widget
# HINT: https://doc.qt.io/qt-5/model-view-programming.html
class DataTableModel(QC.QAbstractTableModel):
    # Initialize DataTableModel class
    def __init__(self, parent=None, *args, **kwargs):
        # Call super constructor
        super().__init__(parent)

        # Set up model
        self.init(*args, **kwargs)

    # This function sets up the data table model
    def init(self):
        # Initialize an empty list of column names and auto_rename flags
        self.col_names = [self.to_base_26(1)]
        self.col_flags = [True]

        # Initialize an empty list of static column names
        self.static_names = []

        # Set the dtype that each data column must have
        self.dtype = float

        # Initialize an empty array of data
        self.table_data = np.zeros((1, 1), dtype=self.dtype)

        # Connect certain signals with slots
        self.columnsAboutToBeInserted.connect(self.insertColumnNames)

    # This function returns the data column belonging to a specified name
    def columnData(self, name):
        """
        Returns the data array that belongs to the column with the provided
        column `name`.

        Parameters
        ----------
        name : str
            The name of the column whose data is requested.

        Returns
        -------
        data_column : 1D :obj:`~numpy.ndarray` object
            The data array that belongs to the column specified by the provided
            `name`.

        """

        # Return the data column belonging to this name
        return(self.table_data[:, self.col_names.index(name)])

    # This function converts a value to base-26 using the alphabetical letters
    @staticmethod
    def to_base_26(value):
        """
        Converts a given positive `value` to a base-26 integer, which is made
        up by the letters in the alphabet, and returns it.

        In base-26, the values are defined in the following way (note that
        there is no zero):

        - [1, 26] -> ['A', 'Z'];
        - [27, 52] -> ['AA', 'AZ'];
        - [53, 78] -> ['BA', 'BZ'];
        - [703, 728] -> ['AAA', 'AAZ'], etc.

        Parameters
        ----------
        value : int
            The positive integer that must be converted to base-26.

        Returns
        -------
        result : str
            The provided `value` converted to base-26.

        """

        # Initialize empty result
        result = ''

        # While value is not zero yet
        while value:
            # Decrease by 1 to map [1, 26] to [0, 25]
            value -= 1

            # Determine the next digit of the base-26 value
            result = base_26[(value % 26)] + result

            # True divide by 26 to determine the next digit
            value //= 26

        # Return result
        return(result)

    # Override headerData function
    def headerData(self, section, orientation, role):
        # If role is not DisplayRole, return empty QVariant
        if(role != QC.Qt.DisplayRole):
            return(QC.QVariant())

        # If the horizontal header information is requested
        if(orientation == QC.Qt.Horizontal):
            # Return the corresponding column name
            return(self.col_names[section])

        # If the vertical header information is requested
        else:
            # Return the row number itself
            return(section)

    # Override data function
    def data(self, index, role):
        # If this index is valid
        if index.isValid():
            # If a valid role is provided
            if role in (QC.Qt.DisplayRole, QC.Qt.EditRole):
                # Obtain the data column belonging to the requested index
                data_col = self.table_data[:, index.column()]

                # Obtain the requested data point
                data_point = data_col[index.row()]

                # Convert to proper QVariant
                data_point = QC.QVariant(self.dtype(data_point))

                # Return it
                return(data_point)

        # If this index is not valid
        else:
            # Return an empty QVariant
            return(QC.QVariant())

    # Override flags function
    def flags(self, index):
        # If this index is valid, this item is editable
        if index.isValid():
            return(QC.Qt.ItemIsEnabled |
                   QC.Qt.ItemIsSelectable |
                   QC.Qt.ItemIsEditable)
        # Else, this item is only enabled and selectable
        else:
            return(QC.Qt.ItemIsEnabled |
                   QC.Qt.ItemIsSelectable)

    # Override setData function
    def setData(self, index, value, role):
        # If this index is valid and the role is editing
        if index.isValid() and (role == QC.Qt.EditRole):
            # Obtain the data column belonging to the requested index
            data_col = self.table_data[:, index.column()]

            # Set the value
            data_col[index.row()] = value

            # Emit dataChanged signal
            self.dataChanged.emit(index, index, [role])

            # Return that operation finished successfully
            return(True)
        # Else, return that operation did not finish successfully
        else:
            return(False)

    # Override rowCount function
    def rowCount(self, *args, **kwargs):
        return(self.table_data.shape[0])

    # Override columnCount function
    def columnCount(self, *args, **kwargs):
        return(self.table_data.shape[1])

    # Override insertRows function
    def insertRows(self, row, count, parent):
        # Notify other functions that rows are going to be inserted
        self.beginInsertRows(parent, row, row+count-1)

        # Set axis to 0 for all operations
        axis = 0

        # If row == -1, set it to current number of rows+1
        if(row == -1):
            row = self.rowCount()+1

        # Create an array with zeros of the size required
        insert_array = np.zeros((count, self.columnCount()), dtype=self.dtype)

        # Insert the array into the current data table
        self.table_data = np.concatenate([self.table_data[:row],
                                          insert_array,
                                          self.table_data[row:]], axis=axis)

        # Notify other functions that rows have been inserted
        self.endInsertRows()

        # Return that operation was successful
        return(True)

    # Override insertColumns function
    def insertColumns(self, col, count, parent):
        # Set axis to 1 for all operations
        axis = 1

        # If col == -1, set it to current number of columns+1
        if(col == -1):
            col = self.columnCount()+1

        # Notify other functions that columns are going to be inserted
        self.beginInsertColumns(parent, col, col+count-1)

        # Create an array with zeros of the size required
        insert_array = np.zeros((self.rowCount(), count), dtype=self.dtype)

        # Insert the array into the current data table
        self.table_data = np.concatenate([self.table_data[:, :col],
                                          insert_array,
                                          self.table_data[:, col:]], axis=axis)

        # Notify other functions that columns have been inserted
        self.endInsertColumns()

        # Return that operation was successful
        return(True)

    # This function edits the name of a column
    # TODO: Whenever this is triggered, draw a lineedit for typing the name
    # TODO: Additionally, also add an 'auto_rename' bool
    # When this bool is True, the column is automatically renamed upon column
    # count changes. It is always set to False if the column has a custom name
    @QC.pyqtSlot(int)
    def editColumnName(self, col):
        raise NotImplementedError

    # This function sets the name of a column
    # TODO: No two columns can have the same name. If attempted, show error
    @QC.pyqtSlot(int, str, bool)
    def setColumnName(self, col, name, auto_rename):
        # Check if the given name not already exists
        if name in self.col_names and (self.col_names[col] != name):
            # TODO: Show an error
            pass

        # Set the column name and auto_rename flag
        self.col_names[col] = name
        self.col_flags[col] = auto_rename

    # This function inserts column names
    @QC.pyqtSlot(QC.QModelIndex, int, int)
    def insertColumnNames(self, parent, first, last):
        # Determine the insertion column and the number of insertions
        col = first
        count = last-first+1

        # Determine the number of columns currently in the table
        n_cols = self.columnCount()

        # Get the flags of all columns that are affected
        col_flags = self.col_flags[col:]

        # Count how many columns have their auto_rename flag set to False
        n_static = len(self.static_names)

        # Create a list of all column names that could be needed
        insert_names = [self.to_base_26(i+1) for i in range(n_cols-n_static,
                                                            n_cols+count)]

        # Remove all static_names from insert_names
        for name in self.static_names:
            try:
                insert_names.remove(name)
            except ValueError:
                pass

        # Add the first 'count' of insert_names to col_names
        self.col_names.extend(list(insert_names)[:count])

        # Add 'count' True to col_flags
        self.col_flags.extend([True]*count)

        # Loop over all columns that are affected by the insertion
        for i, flag in enumerate(col_flags, col):
            # If this column has a static name
            if not flag:
                # Shift its name and flag by 'count'
                self.col_names.insert(i+count, self.col_names.pop(i))
                self.col_flags.insert(i+count, self.col_flags.pop(i))
