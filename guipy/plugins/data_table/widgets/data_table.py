# -*- coding: utf-8 -*-

"""
Data Table Widget
=================

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy.plugins.data_table.widgets.headers import (
    HorizontalHeaderView, VerticalHeaderView)
from guipy.plugins.data_table.widgets.model import DataTableModel
from guipy.plugins.data_table.widgets.selection_model import (
    DataTableSelectionModel)
from guipy.widgets import QW_QAction, QW_QMenu

# All declaration
__all__ = ['DataTableView']


# %% CLASS DEFINITIONS
# Define table view widget for the DataTable plugin
# TODO: Allow for columns and rows to be inserted and removed
# TODO: Allow for the column headers to be modified
# TODO: Save all data in the widget before resizing
# HINT: https://doc.qt.io/qt-5/model-view-programming.html
class DataTableView(QW.QTableView):
    # Signals
    n_rows_changed = QC.Signal(int)
    n_cols_changed = QC.Signal(int)

    # Initialize DataTableWidget class
    def __init__(self, parent, *args, **kwargs):
        # Save parent plugin
        self.parent = parent

        # Call super constructor
        super().__init__(parent)

        # Set up the data table widget
        self.init(*args, **kwargs)

    # This function sets up the data table widget
    def init(self):
        # Create headers
        self.create_headers()

        # Set model for the data table widget
        self.setModel(DataTableModel(self))

        # Create selection model for the data table widget
        selection_model = DataTableSelectionModel(self.model(), self)

        # Set selection model for the data table widget
        self.selectionModel().deleteLater()
        self.setSelectionModel(selection_model)

        # Connect signals from parent
        self.parent.n_rows_changed.connect(self.setRowCount)
        self.parent.n_cols_changed.connect(self.setColumnCount)

    # This function returns the number of columns in the model
    def columnCount(self):
        return(self.model().columnCount())

    # This function sets the number of columns in the model
    def setColumnCount(self, count):
        # Calculate the difference between count and columnCount
        diff = count-self.columnCount()

        # If diff is negative, remove columns from the end
        if(diff < 0):
            self.model().removeColumns(count=abs(diff))
        # If diff is positive, append columns to the end
        elif(diff > 0):
            self.model().insertColumns(count=abs(diff))
        # If diff is zero, do nothing
        else:
            pass

    # This function returns the number of rows in the model
    def rowCount(self):
        return(self.model().rowCount())

    # This function sets the number of rows in the model
    def setRowCount(self, count):
        # Calculate the difference between count and rowCount
        diff = count-self.rowCount()

        # If diff is negative, remove rows from the end
        if(diff < 0):
            self.model().removeRows(count=abs(diff))
        # If diff is positive, append rows to the end
        elif(diff > 0):
            self.model().insertRows(count=abs(diff))
        # If diff is zero, do nothing
        else:
            pass

    # This function creates the headers for the data table
    def create_headers(self):
        # Create context menus for the horizontal and vertical headers
        self.create_header_context_menus()

        # Create horizontal and vertical headers for the data table widget
        self.h_header = HorizontalHeaderView(
            parent=self,
            context_menu=self.show_horizontal_header_context_menu,
            double_clicked=self.show_horizontal_header_dialog)
        self.v_header = VerticalHeaderView(
            parent=self,
            context_menu=self.show_vertical_header_context_menu)

        # Set headers
        self.setHorizontalHeader(self.h_header)
        self.setVerticalHeader(self.v_header)

    # This function creates the header context menus
    def create_header_context_menus(self):
        self.create_horizontal_header_context_menu()
        self.create_vertical_header_context_menu()

    # This function creates the horizontal header context menu
    def create_horizontal_header_context_menu(self):
        # Create context menu
        menu = QW_QMenu(self, 'H_Header')

        # Add insert_above action to menu
        insert_above_act = QW_QAction(
            self, "Insert column left",
            statustip="Insert a new column left of this one",
            triggered=self.insert_cols)
        menu.addAction(insert_above_act)

        # Add insert_below action to menu
        insert_below_act = QW_QAction(
            self, "Insert column right",
            statustip="Insert a new column right of this one",
            triggered=self.insert_cols_after)
        menu.addAction(insert_below_act)

        # Add remove action to menu
        remove_act = QW_QAction(
            self, "Remove column",
            statustip="Remove this column",
            triggered=self.remove_col)
        menu.addAction(remove_act)

        # Add clear action to menu
        clear_act = QW_QAction(
            self, "Clear column",
            statustip="Clear this column",
            triggered=self.clear_col)
        menu.addAction(clear_act)

        # Add hide action to menu
        hide_act = QW_QAction(
            self, "Hide column",
            statustip="Hide this column",
            triggered=self.hide_col)
#        menu.addAction(hide_act)

        # Set last requested col to 0
        self._last_context_col = 0

        # Save made menu as an attribute
        self.h_header_menu = menu

    # This function creates the vertical header context menu
    def create_vertical_header_context_menu(self):
        # Create context menu
        menu = QW_QMenu(self, 'V_Header')

        # Add insert_above action to menu
        insert_above_act = QW_QAction(
            self, "Insert row above",
            statustip="Insert a new row above this one",
            triggered=self.insert_rows)
        menu.addAction(insert_above_act)

        # Add insert_below action to menu
        insert_below_act = QW_QAction(
            self, "Insert row below",
            statustip="Insert a new row below this one",
            triggered=self.insert_rows_after)
        menu.addAction(insert_below_act)

        # Add remove action to menu
        remove_act = QW_QAction(
            self, "Remove row",
            statustip="Remove this row",
            triggered=self.remove_row)
        menu.addAction(remove_act)

        # Add clear action to menu
        clear_act = QW_QAction(
            self, "Clear row",
            statustip="Clear this row",
            triggered=self.clear_row)
        menu.addAction(clear_act)

        # Add hide action to menu
        hide_act = QW_QAction(
            self, "Hide row",
            statustip="Hide this row",
            triggered=self.hide_row)
#        menu.addAction(hide_act)

        # Set last requested row to 0
        self._last_context_row = 0

        # Save made menu as an attribute
        self.v_header_menu = menu

    # This function shows the horizontal header context menu
    # TODO: Figure out how to use the visual index for insertions
    @QC.Slot(QC.QPoint)
    def show_horizontal_header_context_menu(self, pos):
        # Obtain the logical column the context menu was requested for
        logical_index = self.h_header.logicalIndexAt(pos)

        # Determine which visual column this is
        visual_index = self.h_header.visualIndex(logical_index)

        # Save both indexes
#        self._last_context_col = (logical_index, visual_index)
        self._last_context_col = logical_index

        # Show context menu
        self.h_header_menu.popup(QG.QCursor.pos())

    # This function shows the vertical header context menu
    @QC.Slot(QC.QPoint)
    def show_vertical_header_context_menu(self, pos):
        # Obtain the logical row the context menu was requested for
        logical_index = self.v_header.logicalIndexAt(pos)

        # Determine which visual row this is
        visual_index = self.v_header.visualIndex(logical_index)

        # Save both indexes
#        self._last_context_row = (logical_index, visual_index)
        self._last_context_row = logical_index

        # Show context menu
        self.v_header_menu.popup(QG.QCursor.pos())

    # This function shows a dialog when a column header is double-clicked
    @QC.Slot(int)
    def show_horizontal_header_dialog(self, col):
        print(col)

    # This function inserts columns into the data table before given column
    @QC.Slot()
    @QC.Slot(int)
    @QC.Slot(int, int)
    def insert_cols(self, col=None, n_cols=1):
        # Obtain column
        if col is None:
            col = self._last_context_col

        # Insert columns
        self.model().insertColumn(col)
        self.n_cols_changed.emit(self.columnCount())

    # This function inserts columns into the data table after given column
    @QC.Slot()
    @QC.Slot(int)
    @QC.Slot(int, int)
    def insert_cols_after(self, col=None, n_cols=1):
        # Obtain column
        if col is None:
            col = self._last_context_col

        # Call insert_cols with 'col' modified
        self.insert_cols(col+n_cols, n_cols)

    # This function removes a given column in the data table
    @QC.Slot()
    @QC.Slot(int)
    def remove_col(self, col=None):
        # Obtain column
        if col is None:
            col = self._last_context_col

        # Remove column
        self.model().removeColumn(col+1)
        self.n_cols_changed.emit(self.columnCount())

    # This function clears a given column in the data table
    @QC.Slot()
    @QC.Slot(int)
    def clear_col(self, col=None):
        # Obtain column
        if col is None:
            col = self._last_context_col

        # Clear column
        self.model().clearColumns(col)

    # This function hides a given column in the data table
    @QC.Slot()
    @QC.Slot(int)
    def hide_col(self, col=None):
        # Obtain column
        if col is None:
            col = self._last_context_col

        # Hide column
        self.hideColumn(col)

    # This function inserts rows into the data table before given row
    @QC.Slot()
    @QC.Slot(int)
    @QC.Slot(int, int)
    def insert_rows(self, row=None, n_rows=1):
        # Obtain row
        if row is None:
            row = self._last_context_row

        # Insert rows
        self.model().insertRow(row)
        self.n_rows_changed.emit(self.rowCount())

    # This function inserts rows into the data table after given row
    @QC.Slot()
    @QC.Slot(int)
    @QC.Slot(int, int)
    def insert_rows_after(self, row=None, n_rows=1):
        # Obtain row
        if row is None:
            row = self._last_context_row

        # Call insert_rows with 'row' modified
        self.insert_rows(row+n_rows, n_rows)

    # This function removes a given row in the data table
    @QC.Slot()
    @QC.Slot(int)
    def remove_row(self, row=None):
        # Obtain row
        if row is None:
            row = self._last_context_row

        # Remove row
        self.model().removeRow(row+1)
        self.n_rows_changed.emit(self.rowCount())

    # This function clears a given row in the data table
    @QC.Slot()
    @QC.Slot(int)
    def clear_row(self, row=None):
        # Obtain row
        if row is None:
            row = self._last_context_row

        # Clear row
        self.model().clearRows(row)

    # This function hides a given row in the data table
    @QC.Slot()
    @QC.Slot(int)
    def hide_row(self, row=None):
        # Obtain row
        if row is None:
            row = self._last_context_row

        # Hide row
        self.hideRow(row)
