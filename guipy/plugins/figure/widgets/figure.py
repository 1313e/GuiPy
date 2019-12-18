# -*- coding: utf-8 -*-

"""
Figure Widget
=============

"""


# %% IMPORTS
# Built-in imports

# Package imports
import matplotlib.pyplot as plt
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.layouts import QW_QVBoxLayout
from guipy.plugins.figure.widgets.canvas import FigureCanvas
from guipy.plugins.figure.widgets.manager import FigureManager
from guipy.plugins.figure.widgets.toolbar import FigureToolbar
from guipy.widgets import QW_QWidget

# All declaration
__all__ = ['FigureWidget']


# %% CLASS DEFINITIONS
# Define class for the Figure widget
class FigureWidget(QW_QWidget):
    # Initialize FigureWidget
    def __init__(self, data_table_plugin_obj, num, parent=None, *args,
                 **kwargs):
        # Save provided data table object
        self.data_table_plugin = data_table_plugin_obj
        self.num = num

        # Call super constructor
        super().__init__(parent)

        # Set up the figure widget
        self.init(*args, **kwargs)

    # This function sets up the figure widget
    def init(self):
        # Create a layout
        layout = QW_QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Initialize figure
        self.figure, self.canvas, self.manager, self.toolbar =\
            self.create_figure()

        # Add figure toolbar to layout
        layout.addWidget(self.toolbar)

        # Add a separator
        layout.addSeparator()

        # Add figure canvas to layout
        layout.addWidget(self.canvas)

    # This function creates and returns a figure
    def create_figure(self):
        # Create a figure instance
        figure = plt.Figure()

        # Create a canvas for this figure
        canvas = FigureCanvas(figure)

        # Create a manager for this canvas
        manager = FigureManager(canvas, self.num)

        # Create a toolbar for this figure
        toolbar = FigureToolbar(self.data_table_plugin, canvas, self)

        # Return all
        return(figure, canvas, manager, toolbar)
