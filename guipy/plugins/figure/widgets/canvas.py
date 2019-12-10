# -*- coding: utf-8 -*-

"""
Figure Canvas
=============

"""


# %% IMPORTS
# Built-in imports

# Package imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


# All declaration
__all__ = ['FigureCanvas']


# %% CLASS DEFINITIONS
# Custom FigureCanvas class
class FigureCanvas(FigureCanvasQTAgg):
    pass
