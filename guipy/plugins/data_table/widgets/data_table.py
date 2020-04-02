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
from guipy import layouts as GL, widgets as GW
from guipy.plugins.data_table.widgets.view import DataTableView
from guipy.widgets import get_box_value, get_modified_signal, set_box_value

# All declaration
__all__ = ['DataTableWidget']


# %% CLASS DEFINITIONS
# Define class for the DataTable widget
class DataTableWidget(GW.QWidget):
    # Initialize DataTableWidget
    def __init__(self, parent=None, *args, **kwargs):
        # Call super constructor
        super().__init__(parent)

        # Set up the data table widget
        self.init(*args, **kwargs)

    # This function sets up the data table widget
    def init(self, import_func=None):
        # Create a layout
        layout = GL.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a dimensions layout
        dimensions_layout = GL.QHBoxLayout()
        layout.addLayout(dimensions_layout)

        # Add a label to this layout
        dimensions_layout.addWidget(GW.QLabel('Dimensions: '))

        # Create dual spinbox for setting n_rows and n_cols
        dimensions_box = GW.DualSpinBox((int, int), "X")
        dimensions_layout.addWidget(dimensions_box)
        n_rows_box, n_cols_box = dimensions_box[:]
        n_rows_box.setRange(0, 9999999)
        n_rows_box.setToolTip("Number of rows in this data table (max. %i)"
                              % (n_rows_box.maximum()))
        n_cols_box.setRange(0, 702)
        n_cols_box.setToolTip("Number of columns in this data table (max. %i)"
                              % (n_cols_box.maximum()))
        self.dimensions_box = dimensions_box

        # Create a layout for applying or reverting the dimensions
        buttons_layout = GL.QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(0)
        dimensions_layout.addLayout(buttons_layout)

        # If this theme has a 'cancel' icon, use it
        if QG.QIcon.hasThemeIcon('cancel'):
            rev_icon = QG.QIcon.fromTheme('cancel')
        # Else, use a standard icon
        else:
            rev_icon = self.style().standardIcon(
                QW.QStyle.SP_DialogCancelButton)

        # Create a revert toolbutton
        rev_but = GW.QToolButton()
        rev_but.setToolTip("Revert to current data table dimensions")
        rev_but.setIcon(rev_icon)
        get_modified_signal(rev_but).connect(self.revert_table_dimensions)
        buttons_layout.addWidget(rev_but)

        # If this theme has an 'apply' icon, use it
        if QG.QIcon.hasThemeIcon('apply'):
            app_icon = QG.QIcon.fromTheme('apply')
        # Else, use a standard icon
        else:
            app_icon = self.style().standardIcon(
                QW.QStyle.SP_DialogApplyButton)

        # Create an apply toolbutton
        app_but = GW.QToolButton()
        app_but.setToolTip("Apply new data table dimensions")
        app_but.setIcon(app_icon)
        get_modified_signal(app_but).connect(self.apply_table_dimensions)
        buttons_layout.addWidget(app_but)

        # Add a stretcher
        dimensions_layout.addStretch()

        # Create the DataTableView object
        self.view = DataTableView(self, import_func)

        # Set initial values of the spinboxes
        self.revert_table_dimensions()

        # Connect signals from data table view
        self.view.model().rowCountChanged.connect(
            lambda x: set_box_value(n_rows_box, x))
        self.view.model().columnCountChanged.connect(
            lambda x: set_box_value(n_cols_box, x))
        self.view.model().lastColumnRemoved.connect(
            lambda: n_rows_box.setEnabled(False))
        self.view.model().firstColumnInserted.connect(
            lambda: n_rows_box.setEnabled(True))

        # Add data_table to the layout
        layout.addWidget(self.view)

    # Override closeEvent to perform some additional clean-up
    def closeEvent(self, *args, **kwargs):
        # Close the data table view
        self.view.close()

        # Call super event
        super().closeEvent(*args, **kwargs)

    # This property returns the model of the DataTableView in this data table
    @property
    def model(self):
        return(self.view.model())

    # This function applies the table dimensions as requested by the user
    @QC.Slot()
    def apply_table_dimensions(self):
        # Obtain the values of the dimensions_box
        n_rows, n_cols = get_box_value(self.dimensions_box)

        # Set the rows and columns in the model
        self.view.setRowCount(n_rows)
        self.view.setColumnCount(n_cols)

    # This function reverts the table dimensions back to their current values
    @QC.Slot()
    def revert_table_dimensions(self):
        # Obtain the current table dimensions
        n_rows = self.view.rowCount()
        n_cols = self.view.columnCount()

        # Set the spinboxes to the proper values
        set_box_value(self.dimensions_box, (n_rows, n_cols))
