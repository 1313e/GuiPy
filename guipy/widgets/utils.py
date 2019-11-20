# -*- coding: utf-8 -*-

"""
Widget Utilities
================
Utility functions to make using certain widgets easier.

"""


# %% IMPORTS
# Built-in imports
from os import path
import re

# Package imports
from qtpy import QtWidgets as QW

# GuiPy imports


# All declaration
__all__ = ['getSaveFileName']


# %% GLOBALS
# Define list of all supported file formats
FORMATS_LIST = [
    "Windows Bitmap (*.bmp)",
    "Encapsulated PostScript (*.eps)",
    "Hierarchical Data Format (*.hdf5 *.hdf4 *.hdf *.h5 *.h4 *he5 *.he2)",
    "Joint Photographic Experts Group (*.jpg *.jpeg)",
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
    "X11 Pixmap (*.xpm)"]


# %% HIDDEN DEFINITIONS
# This function converts a list of file formats into a dict of file extensions
def _get_file_exts(formats):
    # Define empty dict of exts
    exts = {}

    # Loop over all file formats in given formats
    for file_format in formats:
        # Obtain all extensions for this file format
        file_exts = re.search(r"[(](.*)[)]", file_format, re.M).group(1)

        # Remove all '*'
        file_exts = file_exts.replace('*.', '')

        # Split exts up into a list
        file_exts = file_exts.split()

        # Add all extensions to exts
        for ext in file_exts:
            exts[ext] = file_format

    # Return exts
    return(exts)


# Obtain dict of all supported file formats
FORMATS = _get_file_exts(FORMATS_LIST)


# %% FUNCTION DEFINITIONS
# Define custom getSaveFileName function that automatically applies filters
def getSaveFileName(parent=None, caption='', basedir=None, filters=None,
                    initial_filter=None, options=None):
    """
    Wrapper for the :func:`~PyQt5.QtWidgets.QFileDialog.getSaveFileName`
    function, which automatically applies several standard options and makes
    using filters easier.

    Optional
    --------
    parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
        The parent to use for creating the save file dialog, or *None* for no
        parent.
    caption : str. Default: ''
        The caption (window title) to use for the save file dialog.
    basedir : str or None. Default: None
        The base directory the save file dialog should start in.
        If *None*, the current directory is used instead.
    filters : list of str or None. Default: None
        List of string extensions to use as the file filters.
        If *None*, no filters are used.
    initial_filter : str or None. Default: None
        The string extension that must be used as the initial filter.
        If `filters` does not contain `initial_filter` or if *None*, no initial
        filter will be applied.
    options : :obj:`~PyQt5.QtWidgets.QFileDialog.Options` object or None. \
        Default: None
        The options to use for this save file dialog, or *None* for no options.

    Returns
    -------
    filename : str
        The filename that was chosen by the user.
    selected_filter : str
        The filter that was used by the user.

    """

    # If basedir is None, set it to the current directory
    if basedir is None:
        basedir = path.abspath('.')

    # Check what filters are given and act accordingly
    if filters is None:
        # If no filters are given, set filters and initial_filter to ''
        filters = ''
        initial_filter = ''
    else:
        # Loop over all filters and grab their formats
        filters = [FORMATS.get(file_filter.lower(), '')
                   for file_filter in filters]

        # Remove duplicates by converting to set and back
        filters = list(set(filters))

        # Remove all empty strings from filters
        if '' in filters:
            filters.remove('')

        # Make sure that filters is sorted
        filters.sort()

        # Add all_files to filters
        filters.append("All Files (*)")

        # Combine all filters into a single string
        filters = ';;'.join(filters)

        # Process given initial_filter
        if initial_filter is None:
            # If initial_filter is None, set to ''
            initial_filter = ''
        elif not initial_filter:
            # If initial_filter is already '', keep it
            pass
        elif initial_filter.lower() in filters:
            # If initial_filter is in the filters, set it to the proper format
            initial_filter = FORMATS[initial_filter.lower()]
        else:
            # Else, the requested filter was not found, thus set it to ''
            initial_filter = ''

    # Open the file saving system and return the result
    if options is None:
        return(QW.QFileDialog.getSaveFileName(
            parent=parent,
            caption=caption,
            directory=basedir,
            filter=filters,
            initialFilter=initial_filter))
    else:
        return(QW.QFileDialog.getSaveFileName(
            parent=parent,
            caption=caption,
            directory=basedir,
            filter=filters,
            initialFilter=initial_filter,
            options=options))
