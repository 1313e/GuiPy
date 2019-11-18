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
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports

# All declaration
__all__ = ['DataTableColumn', 'DataTableModel']


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

    # Implement custom closeEvent
    def closeEvent(self, *args, **kwargs):
        # Delete all columns in the column list
        for column in self.column_list:
            del column

        # Call super event
        super().closeEvent(*args, **kwargs)

    # This function sets up the data table model
    def init(self):
        # Initialize the list of column data arrays
        # TODO: Write custom column list that allows for more flexibility
        self.column_list = []

        # Add the first column to this list
        self.insertColumns(-1, 1, QC.QModelIndex())

    # This function returns the data column belonging to a specified name/int
    @QC.Slot(int)
    @QC.Slot(str)
    def dataColumn(self, index):
        """
        Returns the :obj:`~DataTableColumn` object that belongs to the column
        with the provided column `index`.

        Parameters
        ----------
        index : int or str
            If int, the index of the column whose data is requested.
            If str, the name of this column.

        Returns
        -------
        data_column : :obj:`~DataTableColumn`
            The data column that belongs to the column specified by the
            provided `index`.

        """

        # If index is an int, return the column with that index
        if isinstance(index, int):
            return(self.column_list[index])

        # Else if index is a str, check what column that is and return it
        elif isinstance(index, str):
            # Make list with all column display names
            names = [column.display_name for column in self.column_list]

            # Return the column belonging to the requested index
            return(self.column_list[names.index(index)])

    # Override headerData function
    def headerData(self, section, orientation, role):
        # If role is not DisplayRole, return empty QVariant
        if(role != QC.Qt.DisplayRole):
            return(QC.QVariant())

        # If the horizontal header information is requested
        if(orientation == QC.Qt.Horizontal):
            # Return the corresponding column display name
            return(self.column_list[section].display_name)

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
                data_col = self.column_list[index.column()]

                # Obtain the requested data point
                data_point = data_col[index.row()]

                # Convert to proper QVariant
                data_point = QC.QVariant(data_col.dtype(data_point))

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
            data_col = self.column_list[index.column()]

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
        if self.column_list:
            return(len(self.column_list[0]))

    # Override columnCount function
    def columnCount(self, *args, **kwargs):
        return(len(self.column_list))

    # Override insertRows function
    def insertRows(self, row=-1, count=1, parent=None):
        # If row == -1, set it to the current number of rows
        if(row == -1):
            row = self.rowCount()

        # If parent is None, set it to QC.QModelIndex()
        if parent is None:
            parent = QC.QModelIndex()

        # Notify other functions that rows are going to be inserted
        self.beginInsertRows(parent, row, row+count-1)

        # Insert the rows into all data columns
        for column in self.column_list:
            column.insertRows(row, count)

        # Notify other functions that rows have been inserted
        self.endInsertRows()

        # Return that operation was successful
        return(True)

    # Override removeRows function
    def removeRows(self, row=-1, count=1, parent=None):
        # If row == -1, set it to the current number of rows-1
        if(row == -1):
            row = self.rowCount()-1

        # If parent is None, set it to QC.QModelIndex()
        if parent is None:
            parent = QC.QModelIndex()

        # Notify other functions that rows are going to be removed
        self.beginRemoveRows(parent, row-count+1, row)

        # Remove the rows from all data columns
        for column in self.column_list:
            column.removeRows(row, count)

        # Notify other functions that rows have been removed
        self.endRemoveRows()

        # Return that operation was successful
        return(True)

    # This function clears given rows
    def clearRows(self, row, count=1, parent=None):
        # If parent is None, set it to QC.QModelIndex()
        if parent is None:
            parent = QC.QModelIndex()

        # Clear the rows
        for column in self.column_list:
            column.clearRows(row, count)

        # Return that operation was successful
        return(True)

    # Override insertColumns function
    def insertColumns(self, col=-1, count=1, parent=None):
        # If col == -1, set it to current number of columns
        if(col == -1):
            col = self.columnCount()

        # If parent is None, set it to QC.QModelIndex()
        if parent is None:
            parent = QC.QModelIndex()

        # Determine the length the new columns must have
        length = self.rowCount()

        # If length is None, no columns currently exist, so set it to 1
        if length is None:
            length = 1

        # Notify other functions that columns are going to be inserted
        self.beginInsertColumns(parent, col, col+count-1)

        # Create as many columns as required
        for i in range(col, col+count):
            self.column_list.insert(i, DataTableColumn(self, i, length))

        # Modify the index of all columns that have now been moved
        for column in self.column_list[col+count:]:
            column._index += count

        # Notify other functions that columns have been inserted
        self.endInsertColumns()

        # Return that operation was successful
        return(True)

    # Override removeColumns function
    def removeColumns(self, col=-1, count=1, parent=None):
        # If col == -1, set it to current number of columns-1
        if(col == -1):
            col = self.columnCount()-1

        # If parent is None, set it to QC.QModelIndex()
        if parent is None:
            parent = QC.QModelIndex()

        # Notify other functions that columns are going to be removed
        self.beginRemoveColumns(parent, col-count+1, col)

        # Delete as many columns as required
        for _ in range(count):
            self.column_list.pop(col-count+1)

        # Modify the index of all columns that have now been moved
        for column in self.column_list[col-count+1:]:
            column._index -= count

        # Notify other functions that columns have been removed
        self.endRemoveColumns()

        # Return that operation was successful
        return(True)

    # This function clears given columns
    def clearColumns(self, col, count=1, parent=None):
        # If parent is None, set it to QC.QModelIndex()
        if parent is None:
            parent = QC.QModelIndex()

        # Clear the columns
        for column in self.column_list[col:col+count]:
            column.clear()

        # Return that operation was successful
        return(True)

    # This function sets the name of a column
    # TODO: No two columns can have the same name. If attempted, show error
    @QC.Slot(int, str)
    def setColumnName(self, col, name):
        # Get the requested column
        column = self.column_list[col]

        # Set column's name
        column._name = name


