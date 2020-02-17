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

# Package imports
from sortedcontainers import SortedDict as sdict

# All declaration
__all__ = ['PLOT_TYPES', 'register_plot_type']


# %% GLOBALS
# Define dict of plot types
PLOT_TYPES = {
    '2D': sdict(),
    '3D': sdict()}


# %% FUNCTION DEFINITIONS
# This function registers a plot_type
def register_plot_type(plot_type_class):
    """
    Registers a provided plot type `plot_type_class` for use in *GuiPy*.

    All plot types must be registered with this function in order to be used.

    Parameters
    ----------
    plot_type_class : \
        :class:`~guipy.plugins.figure.widgets.types.BasePlotType` subclass
        The plot type class to use for drawing a given plot.

    """

    # Register the plot_type
    name = plot_type_class.NAME
    axis_type = plot_type_class.AXIS_TYPE
    PLOT_TYPES[axis_type][name] = plot_type_class


# This function imports all pre-defined plot types and registers them
def _import_plot_types():
    """
    Imports and registers all pre-defined plot types for use in *GuiPy*.

    """

    # Obtain the path to this directory
    dirpath = path.dirname(__file__)

    # Obtain a list of all files in this directory
    filenames = next(os.walk(dirpath))[2]

    # Remove __init__.py, base.py and core.py
    filenames.remove('__init__.py')
    filenames.remove('base.py')
    filenames.remove('core.py')

    # Loop over all files remaining
    for filename in filenames:
        # Obtain full module name
        modname = "%s.%s" % (__package__, filename[:-3])

        # Import this module
        mod = import_module(modname)

        # Register everything in __all__ as a plot type
        for type_name in mod.__all__:
            type_class = getattr(mod, type_name)
            register_plot_type(type_class)


# Import all defined plot types
_import_plot_types()
