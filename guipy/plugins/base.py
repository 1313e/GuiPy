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
from sortedcontainers import SortedDict as sdict

# GuiPy imports
from guipy import widgets as GW
from guipy.config import BaseConfigPage

# All declaration
__all__ = ['BasePlugin', 'BasePluginWidget', 'PluginConfigPage']


# %% CLASS DEFINITIONS
# Define base class for making plugins
class BasePlugin(object):
    # Define class attributes
    TITLE = ''
    CONFIG_PAGES = []
    MENU_ACTIONS = {}
    REQ_PLUGINS = []
    STATUS_WIDGETS = []
    TOOLBARS = []
    TOOLBAR_ACTIONS = {}

    # Initialize plugin
    def __init__(self, req_plugins):
        # Save provided req_plugins
        self.req_plugins = req_plugins

        # Add config pages
        self.add_config_pages()

    # This function initializes and adds the config pages for this plugin
    def add_config_pages(self):
        # Initialize empty dict of config pages
        self.config_pages = sdict()

        # Initialize all config pages of this plugin
        for config_page in self.CONFIG_PAGES:
            # Initialize config_page
            self.config_pages[config_page.NAME] = config_page(self)

    # This function retrieves a config value
    def get_option(self, section, option):
        return(self.config_pages[section].get_option(option))


# Define base class for making plugin widgets
class BasePluginWidget(GW.QWidget, BasePlugin):
    # Define class attributes
    LOCATION = QC.Qt.LeftDockWidgetArea


# Define base class for making plugin config pages
class PluginConfigPage(BaseConfigPage):
    # Initialize plugin config page
    def __init__(self, plugin, parent=None):
        # Save provided plugin
        self.plugin = plugin

        # Call super constructor
        super().__init__(f'plugin:{plugin.TITLE}/{self.NAME}', parent)
