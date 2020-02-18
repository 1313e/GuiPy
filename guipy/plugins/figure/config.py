# -*- coding: utf-8 -*-

"""
Base Config
===========

"""


# %% IMPORTS
# Built-in imports
from ast import literal_eval

# Package imports
import cycler
from matplotlib import rcParams
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW
from sortedcontainers import SortedDict as sdict

# GuiPy imports
from guipy.plugins import PluginConfigPage

# All declaration
__all__ = ['MPLrcParamsConfigPage']


# %% CLASS DEFINITIONS
# Define config page for setting MPL's rcParams
class MPLrcParamsConfigPage(PluginConfigPage):
    # Define class attributes
    NAME = 'rcParams'

    # This function parses and processes a config section, and returns it
    def parse_config_section(self, section_dict):
        # Initialize empty dict of parsed config values
        config_dict = sdict()

        # Parse all values in section_dict
        for key, value in section_dict.items():
            # If key is 'axes.prop_cycle', create new cycler object
            if(key == 'axes.prop_cycle'):
                config_dict[key] = cycler.cycler(**literal_eval(value))
            # Else, add it as normal
            else:
                config_dict[key] = literal_eval(value)

        # Return config_dict
        return(config_dict)

    # This function returns a dict containing the default config values
    def get_default_config(self):
        return(sdict(rcParams))

    # This function returns its config section, as required by config parser
    def get_config_section(self, config_dict):
        # Add cat to parser
        section_dict = sdict()

        # Loop over all arguments in config and parse them in
        for key, value in config_dict.items():
            if(key == 'axes.prop_cycle'):
                value = value.by_key()
            section_dict[key] = '{!r}'.format(value)

        return(section_dict)
