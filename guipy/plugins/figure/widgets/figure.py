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
from guipy.widgets import (
    QW_QLabel, QW_QSpinBox, QW_QWidget, get_modified_box_signal, set_box_value)

# All declaration
__all__ = ['FigureWidget']


# %% CLASS DEFINITIONS
# Define class for the Figure widget
class FigureWidget(QW_QWidget):
    # Initialize FigureWidget
    def __init__(self, parent=None, *args, **kwargs):
        # Call super constructor
        super().__init__(parent)

        # Set up the figure widget
        self.init(*args, **kwargs)

    # This function sets up the figure widget
    def init(self):
        # Create a layout
        layout = QW.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
