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
from matplotlib import rcParams, rcParamsDefault
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW
from sortedcontainers import SortedDict as sdict

# GuiPy imports
from guipy import layouts as GL, plugins as GP, widgets as GW
from guipy.widgets import get_modified_signal, type_box_dict

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

        # Create 'rcParams' group box
        rcParams_group = GW.QGroupBox('rcParams')
        layout.addWidget(rcParams_group)
        rcParams_layout = GL.QVBoxLayout(rcParams_group)

        # Create entries_box
        entries_box = GW.EntriesBox()
        rcParams_layout.addWidget(entries_box)
        self.add_config_entry('rcParams', entries_box)
        self.entries_box = entries_box

        # Create list of all prefixes that should be skipped
        prefix_skip = ('_internal', 'agg', 'animation', 'backend', 'datapath',
                       'docstring', 'figure.figsize', 'interactive', 'keymap',
                       'mpl_toolkits', 'pdf', 'pgf', 'ps', 'savefig', 'svg',
                       'tk', 'toolbar', 'verbose', 'webagg')

        # Add all prefixes that should be skipped for now
        prefix_skip += ('axes.prop_cycle', 'boxplot.bootstrap',
                        'legend.title_fontsize', 'path.sketch')

        # Create dict of all rcParams that use specific widgets
        # TODO: Certain keywords with 'color' have special values
        key_widgets = {
            'axes.edgecolor': GW.ColorBox,
            'axes.facecolor': GW.ColorBox,
            'axes.formatter.limits': lambda: GW.ItemsBox([float, float]),
            'axes.labelcolor': GW.ColorBox,
            'boxplot.boxprops.color': GW.ColorBox,
            'boxplot.capprops.color': GW.ColorBox,
            'boxplot.flierprops.color': GW.ColorBox,
            'boxplot.meanprops.color': GW.ColorBox,
            'boxplot.medianprops.color': GW.ColorBox,
            'boxplot.whiskerprops.color': GW.ColorBox,
            'figure.edgecolor': GW.ColorBox,
            'figure.facecolor': GW.ColorBox,
            'font.cursive': lambda: GW.GenericItemsBox(str),
            'font.family': lambda: GW.GenericItemsBox(str),
            'font.fantasy': lambda: GW.GenericItemsBox(str),
            'font.monospace': lambda: GW.GenericItemsBox(str),
            'font.sans-serif': lambda: GW.GenericItemsBox(str),
            'font.serif': lambda: GW.GenericItemsBox(str),
            'grid.color': GW.ColorBox,
            'hatch.color': GW.ColorBox,
            'image.cmap': GW.ColorMapBox,
            'lines.color': GW.ColorBox,
            'lines.dashdot_pattern': lambda: GW.ItemsBox([float]*4),
            'lines.dashed_pattern': lambda: GW.ItemsBox([float]*2),
            'lines.dotted_pattern': lambda: GW.ItemsBox([float]*2),
            'patch.edgecolor': GW.ColorBox,
            'patch.facecolor': GW.ColorBox,
            'text.color': GW.ColorBox,
            'xtick.color': GW.ColorBox,
            'ytick.color': GW.ColorBox}

        # Initialize empty dict of entry_types
        entry_types = sdict()

        # Loop over all rcParams and determine what widget to use
        for key, value in rcParamsDefault.items():
            # Check if key starts with anything in prefix_skip
            if key.startswith(prefix_skip):
                # If so, continue
                continue

            # Obtain proper box
            box = key_widgets.get(key, type_box_dict[type(value)])

            # Add box to entry_types dict
            entry_types[key] = (box, value)

        # Add all rcParams entries to the box
        entries_box.addEntryTypes(entry_types)

    # This function parses and processes a config section, and returns it
    def decode_config(self, section_dict):
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

        # Decode all values in section_dict
        for key, value in section_dict.items():
            config_dict[key] = literal_eval(value)

        # Return config_dict
        return(config_dict)

    # This function returns a dict containing the default config values
    def get_default_config(self):
        return({'rcParams': sdict()})

    # This function returns its config section, as required by config parser
    def encode_config(self, config_dict):
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

        # Loop over all arguments in config and encode them in
        for key, value in config_dict.items():
            section_dict[key] = '{!r}'.format(dict(value))

        # Return section_dict
        return(section_dict)

    # This function applies the currently stored config
    def apply_config(self, config_dict):
        # Update MPL's rcParams with the values stored in this config page
        rcParams.update(rcParamsDefault)
        rcParams.update(config_dict['rcParams'])
