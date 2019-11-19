# -*- coding: utf-8 -*-

"""
Data Table Plugin
=================

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.plugins.base import BasePluginWidget
from guipy.plugins.data_table.widgets import DataTableView
from guipy.widgets import (
    QW_QLabel, QW_QSpinBox, get_modified_box_signal, set_box_value)

# All declaration
__all__ = ['DataTable']


# %% CLASS DEFINITIONS
# Define class for the DataTable plugin
class DataTable(BasePluginWidget):
    # Properties
    TITLE = "Data table"

    # Signals
    n_rows_changed = QC.Signal(int)
    n_cols_changed = QC.Signal(int)

    # Initialize DataTable plugin
    def __init__(self, parent, *args, **kwargs):
        # Call super constructor
        super().__init__(parent)

        # Set up the data table plugin
        self.init(*args, **kwargs)

    # This function sets up the data table plugin
    def init(self):
        # Create a layout
        layout = QW.QVBoxLayout()
        self.setLayout(layout)

        # Create a dimensions layout
        dimensions_layout = QW.QHBoxLayout()
        layout.addLayout(dimensions_layout)

        # Add a label to this layout
        dimensions_layout.addWidget(QW_QLabel('Dimensions: '))

        # Create two spinboxes for setting n_rows and n_cols
        n_rows_box = QW_QSpinBox(self)
        n_rows_box.setRange(1, 9999999)
        get_modified_box_signal(n_rows_box).connect(self.n_rows_changed)
        n_cols_box = QW_QSpinBox(self)
        n_cols_box.setRange(1, 702)
        get_modified_box_signal(n_cols_box).connect(self.n_cols_changed)

        # Add spinboxes to dimensions layout
        dimensions_layout.addWidget(n_rows_box)
        dimensions_layout.addWidget(QW_QLabel('X'))
        dimensions_layout.addWidget(n_cols_box)

        # Add a stretcher
        dimensions_layout.addStretch()

        # Create the DataTableView object
        self.data_table = DataTableView(self)

        # Connect signals from data table
        self.data_table.n_rows_changed.connect(
            lambda x: set_box_value(n_rows_box, x))
        self.data_table.n_cols_changed.connect(
            lambda x: set_box_value(n_cols_box, x))

        # Connect signals to data table
        self.n_rows_changed.connect(self.data_table.setRowCount)
        self.n_cols_changed.connect(self.data_table.setColumnCount)

        # Add data_table to the layout
        layout.addWidget(self.data_table)
