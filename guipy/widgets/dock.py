# -*- coding: utf-8 -*-

"""
Dock Widget
===========
Provides the base definition of the dock widgets used in *GuiPy*.

"""


# %% IMPORTS
# Built-in imports

# Package imports
from PyQt5 import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.widgets.base import QW_QDockWidget

# All declaration
__all__ = ['BaseDockWidget']


# %% CLASS DEFINITIONS
# Make base class for dock widgets
class BaseDockWidget(QW_QDockWidget):
    pass
