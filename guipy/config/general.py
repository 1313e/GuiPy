# -*- coding: utf-8 -*-

"""
General Config
==============

"""


# %% IMPORTS
# Built-in imports
from ast import literal_eval

# Package imports
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW
from sortedcontainers import SortedDict as sdict

# GuiPy imports
from guipy.config import BaseConfigPage

# All declaration
__all__ = ['GeneralConfigPage']


# %% CLASS DEFINITIONS
# Define config page for setting the general config
class GeneralConfigPage(BaseConfigPage):
    # Define class attributes
    NAME = 'General'

    # This function parses and processes a config section, and returns it
    def parse_config_section(self, section_dict):
        # Initialize empty dict of parsed config values
        config_dict = sdict()

        # Parse all values in section_dict
        for key, value in section_dict.items():
            # Add all values to config dict using literal_eval
            config_dict[key] = literal_eval(value)

        # Return config_dict
        return(config_dict)

    # This function returns a dict containing the default config values
    def get_default_config(self):
        # Create default dict
        default_dict = sdict({
            'country': QC.QLocale.system().country(),
            'language': QC.QLocale.system().language()})

        # Return default_dict
        return(default_dict)

    # This function returns its config section, as required by config parser
    def get_config_section(self, config_dict):
        # Initialize empty dict of section config values
        section_dict = sdict()

        # Loop over all arguments in config and parse them in
        for key, value in config_dict.items():
            section_dict[key] = '{!r}'.format(value)

        # Return section_dict
        return(section_dict)
