# -*- coding: utf-8 -*-

"""
Plot Types Core
===============
Collects all the registered plot types for figures into a single dict.

"""


# %% IMPORTS
# Built-in imports
from importlib import import_module
import os
from os import path

# GuiPy imports


# All declaration
__all__ = ['PLOT_TYPES', 'register_plot_type']


# %% GLOBALS
# Define dict of plot types
PLOT_TYPES = {}


# %% FUNCTION DEFINITIONS
# This function registers a plot_type
def register_plot_type(plot_type_class):
    """
    Registers a provided plot type `plot_type_class` for use in *GuiPy*.

    All plot types must be registered with this function in order to be used.

    Parameters
    ----------
    plot_type_class : \
        :class:`~guipy.plugins.figure.widgets.plot_types.BasePlotType` subclass
        The plot type class to use for drawing a given plot.

    """

    # Initialize provided PlotType class
    plot_type = plot_type_class()

    # Register the plot_type
    PLOT_TYPES[plot_type.name] = plot_type
