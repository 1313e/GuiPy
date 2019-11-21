# -*- coding: utf-8 -*-

"""
Data Table View
===============

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
from guipy.widgets import (
    QW_QAction, QW_QDialog, QW_QLabel, QW_QLineEdit, QW_QMenu, QW_QTableView,
    get_box_value, get_modified_box_signal, set_box_value)

# All declaration
__all__ = ['DataTableView']


# %% CLASS DEFINITIONS
# Define table view widget for the DataTable plugin
# TODO: Save all data in the widget before resizing
# HINT: https://doc.qt.io/qt-5/model-view-programming.html
class DataTableView(QW_QTableView):
    # Initialize DataTableView class
    def __init__(self, parent=None, *args, **kwargs):
        # Call super constructor
        super().__init__(parent)

        # Set up the data table widget
        self.init(*args, **kwargs)

    # This function sets up the data table widget
    def init(self, import_func=None):
        # Create headers
        self.create_headers()

        # Set model for the data table widget
        self.setModel(DataTableModel(self, import_func))

        # Create selection model for the data table widget
        selection_model = DataTableSelectionModel(self.model(), self)

        # Set selection model for the data table widget
        self.selectionModel().deleteLater()
        self.setSelectionModel(selection_model)

    # Override closeEvent to do automatic clean-up
    def closeEvent(self, *args, **kwargs):
        # Delete the model
        self.model().delete()

        # Call super event
        super().closeEvent(*args, **kwargs)

    # This function returns the number of columns in the model
    def columnCount(self):
        return(self.model().columnCount())

    # This function sets the number of columns in the model
    def setColumnCount(self, count):
        # Calculate the difference between count and columnCount
        diff = count-self.columnCount()

        # If diff is negative, remove columns from the end
        if(diff < 0):
            self.model().removeColumns(abs(diff))
        # If diff is positive, append columns to the end
        elif(diff > 0):
            self.model().insertColumns(abs(diff))
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

        # Extend or shorten the data table model accordingly
        if(diff < 0):
            self.model().removeRows(abs(diff))
        elif(diff > 0):
            self.model().insertRows(abs(diff))
        else:
            pass

    # This function creates the headers for the data table
    def create_headers(self):
        # Create context menus for the horizontal and vertical headers
        self.create_header_context_menus()

        # Create popup editor for the horizontal header
        self.h_header_editor = HorizontalHeaderPopup(self)

        # Create horizontal and vertical headers for the data table widget
        self.h_header = HorizontalHeaderView(
            parent=self,
            context_menu=self.show_horizontal_header_context_menu,
            double_clicked=self.h_header_editor)
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
        menu = QW_QMenu('H_Header', parent=self)

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
            triggered=self.remove_cols)
        menu.addAction(remove_act)

        # Add clear action to menu
        clear_act = QW_QAction(
            self, "Clear column",
            statustip="Clear this column",
            triggered=self.clear_cols)
        menu.addAction(clear_act)

        # Add hide action to menu
        hide_act = QW_QAction(
            self, "Hide column",
            statustip="Hide this column",
            triggered=self.hide_cols)
#        menu.addAction(hide_act)

        # Set last requested col to 0
        self._last_context_col = 0

        # Save made menu as an attribute
        self.h_header_menu = menu

    # This function creates the vertical header context menu
    def create_vertical_header_context_menu(self):
        # Create context menu
        menu = QW_QMenu('V_Header', parent=self)

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
            triggered=self.remove_rows)
        menu.addAction(remove_act)

        # Add clear action to menu
        clear_act = QW_QAction(
            self, "Clear row",
            statustip="Clear this row",
            triggered=self.clear_rows)
        menu.addAction(clear_act)

        # Add hide action to menu
        hide_act = QW_QAction(
            self, "Hide row",
            statustip="Hide this row",
            triggered=self.hide_rows)
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

    # This function inserts columns into the data table before given column
    @QC.Slot()
    @QC.Slot(int)
    def insert_cols(self, n_cols=1):
        self.model().insertColumns(n_cols, self._last_context_col)

    # This function inserts columns into the data table after given column
    @QC.Slot()
    @QC.Slot(int)
    def insert_cols_after(self, n_cols=1):
        self.model().insertColumns(n_cols, self._last_context_col+n_cols)

    # This function removes a given column in the data table
    @QC.Slot()
    @QC.Slot(int)
    def remove_cols(self, n_cols=1):
        self.model().removeColumns(n_cols, self._last_context_col)

    # This function clears a given column in the data table
    @QC.Slot()
    @QC.Slot(int)
    def clear_cols(self, n_cols=1):
        self.model().clearColumns(n_cols, self._last_context_col)

    # This function hides a given column in the data table
    @QC.Slot()
    @QC.Slot(int)
    def hide_cols(self, n_cols=1):
        self.model().hideColumns(n_cols, self._last_context_col)

    # This function inserts rows into the data table before given row
    @QC.Slot()
    @QC.Slot(int)
    def insert_rows(self, n_rows=1):
        self.model().insertRows(n_rows, self._last_context_row)

    # This function inserts rows into the data table after given row
    @QC.Slot()
    @QC.Slot(int)
    def insert_rows_after(self, n_rows=1):
        self.model().insertRows(n_rows, self._last_context_row+n_rows)

    # This function removes a given row in the data table
    @QC.Slot()
    @QC.Slot(int)
    def remove_rows(self, n_rows=1):
        self.model().removeRows(n_rows, self._last_context_row)

    # This function clears a given row in the data table
    @QC.Slot()
    @QC.Slot(int)
    def clear_rows(self, n_rows=1):
        self.model().clearRows(n_rows, self._last_context_row)

    # This function hides a given row in the data table
    @QC.Slot()
    @QC.Slot(int)
    def hide_rows(self, n_rows=1):
        self.model().hideRows(n_rows, self._last_context_row)


# Define class for showing a popup editor for the horizontal header
class HorizontalHeaderPopup(QW_QDialog):
    # Initialize HorizontalHeaderPopup class
    def __init__(self, data_table_view_obj, *args, **kwargs):
        # Save provided DataTableView object
        self.data_table = data_table_view_obj

        # Call super constructor
        super().__init__(data_table_view_obj)

        # Set up the header editor
        self.init(*args, **kwargs)

    # This function shows the editor
    @QC.Slot(int)
    def __call__(self, col):
        # Save which column index was requested
        self.col = col

        # Get the column that was requested
        column = self.data_table.model().dataColumn(col)

        # Set the base name and name of this column
        base_name = "Column %s" % (column.base_name)
        set_box_value(self.base_name_label, base_name)
        set_box_value(self.name_box, column.name)

        # Set keyboard focus to the name_box and select it
        self.name_box.setFocus(True)
        self.name_box.selectAll()

        # Show the popup
        self.show()

    # This function sets up the horizontal header popup editor
    def init(self):
        # Install event filter to catch events that should close the popup
        self.installEventFilter(self)

        # Set dialog flags
        self.setWindowFlags(
            QC.Qt.Popup |
            QC.Qt.FramelessWindowHint)

        # Create a grid layout
        layout = QW.QGridLayout()
        self.setLayout(layout)

        # Add a label stating the base name of the column
        self.base_name_label = QW_QLabel("")
        self.base_name_label.setAlignment(QC.Qt.AlignCenter)
        layout.addWidget(self.base_name_label, 0, 0, 1, -1)

        # Create a name line-edit
        name_box = QW_QLineEdit()
        name_box.setToolTip("Set a custom name for this column or leave empty "
                            "to use its default name")
        get_modified_box_signal(name_box).connect(self.set_column_name)

        # Add it to the layout
        layout.addWidget(QW_QLabel("Name"), 1, 0)
        layout.addWidget(name_box, 1, 1)
        self.name_box = name_box

    # Override eventFilter to filter out clicks, ESC and Enter
    def eventFilter(self, widget, event):
        # Check if the event involves anything for which the popup should close
        if (((event.type() == QC.QEvent.MouseButtonPress) and
             not self.geometry().contains(event.globalPos())) or
            ((event.type() == QC.QEvent.KeyPress) and
             event.key() in (QC.Qt.Key_Escape,
                             QC.Qt.Key_Enter,
                             QC.Qt.Key_Return))):
            # Exit the editor
            self.hide()
            self.name_box.setFocus(False)
            return(True)

        # Else, process events as normal
        else:
            return(super().eventFilter(widget, event))

    # Override hideEvent to automatically update the header
    def hideEvent(self, *args, **kwargs):
        # Tell data table to update the header of the requested column
        self.data_table.h_header.headerDataChanged(QC.Qt.Horizontal,
                                                   self.col, self.col)

        # Call super event
        super().hideEvent(*args, **kwargs)

    # This function is called whenever it is attempted to set the column name
    @QC.Slot(str)
    def set_column_name(self, name):
        # Set the column name
        self.data_table.model().setColumnName(self.col, name)
