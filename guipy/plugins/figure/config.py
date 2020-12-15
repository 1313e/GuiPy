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
import matplotlib as mpl
from matplotlib import rcParams, rcParamsDefault
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW
from sortedcontainers import SortedDict as sdict

# GuiPy imports
from guipy import layouts as GL, plugins as GP, widgets as GW
from guipy.widgets import (
    create_combobox, get_box_value, type_box_dict, set_box_value)

# All declaration
__all__ = ['MPLConfigPage']


# %% HELPER DEFINITIONS
# Create custom togglebox class
class AutoToggleBox(GW.ToggleBox):
    def __init__(self, widget, untoggled):
        # Call super constructor
        super().__init__(widget)

        # Save untoggled
        self.untoggled = untoggled

    # Override get_box_value to return untoggled when the bool is False
    def get_box_value(self, *value_sig):
        # Obtain value of checkbox
        check = get_box_value(self.checkbox)

        # If True, value is obtained from the widget
        if check:
            value = get_box_value(self.widget, *value_sig)
        else:
            value = self.untoggled

        # Return value
        return(value)

    # Override set_box_value to allow for untoggled to toggle the box
    def set_box_value(self, value, *value_sig):
        # Check if value is untoggled
        if(value == self.untoggled):
            # If so, toggle the widget
            set_box_value(self.checkbox, False)
        else:
            # Else, set the checkbox to True and set the value
            set_box_value(self.checkbox, True)
            set_box_value(self.widget, value, *value_sig)


# Create custom combobox class that allows for bools to be used as well
class BoolComboBox(GW.QComboBox):
    def __init__(self, items, *args, **kwargs):
        # Call super constructor
        super().__init__(*args, **kwargs)

        # Initialize uses_bools flag
        self.uses_bools = False

        # Add provided items
        self.addItems(items)

    # Override addItems to handle bools differently
    def addItems(self, items):
        # Make empty lists to separate normal items and bools
        std_items = []
        bool_items = []

        # Loop over all items and separate them into the proper lists
        for item in items:
            # Check if this item is a bool or None
            if item in (True, False, None):
                # If so, save this
                self.uses_bools = True

                # Convert to string and add to bool_items
                bool_items.append(str(item))
            else:
                # Else, add to std_items
                std_items.append(item)

        # Call super method on bool_items
        super().addItems(bool_items)

        # Add a separator
        self.insertSeparator(len(bool_items))

        # Call super method on std_items
        super().addItems(std_items)

    # Add special get_box_value to convert bool-strings to bools
    def get_box_value(self, *value_sig):
        # Use normal method
        value = get_box_value(self, *value_sig, no_custom=True)

        # If the returned value is a bool and bools are used, convert value
        if value in ('True', 'False', 'None') and self.uses_bools:
            value = literal_eval(value)

        # Return value
        return(value)

    # Add special set_box_value to convert bools to bool-strings
    def set_box_value(self, value, *value_sig):
        # If the given value is a bool and bools are used, convert value
        if value in (True, False, None) and self.uses_bools:
            value = str(value)

        # Set value
        set_box_value(self, value, *value_sig, no_custom=True)


# Create function that returns spinbox to use for setting n_bins
def get_n_bins_box():
    # Make spinbox for bin count
    n_bins_box = GW.QSpinBox()
    n_bins_box.setRange(0, 100)
    n_bins_box.setSpecialValueText('auto')

    # Return it
    return(n_bins_box)


