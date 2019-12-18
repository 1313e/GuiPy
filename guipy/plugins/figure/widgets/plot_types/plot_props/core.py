# -*- coding: utf-8 -*-

"""
Plot Properties Core
====================
Collects all the registered figure plot properties into a single dict.

"""


# %% IMPORTS
# Built-in imports

# GuiPy imports
from .data import DataProp
from .line import LineProp
from .marker import MarkerProp


# All declaration
__all__ = ['PLOT_PROPS', 'register_plot_prop']


# %% GLOBALS
# Define dict of data table formatters
PLOT_PROPS = {}


# %% FUNCTION DEFINITIONS
# This function registers a plot property
def register_plot_prop(plot_prop_class):
    """
    Registers a provided plot property class `plot_prop_class` for use in
    *GuiPy*.

    All plot properties must be registered with this function in order to be
    used.

    Parameters
    ----------
    plot_prop_class : :class:`~guipy.plugins.figure.widgets.plot_types.\
        plot_props.BasePlotProp` subclass
        The plot property class to use for formatting a plot property.

    """

    # Register the plot property
    PLOT_PROPS[plot_prop_class.name()] = plot_prop_class


# TODO: Make this automated, as for data table formatters
# Register plot props
register_plot_prop(DataProp)
register_plot_prop(LineProp)
register_plot_prop(MarkerProp)
