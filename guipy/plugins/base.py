# -*- coding: utf-8 -*-

"""
Base Plugins
============
Provides a collection of custom :class:`~PyQt5.QtWidgets.QWidget` base classes
that allow for certain plugins to be standardized.

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.widgets import QW_QWidget

# All declaration
__all__ = ['BasePlugin', 'BasePluginWidget']


# %% CLASS DEFINITIONS
# Define base class for making plugins
class BasePlugin(object):
    # Define class attributes
    TITLE = ''
    CONFIG_PAGES = []
    MENU_ACTIONS = {}
    STATUS_WIDGETS = []
    TOOLBARS = []
    TOOLBAR_ACTIONS = {}


# Define base class for making plugin widgets
class BasePluginWidget(QW_QWidget, BasePlugin):
    # Define class attributes
    LOCATION = QC.Qt.LeftDockWidgetArea