# Define class used as a container for data columns in the DataTableModel
class DataTableColumn(QC.QObject):
    """
    Defines the :class:`~DataTableColumn` class.

    This class is used as a container for making data columns in the
    :class:`~DataTableModel` class.

    """

    # Initialize data column
    def __init__(self, parent, index, length):
        """
        Initialize an instance of the :class:`~DataTableColumn` class.

        Parameters
        ----------
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object
            The widget to use as the parent of this data column.
        index : int
            The logical index of this data column.
        length : int
            The length (number of rows) requested for this data column.

        """

        # Save provided index and length
        self._index = index
        self._length = length

        # Call super constructor
        super().__init__(parent)

        # Set up the data column
        self.init()

    # This function sets up the data column
    def init(self):
        # Set default values for dtype and name
        self._dtype = float
        self._name = ""

        # Initialize data array
        # TODO: Should I use a masked array for this?
        self._data = np.zeros(self._length, dtype=self._dtype)

    # Specify the __getitem__ function
    def __getitem__(self, key):
        return(self._data[key])

    # Specify the __len__ function
    def __len__(self):
        return(self.length)

    # Specify the __setitem__ function
    def __setitem__(self, key, value):
        self._data[key] = value

    # This property contains the name of this data column
    @property
    def name(self):
        return(self._name)

    # This property contains the base name of this data column
    @property
    def base_name(self):
        return(self.to_base_26(self._index+1))

    # This property contains the display name of this data column
    @property
    def display_name(self):
        return(self.name if self.name else self.base_name)

    # This property contains the logical index of this data column
    @property
    def index(self):
        return(self._index)

    # This property contains the length of this data column
    @property
    def length(self):
        return(self._length)

    # This property contains the dtype of this data column
    @property
    def dtype(self):
        return(self._dtype)

    # This property contains the data array of this data column
    @property
    def data(self):
        return(self._data)

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

    # This function clears the entire column and resets it to default values
    @QC.Slot()
    def clear(self):
        # Clear this column
        self._data[:] = 0

    # This function inserts empty rows into the data column before given row
    @QC.Slot()
    @QC.Slot(int)
    @QC.Slot(int, int)
    def insertRows(self, row=-1, count=1):
        # If row == -1, set it to the current number of rows
        if(row == -1):
            row = self._length

        # Create an array with zeros of the length required
        insert_array = np.zeros(count, dtype=self._dtype)

        # Insert the array into this data column
        self._data = np.concatenate([self._data[:row],
                                     insert_array,
                                     self._data[row:]])

        # Set the new length of this data column
        self._length += count

    # This function removes rows from the data column before given row
    @QC.Slot()
    @QC.Slot(int)
    @QC.Slot(int, int)
    def removeRows(self, row=-1, count=1):
        # If row == -1, set it to the current number of rows-1
        if(row == -1):
            row = self._length-1

        # Create new array with specified rows removed
        self._data = np.delete(self._data, slice(row-count+1, row+1))

        # Set the new length of this data column
        self._length -= count

    # This function clears rows from the data column
    @QC.Slot(int)
    @QC.Slot(int, int)
    def clearRows(self, row, count=1):
        # Set specified rows to 0
        self._data[row:row+count] = 0
