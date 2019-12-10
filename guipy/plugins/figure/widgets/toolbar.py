# -*- coding: utf-8 -*-

"""
Figure Toolbar
==============

"""


# %% IMPORTS
# Built-in imports

# Package imports
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT


# All declaration
__all__ = ['FigureToolbar']


# %% CLASS DEFINITIONS
# Custom FigureToolbar class
class FigureToolbar(NavigationToolbar2QT):
    # Initialize FigureToolbar class
    def __init__(self, canvas, parent):
        # Call super constructor
        super().__init__(canvas, parent, coordinates=False)

        # Set up figure toolbar
        self.init()

    # This function sets up the figure toolbar
    def init(self):
        # Create pointer in figure manager to this toolbar
        self.canvas.manager.toolbar = self
