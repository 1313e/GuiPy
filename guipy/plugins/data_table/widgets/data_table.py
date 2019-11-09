# -*- coding: utf-8 -*-

"""
Data Table Widget
=================

"""


# %% IMPORTS
# Built-in imports

# Package imports
from PyQt5 import QtCore as QC, QtWidgets as QW

# GuiPy imports

# All declaration
__all__ = ['DataTableWidget']


# %% CLASS DEFINITIONS
# Define class for the DataTable widget
# TODO: Allow for columns and rows to be inserted and removed
# TODO: Allow for the column headers to be modified
# TODO: Save all data in the widget before resizing
class DataTableWidget(QW.QTableWidget):
    # Initialize DataTableWidget class
    def __init__(self, parent, *args, **kwargs):
        # Save parent plugin
        self.parent = parent

        # Call super constructor
        super().__init__(parent, *args, **kwargs)

        # Set up the data table widget
        self.init()

    # This function sets up the data table widget
    def init(self):
        # Connect signals from parent
        self.parent.n_rows_changed.connect(self.setRowCount)
        self.parent.n_cols_changed.connect(self.setColumnCount)
