# -*- coding: utf-8 -*-

"""
Formatters Core
===============
Collects all the registered formatters for data tables into a single dict.

"""


# %% IMPORTS
# Built-in imports
from importlib import import_module
import os
from os import path

# Package imports
from sortedcontainers import SortedDict as sdict

# GuiPy imports
from guipy.config import register_file_format

# All declaration
__all__ = ['FORMATTERS', 'register_formatter']


# %% GLOBALS
# Define list of potential file formats
FORMATS_LIST = [
    "Windows Bitmap (*.bmp)",
    "Comma-Separated Values (*.csv)",
    "Encapsulated PostScript (*.eps)",
    "Flexible Image Transport System (*.fits)",
    "GuiPy Environment File (*.gpy)",
    "Hierarchical Data Format (*.hdf5 *.hdf4 *.hdf *.h5 *.h4 *.he5 *.he2)",
    "Joint Photographic Experts Group (*.jpg *.jpeg)",
    "NumPy Binary File (*.npy)",
    "NumPy Binary Archive (*.npz)",
    "Portable Document Format (*.pdf)",
    "PGF code for LaTeX (*.pgf)",
    "Portable Network Graphics (*.png)",
    "Postscript (*.ps)",
    "Python Script (*.py)",
    "Raw RGBA Bitmap (*.raw *.rgba)",
    "Scalable Vector Graphics (*.svg *.svgz)",
    "Portable Pixmap (*.ppm)",
    "Text Document (*.txt)",
    "X11 Bitmap (*.xbm)",
    "Excel File Format (*.xlsx *.xls)",
    "X11 Pixmap (*.xpm)"]

# Define dict of data table formatters
FORMATTERS = sdict()


# %% FUNCTION DEFINITIONS
# This function registers a data table formatter
def register_formatter(formatter_class):
    """
    Registers a provided data table formatter `formatter_class` for use in
    *GuiPy*.

    All data table formatters must be registered with this function in order to
    be used.

    Parameters
    ----------
    formatter_class : \
        :class:`~guipy.plugins.data_table.formatters.BaseFormatter` subclass
        The formatter class to use for formatting a data table.

    """

    # Initialize provided Formatter class
    formatter = formatter_class()

    # Register the file format that this formatter uses
    register_file_format(formatter.type, formatter.exts)

    # Register the formatter
    for ext in formatter.exts:
        FORMATTERS[ext] = formatter


# This function imports all pre-defined formatters and registers them
def _import_formatters():
    """
    Imports and registers all pre-defined data table formatters for use in
    *GuiPy*.

    """

    # Obtain the path to this directory
    dirpath = path.dirname(__file__)

    # Obtain a list of all files in this directory
    filenames = next(os.walk(dirpath))[2]

    # Remove __init__.py, base.py and core.py
    filenames.remove('__init__.py')
    filenames.remove('base.py')
    filenames.remove('core.py')

    # Loop over all modules and import their Formatter class
    for filename in filenames:
        # Obtain full module name
        modname = "%s.%s" % (__package__, filename[:-3])

        # Import this module
        mod = import_module(modname)

        # Register everything in __all__ as a formatter
        for prop in mod.__all__:
            formatter = getattr(mod, prop)
            register_formatter(formatter)


# Import all defined formatters
_import_formatters()
