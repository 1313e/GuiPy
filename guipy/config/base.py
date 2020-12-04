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
from sortedcontainers import SortedDict as sdict

# GuiPy imports
from guipy import widgets as GW
from guipy.config.manager import CONFIG
from guipy.widgets import get_box_value, get_modified_signal, set_box_value

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

        # Initialize empty config_entries dict
        self.config_entries = sdict()

        # Initialize restart_flag
        self.restart_flag = False

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

    # This function adds the provided widget as a config entry
    def add_config_entry(self, name, widget, restart_flag=False):
        """
        Adds the provided `widget` as a config entry to this config page with
        given `name`.
        This allows for the values of `widget` to be tracked and potentially
        discarded/reverted.

        """

        # Make sure that name is lowercase
        name = name.lower()

        # Add widget as an entry to config_entries
        self.config_entries[name] = widget
        get_modified_signal(widget).connect(self.modified)

        # If restart_flag is True, connect set_restart_flag as well
        if restart_flag:
            get_modified_signal(widget).connect(self.set_restart_flag)

    # This function sets restart_flag to True when called
    def set_restart_flag(self):
        self.restart_flag = True

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

    # This function returns a dict containing the current config values
    def get_box_value(self, *value_sig):
        """
        Returns the current values for the config section belonging to this
        config page.

        Returns
        -------
        config_dict : dict
            Dict containing the current config section values.

        """

        # Create empty dict of config values
        config_dict = sdict()

        # Retrieve values of all config entries
        for key, entry_box in self.config_entries.items():
            config_dict[key] = get_box_value(entry_box)

        # Return the config_dict
        return(config_dict)

    # This function sets a config dict as the new config values
    def set_box_value(self, value, *value_sig):
        """
        Sets the values in the provided config dict `value` as the new values
        of the config section belonging to this config page.

        Parameters
        ----------
        value : dict
            Dict containing the new config section values.

        """

        # Assign config_dict
        config_dict = value

        # Set all values contained in the config_dict
        for key, value in config_dict.items():
            entry_box = self.config_entries[key]
            set_box_value(entry_box, value)
