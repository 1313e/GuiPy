# -*- coding: utf-8 -*-

"""
Base Config
===========
Provides a collection of base functions to standardize the configuration of
*GuiPy*.

"""


# %% IMPORTS
# Package imports
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy import widgets as GW
from guipy.config.manager import CONFIG

# All declaration
__all__ = ['BaseConfigPage']


# %% CLASS DEFINITIONS
# Define base class for making config pages
class BaseConfigPage(GW.BaseBox):
    # Define class attributes
    NAME = ''

    # Initialize config page
    def __init__(self, section_name=None, parent=None):
        # Save the config section name
        self.section_name = self.NAME if section_name is None else section_name

        # Call super constructor
        super().__init__(parent)

        # Set up config page
        self.init()

        # Add this config page to the config manager
        CONFIG.add_config_page(self)

    # This function sets up the config page
    def init(self):
        pass

    # This function retrieves a config value
    def get_option(self, option):
        return(CONFIG.get_option(self.section_name, option))

    # This function parses and processes a config section, and returns it
    def parse_config_section(self, section_dict):
        """
        Parses a section of the config parser, converting it into the values as
        used by *GuiPy* and returns it.

        Parameters
        ----------
        section_dict : dict
            Dict containing the config section belonging to this config page.

        Returns
        -------
        config_dict : dict
            Dict containing the processed config section values. This dict is
            used in *GuiPy* for getting/setting values.

        """

        raise NotImplementedError(self.__class__)

    # This function returns a dict containing the default config values
    def get_default_config(self):
        """
        Returns the default values for the config section belonging to this
        config page.

        Returns
        -------
        default_dict : dict
            Dict containing the default config section values.

        """

        raise NotImplementedError(self.__class__)

    # This function returns its config section, as required by config parser
    def get_config_section(self, config_dict):
        """
        Returns a dict containing the config values for the config section
        associated with this config page.

        Parameters
        ----------
        config_dict : dict
            Dict containing the config values belonging to this config page as
            used by *GuiPy*.

        Returns
        -------
        section_dict : dict
            Dict containing the config section belonging to this config page.
            This dict is used by the config parser to save config values to
            file.

        """

        raise NotImplementedError(self.__class__)