# Create custom spinbox that only allows values between 0 and 1
class UnitySpinBox(GW.QDoubleSpinBox):
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(*args, **kwargs)

        # Set unity range
        self.setDecimals(5)
        self.setRange(0, 1)


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
        prefix_skip = ('_internal', 'agg', 'animation', 'backend',
                       'boxplot.bootstrap', 'datapath', 'docstring',
                       'figure.figsize', 'figure.max_open_warning',
                       'image.aspect', 'image.composite_image', 'image.origin',
                       'interactive', 'keymap', 'lines.color', 'mpl_toolkits',
                       'path', 'pdf', 'pgf', 'ps', 'savefig', 'svg',
                       'text.kerning_factor', 'tk', 'toolbar', 'verbose',
                       'webagg')

        # Create a combobox factory for text weights
        text_weight_box = create_combobox(
            ['normal', 'bold', 'bolder', 'lighter', '100', '200', '300', '400',
             '500', '600', '700', '800', '900'])

        # Create dict of all rcParams that use specific widgets
        key_widgets = {
            'axes.autolimit_mode': create_combobox(['data', 'round_numbers']),
            'axes.axisbelow': lambda: BoolComboBox([True, 'line', False]),
            'axes.edgecolor': GW.ColorBox,
            'axes.facecolor': GW.ColorBox,
            'axes.formatter.limits': lambda: GW.ItemsBox([int]*2),
            'axes.formatter.min_exponent': GW.QSpinBox,
            'axes.formatter.offset_threshold': GW.QSpinBox,
            'axes.formatter.use_locale': GW.QCheckBox,
            'axes.formatter.use_mathtext': GW.QCheckBox,
            'axes.formatter.useoffset': GW.QCheckBox,
            'axes.grid': GW.QCheckBox,
            'axes.grid.axes': create_combobox(['major', 'minor', 'both']),
            'axes.grid.which': create_combobox(['major', 'minor', 'both']),
            'axes.labelcolor': GW.ColorBox,
            'axes.labelpad': GW.FontSizeBox,
            'axes.labelsize': GW.FontSizeBox,
            'axes.labelweight': text_weight_box,
            'axes.linewidth': GW.FontSizeBox,
            'axes.prop_cycle': lambda: GW.GenericItemsBox(
                lambda: GW.ColorBox(False)),
            'axes.spines.bottom': GW.QCheckBox,
            'axes.spines.left': GW.QCheckBox,
            'axes.spines.right': GW.QCheckBox,
            'axes.spines.top': GW.QCheckBox,
            'axes.titlecolor': lambda: AutoToggleBox(GW.ColorBox(), 'auto'),
            'axes.titlelocation': create_combobox(['left', 'center', 'right']),
            'axes.titlepad': GW.FontSizeBox,
            'axes.titlesize': GW.FontSizeBox,
            'axes.titleweight': text_weight_box,
            'axes.unicode_minus': GW.QCheckBox,
            'axes.xmargin': UnitySpinBox,
            'axes.ymargin': UnitySpinBox,
            'axes3d.grid': GW.QCheckBox,
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
            'boxplot.flierprops.markeredgecolor': lambda: AutoToggleBox(
                GW.ColorBox(), 'none'),
            'boxplot.flierprops.markeredgewidth': GW.FontSizeBox,
            'boxplot.flierprops.markerfacecolor': lambda: AutoToggleBox(
                GW.ColorBox(), 'none'),
            'boxplot.flierprops.markersize': GW.FontSizeBox,
            'boxplot.meanline': GW.QCheckBox,
            'boxplot.meanprops.color': GW.ColorBox,
            'boxplot.meanprops.linestyle': GW.LineStyleBox,
            'boxplot.meanprops.linewidth': GW.FontSizeBox,
            'boxplot.meanprops.marker': GW.MarkerStyleBox,
            'boxplot.meanprops.markeredgecolor': lambda: AutoToggleBox(
                GW.ColorBox(), 'none'),
            'boxplot.meanprops.markerfacecolor': lambda: AutoToggleBox(
                GW.ColorBox(), 'none'),
            'boxplot.meanprops.markersize': GW.FontSizeBox,
            'boxplot.medianprops.color': GW.ColorBox,
            'boxplot.medianprops.linestyle': GW.LineStyleBox,
            'boxplot.medianprops.linewidth': GW.FontSizeBox,
            'boxplot.notch': GW.QCheckBox,
            'boxplot.showbox': GW.QCheckBox,
            'boxplot.showcaps': GW.QCheckBox,
            'boxplot.showfliers': GW.QCheckBox,
            'boxplot.showmeans': GW.QCheckBox,
            'boxplot.vertical': GW.QCheckBox,
            'boxplot.whiskerprops.color': GW.ColorBox,
            'boxplot.whiskerprops.linestyle': GW.LineStyleBox,
            'boxplot.whiskerprops.linewidth': GW.FontSizeBox,
            'boxplot.whiskers': GW.FloatLineEdit,
            'contour.corner_mask': lambda: BoolComboBox(
                [True, False, 'legacy']),
            'contour.negative_linestyle': GW.LineStyleBox,
            'date.autoformatter.day': GW.QLineEdit,
            'date.autoformatter.hour': GW.QLineEdit,
            'date.autoformatter.microsecond': GW.QLineEdit,
            'date.autoformatter.minute': GW.QLineEdit,
            'date.autoformatter.month': GW.QLineEdit,
            'date.autoformatter.second': GW.QLineEdit,
            'date.autoformatter.year': GW.QLineEdit,
            'errorbar.capsize': GW.FloatLineEdit,
            'figure.autolayout': GW.QCheckBox,
            'figure.constrained_layout.h_pad': UnitySpinBox,
            'figure.constrained_layout.hspace': UnitySpinBox,
            'figure.constrained_layout.use': GW.QCheckBox,
            'figure.constrained_layout.w_pad': UnitySpinBox,
            'figure.constrained_layout.wspace': UnitySpinBox,
            'figure.dpi': GW.FloatLineEdit,
            'figure.edgecolor': GW.ColorBox,
            'figure.facecolor': GW.ColorBox,
            'figure.frameon': GW.QCheckBox,
            'figure.subplot.bottom': UnitySpinBox,
            'figure.subplot.hspace': UnitySpinBox,
            'figure.subplot.left': UnitySpinBox,
            'figure.subplot.right': UnitySpinBox,
            'figure.subplot.top': UnitySpinBox,
            'figure.subplot.wspace': UnitySpinBox,
            'figure.titlesize': GW.FontSizeBox,
            'figure.titleweight': text_weight_box,
            'font.cursive': lambda: GW.GenericItemsBox(GW.QFontComboBox),
            'font.family': lambda: GW.GenericItemsBox(GW.QFontComboBox),
            'font.fantasy': lambda: GW.GenericItemsBox(GW.QFontComboBox),
            'font.monospace': lambda: GW.GenericItemsBox(GW.QFontComboBox),
            'font.sans-serif': lambda: GW.GenericItemsBox(GW.QFontComboBox),
            'font.serif': lambda: GW.GenericItemsBox(GW.QFontComboBox),
            'font.size': GW.FontSizeBox,
            'font.stretch': create_combobox(
                ['ultra-condensed', 'extra-condensed', 'condensed',
                 'semi-condensed', 'normal', 'semi-expanded', 'expanded',
                 'extra-expanded', 'ultra-expanded', 'wider', 'narrower']),
            'font.style': create_combobox(['normal', 'italic', 'oblique']),
            'font.variant': create_combobox(['normal', 'small-caps']),
            'font.weight': text_weight_box,
            'grid.alpha': UnitySpinBox,
            'grid.color': GW.ColorBox,
            'grid.linestyle': GW.LineStyleBox,
            'grid.linewidth': GW.FontSizeBox,
            'hatch.color': GW.ColorBox,
            'hatch.linewidth': GW.FontSizeBox,
            'hist.bins': get_n_bins_box,
            'image.cmap': GW.ColorMapBox,
            'image.interpolation': create_combobox(
                ['none', 'antialiased', 'nearest', 'bilinear', 'bicubic',
                 'spline16', 'spline36', 'hanning', 'hamming', 'hermite',
                 'kaiser', 'quadric', 'catrom', 'gaussian', 'bessel',
                 'mitchell', 'sinc', 'lanczos']),
            'image.lut': GW.IntLineEdit,
            'image.resample': GW.QCheckBox,
            'legend.borderaxespad': GW.FontSizeBox,
            'legend.borderpad': GW.FontSizeBox,
            'legend.columnspacing': GW.FontSizeBox,
            'legend.edgecolor': GW.ColorBox,
            'legend.facecolor': lambda: AutoToggleBox(
                GW.ColorBox(), 'inherit'),
            'legend.fancybox': GW.QCheckBox,
            'legend.fontsize': GW.FontSizeBox,
            'legend.framealpha': UnitySpinBox,
            'legend.frameon': GW.QCheckBox,
            'legend.handleheight': GW.FontSizeBox,
            'legend.handlelength': GW.FontSizeBox,
            'legend.handletextpad': GW.FontSizeBox,
            'legend.labelspacing': GW.FontSizeBox,
            'legend.loc': create_combobox(mpl.legend.Legend.codes.keys()),
            'legend.markerscale': GW.FloatLineEdit,
            'legend.numpoints': GW.IntLineEdit,
            'legend.scatterpoints': GW.IntLineEdit,
            'legend.shadow': GW.QCheckBox,
            'legend.title_fontsize': lambda: AutoToggleBox(
                GW.FontSizeBox(), None),
            'lines.antialiased': GW.QCheckBox,
            'lines.dash_capstyle': create_combobox(
                ['butt', 'projecting', 'round']),
            'lines.dash_joinstyle': create_combobox(
                ['bevel', 'miter', 'round']),
            'lines.dashdot_pattern': lambda: GW.ItemsBox([float]*4),
            'lines.dashed_pattern': lambda: GW.ItemsBox([float]*2),
            'lines.dotted_pattern': lambda: GW.ItemsBox([float]*2),
            'lines.linestyle': GW.LineStyleBox,
            'lines.linewidth': GW.FontSizeBox,
            'lines.marker': GW.MarkerStyleBox,
            'lines.markeredgecolor': lambda: AutoToggleBox(
                GW.ColorBox(), 'auto'),
            'lines.markeredgewidth': GW.FontSizeBox,
            'lines.markerfacecolor': lambda: AutoToggleBox(
                GW.ColorBox(), 'auto'),
            'lines.markersize': GW.FontSizeBox,
            'lines.scale_dashes': GW.QCheckBox,
            'lines.solid_capstyle': create_combobox(
                ['butt', 'projecting', 'round']),
            'lines.solid_joinstyle': create_combobox(
                ['bevel', 'miter', 'round']),
            'markers.fillstyle': create_combobox(
                ['full', 'left', 'right', 'bottom', 'top', 'none']),
            'mathtext.bf': GW.QLineEdit,
            'mathtext.cal': GW.QLineEdit,
            'mathtext.default': GW.QLineEdit,
            'mathtext.fallback_to_cm': GW.QCheckBox,
            'mathtext.fontset': create_combobox(
                ['dejavusans', 'cm', 'stix', 'stixsans', 'custom']),
            'mathtext.it': GW.QLineEdit,
            'mathtext.rm': GW.QLineEdit,
            'mathtext.sf': GW.QLineEdit,
            'mathtext.tt': GW.QLineEdit,
            'patch.antialiased': GW.QCheckBox,
            'patch.edgecolor': GW.ColorBox,
            'patch.facecolor': GW.ColorBox,
            'patch.force_edgecolor': GW.QCheckBox,
            'patch.linewidth': GW.FontSizeBox,
            'polaraxes.grid': GW.QCheckBox,
            'scatter.edgecolors': lambda: AutoToggleBox(
                GW.ColorBox(), 'face'),
            'scatter.marker': GW.MarkerStyleBox,
            'text.antialiased': GW.QCheckBox,
            'text.color': GW.ColorBox,
            'text.hinting': create_combobox(
                ['either', 'native', 'auto', 'none']),
            'text.hinting_factor': GW.IntLineEdit,
            'text.latex.preamble': GW.QLineEdit,
            'text.latex.preview': GW.QCheckBox,
            'text.usetex': GW.QCheckBox,
            'timezone': GW.QLineEdit,
            'xtick.alignment': create_combobox(['left', 'center', 'right']),
            'xtick.bottom': GW.QCheckBox,
            'xtick.color': GW.ColorBox,
            'xtick.direction': create_combobox(['in', 'out', 'inout']),
            'xtick.labelbottom': GW.QCheckBox,
            'xtick.labelsize': GW.FontSizeBox,
            'xtick.labeltop': GW.QCheckBox,
            'xtick.major.bottom': GW.QCheckBox,
            'xtick.major.pad': GW.FontSizeBox,
            'xtick.major.size': GW.FontSizeBox,
            'xtick.major.top': GW.QCheckBox,
            'xtick.major.width': GW.FontSizeBox,
            'xtick.minor.bottom': GW.QCheckBox,
            'xtick.minor.pad': GW.FontSizeBox,
            'xtick.minor.size': GW.FontSizeBox,
            'xtick.minor.top': GW.QCheckBox,
            'xtick.minor.visible': GW.QCheckBox,
            'xtick.minor.width': GW.FontSizeBox,
            'xtick.top': GW.QCheckBox,
            'ytick.alignment': create_combobox(
                ['left_baseline', 'center_baseline', 'right_baseline']),
            'ytick.color': GW.ColorBox,
            'ytick.direction': create_combobox(['in', 'out', 'inout']),
            'ytick.labelleft': GW.QCheckBox,
            'ytick.labelright': GW.QCheckBox,
            'ytick.labelsize': GW.FontSizeBox,
            'ytick.left': GW.QCheckBox,
            'ytick.major.left': GW.QCheckBox,
            'ytick.major.pad': GW.FontSizeBox,
            'ytick.major.right': GW.QCheckBox,
            'ytick.major.size': GW.FontSizeBox,
            'ytick.major.width': GW.FontSizeBox,
            'ytick.minor.left': GW.QCheckBox,
            'ytick.minor.pad': GW.FontSizeBox,
            'ytick.minor.right': GW.QCheckBox,
            'ytick.minor.size': GW.FontSizeBox,
            'ytick.minor.visible': GW.QCheckBox,
            'ytick.minor.width': GW.FontSizeBox,
            'ytick.right': GW.QCheckBox}

        # Initialize empty dict of entry_types
        entry_types = sdict()

        # Loop over all rcParams and determine what widget to use
        for key, value in rcParamsDefault.items():
            # Check if key starts with anything in prefix_skip
            if key.startswith(prefix_skip):
                # If so, continue
                continue

            # Obtain proper box
            box = key_widgets.get(key, GW.LongGenericBox)

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
        return({'rcParams': {},
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
