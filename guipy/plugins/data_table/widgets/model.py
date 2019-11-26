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
    # Signals
    firstColumnInserted = QC.Signal()
    lastColumnRemoved = QC.Signal()
    rowCountChanged = QC.Signal(int)
    columnCountChanged = QC.Signal(int)

    # Initialize DataTableModel class
    def __init__(self, parent=None, *args, **kwargs):
        # Call super constructor
        super().__init__(parent)

        # Set up model
        self.init(*args, **kwargs)

    # Implement delete function
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
            np.str_: 'str'}

        # If import_func is None, initialize an empty table
        if import_func is None:
            # Initialize the list of column data arrays
            # TODO: Write custom column list that allows for more flexibility
            self.column_list = []

            # Initialize this data table with a 5x5 table
            self.insertColumns(5)
            self.insertRows(5)

        # If import_func is not None, call it to initialize the table
        else:
            # Call the function to obtain the list of data columns
            self.column_list = import_func(self)

            # Notify other functions that columns have been inserted
            self.beginInsertColumns(QC.QModelIndex(), 0, self.columnCount()-1)
            self.endInsertColumns()

            # Notify other functions that rows have been inserted
            self.beginInsertRows(QC.QModelIndex(), 0, self.rowCount()-1)
            self.endInsertRows()

    # This function emits proper signals when columns have been inserted
    def emitColumnsInsertedSignals(self, parent, first, last):
        # Emit columnCountChanged signal
        self.columnCountChanged.emit(self.columnCount())

        # If first is equal to zero, emit firstColumnInserted signal
        if not first:
            self.firstColumnInserted.emit()

    # This function emits proper signals when columns have been removed
    def emitColumnsRemovedSignals(self, parent, first, last):
        # Emit columnCountChanged signal
        self.columnCountChanged.emit(self.columnCount())

        # If columnCount is equal to zero, emit lastColumnRemoved signal
        if not self.columnCount():
            self.lastColumnRemoved.emit()

    # This function emits proper signals when rows have been inserted
    def emitRowsInsertedSignals(self, parent, first, last):
        # Emit rowCountChanged signal
        self.rowCountChanged.emit(self.rowCount())

    # This function emits proper signals when rows have been removed
    def emitRowsRemovedSignals(self, parent, first, last):
        # Emit rowCountChanged signal
        self.rowCountChanged.emit(self.rowCount())

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

                # Convert to proper QVariant
                data_point = QC.QVariant(data_col.item(index.row()))

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
            return(self.column_list[0].length)
        else:
            return(0)

    # Override columnCount function
    def columnCount(self, *args, **kwargs):
        return(len(self.column_list))

    # This function inserts rows before given row
    def insertRows(self, count=1, row=None, parent=None):
        # If row is None, set it to the current number of rows
        if row is None:
            row = self.rowCount()

        # If parent is None, set it to QC.QModelIndex()
        if parent is None:
            parent = QC.QModelIndex()

        # Notify other functions that rows are going to be inserted
        self.beginInsertRows(parent, row, row+count-1)

        # Insert the rows into all data columns
        for column in self.column_list:
            column.insertRows(count, row)

        # Notify other functions that rows have been inserted
        self.endInsertRows()

        # Emit rowCountChanged signal
        self.rowCountChanged.emit(self.rowCount())

        # Return that operation was successful
        return(True)

    # This function removes rows starting at given row
    def removeRows(self, count=1, row=None, parent=None):
        # If row is None, set it to the current number of rows-count
        if row is None:
            row = self.rowCount()-count

        # If parent is None, set it to QC.QModelIndex()
        if parent is None:
            parent = QC.QModelIndex()

        # Notify other functions that rows are going to be removed
        self.beginRemoveRows(parent, row, row+count-1)

        # Remove the rows from all data columns
        for column in self.column_list:
            column.removeRows(count, row)

        # Notify other functions that rows have been removed
        self.endRemoveRows()

        # Emit rowCountChanged signal
        self.rowCountChanged.emit(self.rowCount())

        # Return that operation was successful
        return(True)

    # This function clears rows starting at given row
    def clearRows(self, row, count=1, parent=None):
        # If parent is None, set it to QC.QModelIndex()
        if parent is None:
            parent = QC.QModelIndex()

        # Clear the rows
        for column in self.column_list:
            column.clearRows(row, count)

        # Return that operation was successful
        return(True)

    # This function inserts columns before given col
    def insertColumns(self, count=1, col=None, parent=None):
        # If col is None, set it to current number of columns
        if col is None:
            col = self.columnCount()

        # If parent is None, set it to QC.QModelIndex()
        if parent is None:
            parent = QC.QModelIndex()

        # Determine the length the new columns must have
        length = self.rowCount()

        # Notify other functions that columns are going to be inserted
        self.beginInsertColumns(parent, col, col+count-1)

        # Create as many columns as required
        for i in range(col, col+count):
            self.column_list.insert(i, DataTableColumn(length, None, i, self))

        # Modify the index of all columns that have now been moved
        for column in self.column_list[col+count:]:
            column._index += count

        # Notify other functions that columns have been inserted
        self.endInsertColumns()

        # Return that operation was successful
        return(True)

    # This function removes columns starting at given col
    def removeColumns(self, count=1, col=None, parent=None):
        # If col is None, set it to current number of columns-count
        if col is None:
            col = self.columnCount()-count

        # If parent is None, set it to QC.QModelIndex()
        if parent is None:
            parent = QC.QModelIndex()

        # If count is equal to columnCount, remove all rows first
        if(self.columnCount() == count):
            self.removeRows(self.rowCount())

        # Notify other functions that columns are going to be removed
        self.beginRemoveColumns(parent, col, col+count-1)

        # Delete as many columns as required
        for i in reversed(range(col, col+count)):
            column = self.column_list.pop(i)
            column.delete()

        # Modify the index of all columns that have now been moved
        for column in self.column_list[col:]:
            column._index -= count

        # Notify other functions that columns have been removed
        self.endRemoveColumns()

        # Return that operation was successful
        return(True)

    # This function clears columns starting at given col
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
    @QC.Slot(int, str)
    def setColumnName(self, col, name):
        # Get the requested column
        column = self.column_list[col]

        # Set column's name
        column.name = name

    # This function sets the dtype of a column
    # TODO: If auto-conversion is not possible, ask user if the column should
    # be cleared instead
    @QC.Slot(int, str)
    def setColumnDataType(self, col, dtype):
        # Get the requested column
        column = self.column_list[col]

        # Set column's dtype
        column.dtype = dtype


