# -*- coding: utf-8 -*-

"""
Data Table Widget
=================

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.layouts import QW_QHBoxLayout, QW_QVBoxLayout
from guipy.plugins.data_table.widgets.view import DataTableView
from guipy.widgets import (
    QW_QLabel, QW_QSpinBox, QW_QWidget, get_modified_box_signal, set_box_value)

# All declaration
__all__ = ['DataTableWidget']


# %% CLASS DEFINITIONS
# Define class for the DataTable widget
class DataTableWidget(QW_QWidget):
    # Signals
    n_rows_changed = QC.Signal(int)
    n_cols_changed = QC.Signal(int)

    # Initialize DataTableWidget
    def __init__(self, parent=None, *args, **kwargs):
        # Call super constructor
        super().__init__(parent)

        # Set up the data table widget
        self.init(*args, **kwargs)

    # This function sets up the data table widget
    def init(self, import_func=None):
        # Create a layout
        layout = QW_QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Create a dimensions layout
        dimensions_layout = QW_QHBoxLayout()
        layout.addLayout(dimensions_layout)

        # Add a label to this layout
        dimensions_layout.addWidget(QW_QLabel('Dimensions: '))

        # Create two spinboxes for setting n_rows and n_cols
        n_rows_box = QW_QSpinBox(self)
        n_rows_box.setRange(0, 9999999)
        n_rows_box.setToolTip("Number of rows in this data table (max. %i)"
                              % (n_rows_box.maximum()))
        get_modified_box_signal(n_rows_box).connect(self.n_rows_changed)
        n_cols_box = QW_QSpinBox(self)
        n_cols_box.setRange(0, 702)
        n_cols_box.setToolTip("Number of columns in this data table (max. %i)"
                              % (n_cols_box.maximum()))
        get_modified_box_signal(n_cols_box).connect(self.n_cols_changed)

        # Add spinboxes to dimensions layout
        dimensions_layout.addWidget(n_rows_box)
        dimensions_layout.addWidget(QW_QLabel('X'))
        dimensions_layout.addWidget(n_cols_box)

        # Add a stretcher
        dimensions_layout.addStretch()

        # Create the DataTableView object
        self.view = DataTableView(self, import_func)

        # Set initial values of the spinboxes
        set_box_value(n_rows_box, self.view.rowCount())
        set_box_value(n_cols_box, self.view.columnCount())

        # Connect signals from data table view
        self.view.model().rowCountChanged.connect(
            lambda x: set_box_value(n_rows_box, x))
        self.view.model().columnCountChanged.connect(
            lambda x: set_box_value(n_cols_box, x))
        self.view.model().lastColumnRemoved.connect(
            lambda: n_rows_box.setEnabled(False))
        self.view.model().firstColumnInserted.connect(
            lambda: n_rows_box.setEnabled(True))

        # Connect signals to data table view
        self.n_rows_changed.connect(self.view.setRowCount)
        self.n_cols_changed.connect(self.view.setColumnCount)

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
