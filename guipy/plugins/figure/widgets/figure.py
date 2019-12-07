# -*- coding: utf-8 -*-

"""
Figure Widget
=============

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.layouts import QW_QVBoxLayout
from guipy.plugins.figure.widgets.options import FigureOptions
from guipy.widgets import QW_QWidget

# All declaration
__all__ = ['FigureWidget']


# %% CLASS DEFINITIONS
# Define class for the Figure widget
class FigureWidget(QW_QWidget):
    # Initialize FigureWidget
    def __init__(self, data_table_obj, parent=None, *args, **kwargs):
        # Save provided data table object
        self.data_table = data_table_obj

        # Call super constructor
        super().__init__(parent)

        # Set up the figure widget
        self.init(*args, **kwargs)

    # This function sets up the figure widget
    def init(self):
        # Create a layout
        layout = QW_QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Create an options box for this figure
        layout.addWidget(FigureOptions(self.data_table, self))
