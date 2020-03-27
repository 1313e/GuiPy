# -*- coding: utf-8 -*-

"""
Config Manager
==============

"""


# %% IMPORTS
# Built-in imports
from configparser import ConfigParser
import os
from os import path

# Package imports
from qtpy import QtCore as QC
from sortedcontainers import SortedDict as sdict

# GuiPy imports
from guipy import CONFIG_DIR, CONFIG_NAME

# All declaration
__all__ = ['CONFIG']


# %% CLASS DEFINITIONS
# Define config manager
class ConfigManager(object):
    # Initialize config manager
    def __init__(self):
        # Initialize different configuration dicts and parsers
        self.config = sdict()
        self.parser = ConfigParser(interpolation=None)
        self.config_pages = sdict()

    # Initialize config manager for actual use in GuiPy
    def _init(self, parent=None):
        # Save provided parent
        self.parent = parent

        # Read in the configuration file
        self.read_config()

        # Add core config pages
        self._add_config_pages()

        # Save the current system locale
        self.locale = QC.QLocale.system()

    # This function returns the value of a specific config
    def get_option(self, section, option):
        return(self.config[section][option])

    # This function retrieves the config folder
    def _get_config_dir(self):
        """
        Determines the directory that contains the configuration files of
        *GuiPy*, located in the user's home directory, and returns it.
        If it does not exist yet, it will be created first.

        Returns
        -------
        config_dir : str
            Path to the configuration directory of *GuiPy*.

        """

        # Determine the directory that should contain the GuiPy config
        config_dir = path.join(path.expanduser('~'), CONFIG_DIR)

        # If this directory does not exist, make it
        if not path.exists(config_dir):
            os.mkdir(config_dir)

        # Return config_dir
        return(config_dir)

    # This function retrieves the config file
    def _get_config_file(self):
        """
        Determines the main configuration file of *GuiPy*, located in the
        configuration directory, and returns it.

        Returns
        -------
        config_file : str
            Path to the main configuration file of *GuiPy*.

        """

        # Obtain the configuration directory
        config_dir = self._get_config_dir()

        # Determine the file that should contain the GuiPy main config
        config_file = path.join(config_dir, CONFIG_NAME)

        # If the config file does not exist, make an empty one
        if not path.exists(config_file):
            os.mknod(config_file, 0o644)

        # Return config_file
        return(config_file)

    # This function adds the core config pages to the config manager
    def _add_config_pages(self):
        """
        Adds the core config pages to the config manager, which are required by
        *GuiPy* itself.

        """

        # Import all required config pages
        from guipy.config import GeneralConfigPage

        # Add 'General' config page
        GeneralConfigPage()

    # This function adds a config page to the config manager
    def add_config_page(self, config_page):
        """
        Adds a provided :obj:`~guipy.config.BaseConfigPage` `config_page` to
        the config manager.

        """

        # Obtain the section name of this config page
        section_name = config_page.section_name

        # Add the config_page to the config_pages dict
        self.config_pages[section_name] = config_page

        # Check if the section already exists, add it if not
        if not self.parser.has_section(section_name):
            self.parser.add_section(section_name)

        # Obtain the associated config section from the parser
        config_section = self.parser[section_name]

        # Parse the config section belonging to this config page
        parsed_dict = config_page.parse_config_section(config_section)

        # Obtain the default config of this section
        config_dict = config_page.get_default_config()

        # Update default dict with parsed dict
        config_dict.update(parsed_dict)

        # Add this config_dict to the global config
        self.config[section_name] = config_dict

        # Get updated config section from the config page
        config_section = config_page.get_config_section(config_dict)

        # Update the parser with the config_section
        self.parser[section_name] = config_section

    # This function reads in the configuration file from the config folder
    def read_config(self, config_file=None):
        """
        Reads the main configuration file of *GuiPy* given by `config_file`
        into this config manager.

        Optional
        --------
        config_file : str or None. Default: None
            The path to the configuration file to read. If *None*, the default
            is used.

        """

        # Retrieve the configuration file of GuiPy if required
        if config_file is None:
            config_file = self._get_config_file()

        # Read configuration
        self.parser.read(config_file)

    # This function write the current config to the configuration file
    def write_config(self, config_file=None):
        """
        Writes all configuration values in this config manager to the main
        configuration file of *GuiPy* given by `config_file`.

        Optional
        --------
        config_file : str or None. Default: None
            The path to the configuration file to write. If *None*, the default
            is used.

        """

        # Retrieve the configuration file if required
        if config_file is None:
            config_file = self._get_config_file()

        # Write current parser to this file
        with open(config_file, 'w') as config_file:
            self.parser.write(config_file)


# %% IMPORT SCRIPT
# Initialize config manager as CONFIG
CONFIG = ConfigManager()