# Define class used as a container for data columns in the DataTableModel
class DataTableColumn(object):
    """
    Defines the :class:`~DataTableColumn` class.

    This class is used as a container for making data columns in the
    :class:`~DataTableModel` class.

    """

    # Initialize data column
    def __init__(self, length, data=None, index=0, parent=None):
        """
        Initialize an instance of the :class:`~DataTableColumn` class.

        Parameters
        ----------
        length : int
            The length (number of rows) requested for this data column.
            If `data` is not *None* and `length != len(data)`, the array given
            by `data` will be extended/shortened accordingly.

        Optional
        --------
        data : 1D :obj:`~numpy.ndarray` object or None. Default: None
            The array that must be used to initialize this data column with.
            If *None*, an empty data column is created instead.
        index : int. Default: 0
            The logical index of this data column. This is only important if
            this data column has a parent.
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
            The widget to use as the parent of this data column.
            If *None*, this data column has no parent.

        """

        # Save provided index and parent
        self._index = index
        self._parent = parent

        # Set up the data column
        self.init(data, length)

    # This function sets up the data column
    def init(self, data, length):
        # Set data column name
        self._name = ""

        # If data is None, initialize default array
        if data is None:
            # Set default value for dtype
            self._dtype = np.float64

            # Initialize data array
            # TODO: Should I use a masked array for this?
            self._data = np.zeros(length, dtype=self._dtype)

            # Save the length of the array
            self._length = length

        # If data is not None, act accordingly
        else:
            # Make sure that data is a NumPy array
            data = np.asarray(data)

            # Obtain the dtype of the provided data
            self._dtype = data.dtype.type

            # Set the data array
            self._data = data

            # Save the length of the array
            self._length = len(data)

            # Determine the difference between length and the array length
            diff = length-self._length

            # Extend or shorten the data array accordingly
            if(diff < 0):
                self.removeRows(abs(diff))
            elif(diff > 0):
                self.insertRows(abs(diff))
            else:
                pass

    # Specify the __repr__ function
    def __repr__(self):
        # Make empty list of representations
        str_repr = []

        # Obtain the representation of the NumPy data array
        data_repr = str(self._data.tolist())
        str_repr.append(data_repr)

        # Add length to representation
        str_repr.append("length=%i" % (self._length))

        # Add index to representation if it has a parent
        if self._parent is not None:
            str_repr.append("index=%i" % (self._index))

        # Combine all together to a string and return representation
        return("DataTableColumn(%s)" % (", ".join(str_repr)))

    # Specify the __str__ function
    def __str__(self):
        return(str(self._data))

    # Specify the __getitem__ function
    def __getitem__(self, key):
        return(self._data[key])

    # Specify the __len__ function
    def __len__(self):
        return(self._length)

    # Specify the __setitem__ function
    def __setitem__(self, key, value):
        self._data[key] = value

    # This function is called whenever this column should be deleted
    def delete(self):
        # Delete the data array of this column
        del self._data

    # This property contains the name of this data column
    @property
    def name(self):
        return(self._name)

    # Property setter for name
    @name.setter
    def name(self, name):
        self._name = name

    # This property contains the base name of this data column
    @property
    def base_name(self):
        return(self.to_base_26(self._index+1))

    # This property contains the display name of this data column
    @property
    def display_name(self):
        return(self.name if self.name else self.base_name)

    # This property contains the parent of this data column
    @property
    def parent(self):
        return(self._parent)

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

    # Property setter for dtype
    @dtype.setter
    def dtype(self, dtype):
        # Try to convert the current data to an array with the new dtype
        try:
            new_data = np.asarray(self._data, dtype)
        # If this fails, raise error
        except Exception as error:
            raise TypeError("Data column %r cannot be converted to dtype %r! "
                            "(%s)" % (self._name, dtype, error))
        # If this succeeds, save new array and dtype
        else:
            self._data = new_data
            self._dtype = new_data.dtype.type

    # This property contains the data array of this data column
    @property
    def data(self):
        return(self._data)

    # This function calls the item()-method of the NumPy data array
    def item(self, *args):
        return(self._data.item(*args))

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
    def insertRows(self, count=1, row=None):
        # If row is None, set it to length
        if row is None:
            row = self._length

        # Create an array with zeros of the length required
        insert_array = np.zeros(count, dtype=self._dtype)

        # Insert the array into this data column
        self._data = np.concatenate([self._data[:row],
                                     insert_array,
                                     self._data[row:]])

        # Set the new length of this data column
        self._length += count

    # This function removes rows from the data column starting at given row
    @QC.Slot()
    @QC.Slot(int)
    @QC.Slot(int, int)
    def removeRows(self, count=1, row=None):
        # If row is None, set it to length-count
        if row is None:
            count = min(count, self._length)
            row = self._length-count
        else:
            count = min(count, self._length-row)

        # Create new array with specified rows removed
        self._data = np.delete(self._data, slice(row, row+count))

        # Set the new length of this data column
        self._length -= count

    # This function clears rows from the data column starting at given row
    @QC.Slot(int)
    @QC.Slot(int, int)
    def clearRows(self, row, count=1):
        # Set specified rows to 0
        self._data[row:row+count] = 0
