# -*- coding: utf-8 -*-

"""
Plot Properties Core
====================
Collects all the registered figure plot properties into a single dict.

"""


# %% IMPORTS
# Built-in imports
from importlib import import_module
import os
from os import path

# Package imports
from sortedcontainers import SortedDict as sdict

# All declaration
__all__ = ['PLOT_PROPS', 'register_plot_prop']


# %% GLOBALS
# Define dict of data table formatters
PLOT_PROPS = sdict()


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
    plot_prop_class : :class:`~guipy.plugins.figure.widgets.types.\
        props.BasePlotProp` subclass
        The plot property class to use for formatting a plot property.

    """

    # Register the plot property
    PLOT_PROPS[plot_prop_class.NAME] = plot_prop_class


# This function imports all pre-defined plot properties and registers them
def _import_plot_props():
    """
    Imports and registers all pre-defined plot properties for use in *GuiPy*.

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

        # Register everything in __all__ as a plot property
        for prop in mod.__all__:
            prop_class = getattr(mod, prop)
            register_plot_prop(prop_class)


# Import all defined plot properties
_import_plot_props()
