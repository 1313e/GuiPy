# -*- coding: utf-8 -*-

"""
Figure Config
=============

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
from guipy import layouts as GL, plugins as GP, widgets as GW
from guipy.widgets import get_modified_signal

# All declaration
__all__ = ['MPLConfigPage']


# %% CLASS DEFINITIONS
# Define config page for setting MPL's rcParams
class MPLConfigPage(GP.PluginConfigPage):
    # Define class attributes
    NAME = 'MPL'

    # This function sets up the rcParams config page
    def init(self):
        # Create layout
        layout = GL.QVBoxLayout(self)

        # Create entries_box
        entries_box = GW.EntriesBox()
        layout.addWidget(entries_box)
        self.add_config_entry('rcParams', entries_box)
        self.entries_box = entries_box

        # Initialize empty dict of entry_types
        entry_types = sdict()

        # Loop over all rcParams and determine what widget to use
        for key, value in rcParams.items():
            # For now, use default widgets for everything
            entry_types[key] = None

        # Add all rcParams entries to the box
        entries_box.addEntryTypes(entry_types)

    # This function parses and processes a config section, and returns it
    def decode_config_section(self, section_dict):
        # Initialize empty dict of parsed config values
        config_dict = sdict()

#        # Parse all values in section_dict
#        for key, value in section_dict.items():
#            # If key is 'axes.prop_cycle', create new cycler object
#            if(key == 'axes.prop_cycle'):
#                config_dict[key] = cycler.cycler(**literal_eval(value))
#            # Else, add it as normal
#            else:
#                config_dict[key] = literal_eval(value)

        # Parse all values in section_dict
        for key, value in section_dict.items():
            config_dict[key] = literal_eval(value)

        # Return config_dict
        return(config_dict)

    # This function returns a dict containing the default config values
    def get_default_config(self):
        return(sdict())

    # This function returns its config section, as required by config parser
    def encode_config_section(self, config_dict):
        # Initialize empty dict of section config values
        section_dict = sdict()

#        # Loop over all arguments in config and parse them in
#        for key, value in config_dict.items():
#            # If key is 'axes.prop_cycle', retrieve the cycler values first
#            if(key == 'axes.prop_cycle'):
#                value = value.by_key()
#
#            # Add raw string value
#            section_dict[key] = '{!r}'.format(value)

        # Loop over all arguments in config and parse them in
        for key, value in config_dict.items():
            section_dict[key] = '{!r}'.format(dict(value))

        # Return section_dict
        return(section_dict)
