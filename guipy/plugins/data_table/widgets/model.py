# -*- coding: utf-8 -*-

"""
Data Table Model
================

"""


# %% IMPORTS
# Built-in imports
from itertools import chain
import string

# Package imports
import numpy as np
import pandas as pd
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports

# All declaration
__all__ = ['DataTableModel']


# %% GLOBALS
base_26 = list(string.ascii_uppercase)


# %% CLASS DEFINITIONS
# Define model for the DataTable widget
# HINT: https://doc.qt.io/qt-5/model-view-programming.html
# TODO: Implement fetchMore system?
# TODO: Implement drag/drop system (HINT+#using-drag-and-drop-with-item-views)
# OPTIMIZE: Should Vaex be used for this instead of Pandas?
class DataTableModel(QC.QAbstractTableModel):
    # Signals
    firstColumnInserted = QC.Signal()
    lastColumnRemoved = QC.Signal()
    rowCountChanged = QC.Signal(int)
    columnCountChanged = QC.Signal(int)
    columnNameChanged = QC.Signal(int, str)

    # Initialize DataTableModel class
    def __init__(self, parent=None, *args, **kwargs):
        # Call super constructor
        super().__init__(parent)

        # Set up model
        self.init(*args, **kwargs)

    # Implement delete function
    @QC.Slot()
    def delete(self):
        # Delete all columns in the column list
        self.removeColumns(count=self.columnCount())

    # This function sets up the data table model
    def init(self, import_func=None):
        # Connect signals
        self.destroyed.connect(self.delete)
        self.columnsInserted.connect(self.emitColumnsInsertedSignals)
        self.columnsRemoved.connect(self.emitColumnsRemovedSignals)
        self.rowsInserted.connect(self.emitRowsInsertedSignals)
        self.rowsRemoved.connect(self.emitRowsRemovedSignals)

        # Make a look-up dict for dtypes
        self.dtypes = {
            np.bool_: 'bool',
            np.float64: 'float',
            np.int64: 'int',
            np.object_: 'str'}

        # If import_func is None, initialize an empty table
        if import_func is None:
            # Initialize an empty table
            self._data = pd.DataFrame([])

            # Initialize this data table with a 5x5 table
            self.insertColumns(count=5)
            self.insertRows(count=5)

        # If import_func is not None, call it to initialize the table
        else:
            # Call the function to obtain the data
            self._data = import_func(self)

            # Check if the data frame has the proper column names
            if self._data.columns.dtype.type is np.int64:
                renames = {i: to_base_26(i+1) for i in self._data.columns}
                self._data.rename(columns=renames, inplace=True)

            # Notify other functions that columns have been inserted
            self.beginInsertColumns(QC.QModelIndex(), 0, self.columnCount()-1)
            self.endInsertColumns()

            # Notify other functions that rows have been inserted
            self.beginInsertRows(QC.QModelIndex(), 0, self.rowCount()-1)
            self.endInsertRows()

    # This function emits proper signals when columns have been inserted
    @QC.Slot(QC.QModelIndex, int, int)
    def emitColumnsInsertedSignals(self, parent, first, last):
        # Emit columnCountChanged signal
        self.columnCountChanged.emit(self.columnCount())

        # If first+last+1 is equal to count, emit firstColumnInserted signal
        if(first+last+1 == self.columnCount()):
            self.firstColumnInserted.emit()

    # This function emits proper signals when columns have been removed
    @QC.Slot(QC.QModelIndex, int, int)
    def emitColumnsRemovedSignals(self, parent, first, last):
        # Emit columnCountChanged signal
        self.columnCountChanged.emit(self.columnCount())

        # If columnCount is equal to zero, emit lastColumnRemoved signal
        if not self.columnCount():
            self.lastColumnRemoved.emit()

    # This function emits proper signals when rows have been inserted
    @QC.Slot(QC.QModelIndex, int, int)
    def emitRowsInsertedSignals(self, parent, first, last):
        # Emit rowCountChanged signal
        self.rowCountChanged.emit(self.rowCount())

    # This function emits proper signals when rows have been removed
    @QC.Slot(QC.QModelIndex, int, int)
    def emitRowsRemovedSignals(self, parent, first, last):
        # Emit rowCountChanged signal
        self.rowCountChanged.emit(self.rowCount())

    # This function returns the data column belonging to a specified name/int
    @QC.Slot(int)
    @QC.Slot(str)
    def dataColumn(self, index):
        """
        Returns the :obj:`~pandas.Series` object that belongs to the column
        with the provided column `index`.

        Parameters
        ----------
        index : int or str
            If int, the index of the column whose data is requested.
            If str, the name of this column.

        Returns
        -------
        data_column : :obj:`~pandas.Series`
            The data column that belongs to the column specified by the
            provided `index`.

        """

        # If index is an int, return the column with that index
        if isinstance(index, int):
            return(self._data.iloc[:, index])

        # Else if index is a str, check what column that is and return it
        elif isinstance(index, str):
            return(self._data.loc[:, index])

    # This function returns a list with all data column names
    @QC.Slot()
    def columnNames(self):
        """
        Returns a list with the names of all :obj:`~pandas.Series` objects
        stored in this model.

        Returns
        -------
        names : list of str
            List with names of all data columns.

        """

        # Return list of data column names
        return(list(self._data.columns))

    # Override headerData function
    def headerData(self, section, orientation, role):
        # If role is not DisplayRole, return empty QVariant
        if(role != QC.Qt.DisplayRole):
            return(QC.QVariant())

        # If the horizontal header information is requested
        if(orientation == QC.Qt.Horizontal):
            # Return the corresponding column name
            return(self._data.columns[section])

        # If the vertical header information is requested
        else:
            # Return the corresponding row name
            return(self._data.index[section])

    # Override data function
    def data(self, index, role):
        # If this index is valid
        if index.isValid() and role in (QC.Qt.DisplayRole, QC.Qt.EditRole):
            # Obtain the requested value
            value = self._data.iat[index.row(), index.column()]

            # Convert value to a Python scalar
            if isinstance(value, np.generic):
                value = value.item()

            # If value is None, always use an empty QVariant
            if pd.isna(value):
                data_point = QC.QVariant()

            # Else, create proper QVariant
            else:
                data_point = QC.QVariant(value)

        # Else, use an empty QVariant
        else:
            data_point = QC.QVariant()

        # Return created data_point
        return(data_point)

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
            # Set the value
            self._data.iat[index.row(), index.column()] = value

            # Emit dataChanged signal
            self.dataChanged.emit(index, index, [role])

            # Return that operation finished successfully
            return(True)

        # Else, return that operation did not finish successfully
        else:
            return(False)

    # Override rowCount function
    @QC.Slot()
    @QC.Slot(QC.QModelIndex)
    def rowCount(self, parent=None):
        # Return row count
        if self._data.empty:
            return(0)
        else:
            return(self._data.shape[0])

    # Override columnCount function
    @QC.Slot()
    @QC.Slot(QC.QModelIndex)
    def columnCount(self, parent=None):
        # Return column count
        return(self._data.shape[1])

    # This function inserts rows before given row
    # Vaex: df.concat
    @QC.Slot()
    @QC.Slot(int)
    @QC.Slot(int, int)
    @QC.Slot(int, int, QC.QModelIndex)
    def insertRows(self, row=None, count=1, parent=None):
        # If row is None, set it to the current number of rows
        if row is None:
            row = self.rowCount()

        # If parent is None, set it to QC.QModelIndex()
        if parent is None:
            parent = QC.QModelIndex()

        # Notify other functions that rows are going to be inserted
        self.beginInsertRows(parent, row, row+count-1)

        # Create dataframe with the required shape
        insert_df = pd.DataFrame(np.full((count, self.columnCount()), np.nan),
                                 columns=self._data.columns)

        # Concatenate the current dataframe and insert_df
        self._data = pd.concat([self._data[:row], insert_df, self._data[row:]],
                               ignore_index=True)

        # Notify other functions that rows have been inserted
        self.endInsertRows()

        # Emit rowCountChanged signal
        self.rowCountChanged.emit(self.rowCount())

        # Return that operation was successful
        return(True)

    # This function removes rows starting at given row
    # Vaex: df.take + df.to_copy?
    @QC.Slot()
    @QC.Slot(int)
    @QC.Slot(int, int)
    @QC.Slot(int, int, QC.QModelIndex)
    def removeRows(self, row=None, count=1, parent=None):
        # If row is None, set it to the current number of rows-count
        if row is None:
            row = self.rowCount()-count

        # If parent is None, set it to QC.QModelIndex()
        if parent is None:
            parent = QC.QModelIndex()

        # Notify other functions that rows are going to be removed
        self.beginRemoveRows(parent, row, row+count-1)

        # Remove the rows
        indexes = chain(range(0, row), range(row+count, self.rowCount()))
        self._data = self._data.reindex(index=indexes)
        self._data.reset_index(drop=True, inplace=True)

        # Notify other functions that rows have been removed
        self.endRemoveRows()

        # Emit rowCountChanged signal
        self.rowCountChanged.emit(self.rowCount())

        # Return that operation was successful
        return(True)

    # This function clears rows starting at given row
    @QC.Slot(int)
    @QC.Slot(int, int)
    @QC.Slot(int, int, QC.QModelIndex)
    def clearRows(self, row, count=1, parent=None):
        # Clear the rows
        self._data.iloc[row:row+count] = np.nan

        # Return that operation was successful
        return(True)

    # This function inserts columns before given col
    # Vaex: df.add_column
    @QC.Slot()
    @QC.Slot(int)
    @QC.Slot(int, int)
    @QC.Slot(int, int, QC.QModelIndex)
    def insertColumns(self, col=None, count=1, parent=None):
        # If col is None, set it to current number of columns
        if col is None:
            col = self.columnCount()

        # If parent is None, set it to QC.QModelIndex()
        if parent is None:
            parent = QC.QModelIndex()

        # Notify other functions that columns are going to be inserted
        self.beginInsertColumns(parent, col, col+count-1)

        # Create dict with all renames required
        renames = {to_base_26(i+1): to_base_26(i+1+count)
                   for i in range(col, self.columnCount())}

        # Rename all columns that require renaming
        self._data.rename(columns=renames, inplace=True)

        # Create as many columns as required
        for i in reversed(range(col, col+count)):
            self._data.insert(col, to_base_26(i+1), np.nan)

        # Notify other functions that columns have been inserted
        self.endInsertColumns()

        # Return that operation was successful
        return(True)

    # This function removes columns starting at given col
    # Vaex: df.drop
    @QC.Slot()
    @QC.Slot(int)
    @QC.Slot(int, int)
    @QC.Slot(int, int, QC.QModelIndex)
    def removeColumns(self, col=None, count=1, parent=None):
        # If col is None, set it to current number of columns-count
        if col is None:
            col = self.columnCount()-count

        # If parent is None, set it to QC.QModelIndex()
        if parent is None:
            parent = QC.QModelIndex()

        # If count is equal to columnCount, remove all rows first
        if(self.columnCount() == count):
            self.removeRows(count=self.rowCount())

        # Notify other functions that columns are going to be removed
        self.beginRemoveColumns(parent, col, col+count-1)

        # Create dict with all renames required
        renames = {to_base_26(i+1): to_base_26(i+1-count)
                   for i in range(col+count, self.columnCount())}

        # Delete as many columns as required
        for name in self._data.columns[col:col+count]:
            self._data.pop(name)

        # Rename the remaining columns
        self._data.rename(columns=renames, inplace=True)

        # Notify other functions that columns have been removed
        self.endRemoveColumns()

        # Return that operation was successful
        return(True)

    # This function clears columns starting at given col
    @QC.Slot(int)
    @QC.Slot(int, int)
    @QC.Slot(int, int, QC.QModelIndex)
    def clearColumns(self, col, count=1, parent=None):
        # Clear the columns
        self._data.iloc[:, col:col+count] = np.nan

        # Return that operation was successful
        return(True)

    # This function sets the name of a column
    # Vaex: df.rename_column
    @QC.Slot(int, str)
    def setColumnName(self, col, name):
        # If no name was given, use the base name
        if not name:
            name = to_base_26(col+1)

        # Set column name
        self._data.rename(
            columns={self._data.columns[col]: name}, inplace=True)

        # Emit a signal stating that a column changed its name
        self.columnNameChanged.emit(col, name)

    # This function sets the dtype of a column
    # TODO: If auto-conversion is not possible, ask user if the column should
    # be cleared first instead
    @QC.Slot(int, str)
    def setColumnDataType(self, col, dtype):
        # Set the requested data type
        self._data = self._data.astype({self._data.columns[col]: dtype},
                                       copy=False)


# %% FUNCTION DEFINITIONS
# This function converts a value to base-26 using the alphabetical letters
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
