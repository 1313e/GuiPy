# -*- coding: utf-8 -*-

"""
Figure Config
=============

"""


# %% IMPORTS
# Built-in imports
from ast import literal_eval
from importlib import import_module

# Package imports
from cycler import cycler
from matplotlib import rcParams, rcParamsDefault
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW
from sortedcontainers import SortedDict as sdict

# GuiPy imports
from guipy import layouts as GL, plugins as GP, widgets as GW
from guipy.widgets import type_box_dict

# All declaration
__all__ = ['MPLConfigPage']


# %% CLASS DEFINITIONS
# Define config page for setting MPL configurations
class MPLConfigPage(GP.PluginConfigPage):
    # Define class attributes
    NAME = 'MPL'

    # This function sets up the MPL config page
    def init(self):
        # Create layout
        layout = GL.QVBoxLayout(self)

        # COLORMAPS
        # Create 'Colormaps' group box
        colormaps_group = GW.QGroupBox('Import colormaps')
        layout.addWidget(colormaps_group)
        colormaps_layout = GL.QFormLayout(colormaps_group)

        # Add label with explaining text
        cmaps_label = GW.QLabel(
            "You can import several Python packages that register colormaps in"
            " <u>matplotlib</u> before a figure is created. Packages that are "
            "not installed are ignored. Please provide each package separated "
            "by a comma, like: <i>cmasher, cmocean</i>")
        colormaps_layout.addRow(cmaps_label)

        # Create box for setting the colormap packages that must be imported
        cmap_pkg_box = GW.QLineEdit()
        colormaps_layout.addRow("Packages:", cmap_pkg_box)
        self.add_config_entry('cmap_packages', cmap_pkg_box, True)

        # RCPARAMS
        # Create 'rcParams' group box
        rcParams_group = GW.QGroupBox('rcParams')
        layout.addWidget(rcParams_group)
        rcParams_layout = GL.QVBoxLayout(rcParams_group)

        # Add label with explaining text
        rcParams_label = GW.QLabel(
            "You can modify most of the <u>rcParams</u> used in "
            "<u>matplotlib</u> below. Adding an entry will override the value "
            "for that specific parameter for every figure created.<br>"
            "See <a href=\"%s\">here</a> for an overview with descriptions of "
            "each parameter." %
            ("https://matplotlib.org/tutorials/introductory/customizing.html"))
        rcParams_layout.addWidget(rcParams_label)

        # Add separator
        rcParams_layout.addSeparator()

        # Create entries_box
        entries_box = GW.EntriesBox()
        rcParams_layout.addWidget(entries_box)
        self.add_config_entry('rcParams', entries_box)

        # Create list of all prefixes that should be skipped
        prefix_skip = ('_internal', 'agg', 'animation', 'backend', 'datapath',
                       'docstring', 'figure.figsize', 'interactive', 'keymap',
                       'mpl_toolkits', 'pdf', 'pgf', 'ps', 'savefig', 'svg',
                       'tk', 'toolbar', 'verbose', 'webagg')

        # Add all prefixes that should be skipped for now
        prefix_skip += ('boxplot.bootstrap', 'legend.title_fontsize',
                        'path.sketch')

        # Create dict of all rcParams that use specific widgets
        # TODO: Certain keywords with 'color' have special values
        key_widgets = {
            'axes.edgecolor': GW.ColorBox,
            'axes.facecolor': GW.ColorBox,
            'axes.formatter.limits': lambda: GW.ItemsBox([float]*2),
            'axes.labelcolor': GW.ColorBox,
            'axes.labelpad': GW.FontSizeBox,
            'axes.labelsize': GW.FontSizeBox,
            'axes.linewidth': GW.FontSizeBox,
            'axes.prop_cycle': lambda: GW.GenericItemsBox(
                lambda: GW.ColorBox(False)),
            'axes.titlepad': GW.FontSizeBox,
            'axes.titlesize': GW.FontSizeBox,
            'boxplot.boxprops.color': GW.ColorBox,
            'boxplot.boxprops.linestyle': GW.LineStyleBox,
            'boxplot.boxprops.linewidth': GW.FontSizeBox,
            'boxplot.capprops.color': GW.ColorBox,
            'boxplot.capprops.linestyle': GW.LineStyleBox,
            'boxplot.capprops.linewidth': GW.FontSizeBox,
            'boxplot.flierprops.color': GW.ColorBox,
            'boxplot.flierprops.linestyle': GW.LineStyleBox,
            'boxplot.flierprops.linewidth': GW.FontSizeBox,
            'boxplot.flierprops.marker': GW.MarkerStyleBox,
            'boxplot.flierprops.markeredgewidth': GW.FontSizeBox,
            'boxplot.flierprops.markersize': GW.FontSizeBox,
            'boxplot.meanprops.color': GW.ColorBox,
            'boxplot.meanprops.linestyle': GW.LineStyleBox,
            'boxplot.meanprops.linewidth': GW.FontSizeBox,
            'boxplot.meanprops.marker': GW.MarkerStyleBox,
            'boxplot.meanprops.markersize': GW.FontSizeBox,
            'boxplot.medianprops.color': GW.ColorBox,
            'boxplot.medianprops.linestyle': GW.LineStyleBox,
            'boxplot.medianprops.linewidth': GW.FontSizeBox,
            'boxplot.whiskerprops.color': GW.ColorBox,
            'boxplot.whiskerprops.linestyle': GW.LineStyleBox,
            'figure.edgecolor': GW.ColorBox,
            'figure.facecolor': GW.ColorBox,
            'figure.titlesize': GW.FontSizeBox,
            'font.cursive': lambda: GW.GenericItemsBox(GW.QFontComboBox),
            'font.family': lambda: GW.GenericItemsBox(GW.QFontComboBox),
            'font.fantasy': lambda: GW.GenericItemsBox(GW.QFontComboBox),
            'font.monospace': lambda: GW.GenericItemsBox(GW.QFontComboBox),
            'font.sans-serif': lambda: GW.GenericItemsBox(GW.QFontComboBox),
            'font.serif': lambda: GW.GenericItemsBox(GW.QFontComboBox),
            'font.size': GW.FontSizeBox,
            'grid.color': GW.ColorBox,
            'grid.linestyle': GW.LineStyleBox,
            'grid.linewidth': GW.FontSizeBox,
            'hatch.color': GW.ColorBox,
            'hatch.linewidth': GW.FontSizeBox,
            'image.cmap': GW.ColorMapBox,
            'legend.borderaxespad': GW.FontSizeBox,
            'legend.borderpad': GW.FontSizeBox,
            'legend.fontsize': GW.FontSizeBox,
            'legend.handletextpad': GW.FontSizeBox,
            'lines.color': GW.ColorBox,
            'lines.dashdot_pattern': lambda: GW.ItemsBox([float]*4),
            'lines.dashed_pattern': lambda: GW.ItemsBox([float]*2),
            'lines.dotted_pattern': lambda: GW.ItemsBox([float]*2),
            'lines.linestyle': GW.LineStyleBox,
            'lines.linewidth': GW.FontSizeBox,
            'lines.marker': GW.MarkerStyleBox,
            'lines.markeredgewidth': GW.FontSizeBox,
            'lines.markersize': GW.FontSizeBox,
            'patch.edgecolor': GW.ColorBox,
            'patch.facecolor': GW.ColorBox,
            'patch.linewidth': GW.FontSizeBox,
            'scatter.marker': GW.MarkerStyleBox,
            'text.color': GW.ColorBox,
            'xtick.color': GW.ColorBox,
            'xtick.labelsize': GW.FontSizeBox,
            'xtick.major.pad': GW.FontSizeBox,
            'xtick.major.size': GW.FontSizeBox,
            'xtick.major.width': GW.FontSizeBox,
            'xtick.minor.pad': GW.FontSizeBox,
            'xtick.minor.size': GW.FontSizeBox,
            'xtick.minor.width': GW.FontSizeBox,
            'ytick.color': GW.ColorBox,
            'ytick.labelsize': GW.FontSizeBox,
            'ytick.major.pad': GW.FontSizeBox,
            'ytick.major.size': GW.FontSizeBox,
            'ytick.major.width': GW.FontSizeBox,
            'ytick.minor.pad': GW.FontSizeBox,
            'ytick.minor.size': GW.FontSizeBox,
            'ytick.minor.width': GW.FontSizeBox}

        # Initialize empty dict of entry_types
        entry_types = sdict()

        # Loop over all rcParams and determine what widget to use
        for key, value in rcParamsDefault.items():
            # Check if key starts with anything in prefix_skip
            if key.startswith(prefix_skip):
                # If so, continue
                continue

            # Obtain proper box
            box = key_widgets.get(key)
            if box is None:
                box = type_box_dict[type(value)]

            # If key is 'axes.prop_cycle', obtain the proper value
            if(key == 'axes.prop_cycle'):
                value = value.by_key()['color']

            # Add box to entry_types dict with default value
            entry_types[key] = (box, value)

        # Add all rcParams entries to the box
        entries_box.addEntryTypes(entry_types)

    # This function parses and processes a config section, and returns it
    def decode_config(self, section_dict):
        # Initialize empty dict of parsed config values
        config_dict = sdict()

        # Decode all values in section_dict
        for key, value in section_dict.items():
            # Convert to Python object
            value = literal_eval(value)

            # Add to dict
            config_dict[key] = value

        # Return config_dict
        return(config_dict)

    # This function returns a dict containing the default config values
    def get_default_config(self):
        return({'rcParams': sdict(),
                'cmap_packages': ("cmasher, cmocean, palettable, colorcet")})

    # This function returns its config section, as required by config parser
    def encode_config(self, config_dict):
        # Initialize empty dict of section config values
        section_dict = sdict()

        # Loop over all arguments in config and encode them in
        for key, value in config_dict.items():
            # Add to dict
            section_dict[key] = '{!r}'.format(value)

        # Return section_dict
        return(section_dict)

    # This function applies the currently stored config
    def apply_config(self, config_dict):
        # Try to import all colormap packages
        pkgs = config_dict['cmap_packages'].replace(' ', '').split(',')
        for pkg in pkgs:
            try:
                import_module(pkg)
            except ImportError:
                pass

        # Obtain rcParams from config_dict and make a copy
        rcParams_config = dict(config_dict['rcParams'])

        # Modify the axes.prop_cycle if it is present
        if 'axes.prop_cycle' in rcParams_config:
            rcParams_config['axes.prop_cycle'] =\
                cycler(color=rcParams_config['axes.prop_cycle'])

        # Update MPL's rcParams with the values stored in this config page
        rcParams.update(rcParamsDefault)
        rcParams.update(rcParams_config)
