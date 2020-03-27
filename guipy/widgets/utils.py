# -*- coding: utf-8 -*-

"""
Widget Utilities
================
Utility functions to make using certain widgets easier.

"""


# %% IMPORTS
# Built-in imports
import os
from sys import platform

# Package imports
import e13tools as e13
from sortedcontainers import SortedSet as sset

# GuiPy imports
from guipy import widgets as GW
from guipy.config import FILE_EXTS, FILE_FORMATS

# All declaration
__all__ = ['getOpenFileName', 'getOpenFileNames', 'getSaveFileName']


# %% DOCSTRINGS
optional_doc =\
    """Optional
    --------
    parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
        The parent to use for creating the file dialog, or *None* for no
        parent.
    caption : str. Default: ''
        The caption (window title) to use for the file dialog.
    basedir : str or None. Default: None
        The base directory the file dialog should start in.
        If *None*, the current directory is used instead.
    filters : list of str or None. Default: None
        List of string extensions to use as the file filters.
        If *None*, no filters are used.
    initial_filter : str. Default: ''
        The string extension that must be used as the initial filter.
        If `filters` is empty, no initial filter will be applied.
        If `filters` does not contain `initial_filter` or if empty, the initial
        filter is set to 'All Supported Files'.
    options : :obj:`~PyQt5.QtWidgets.QFileDialog.Options` object or None. \
        Default: None
        The options to use for this file dialog, or *None* for no options."""


# %% HIDDEN DEFINITIONS
# This function processes all arguments provided to a getXXXFileName function
def _processFileDialogArguments(parent=None, caption='', basedir=None,
                                filters=None, initial_filter='', options=None):
    # If basedir is None, set it to the current directory
    if basedir is None:
        basedir = os.getcwd()

    # Check what filters are given and act accordingly
    if filters is None:
        # If no filters are given, set filters and initial_filter to ''
        filters = ''
        initial_filter = ''
    else:
        # Loop over all filters and grab their formats and exts
        formats = sset({FILE_FORMATS.get(file_filter.lower(), '')
                       for file_filter in filters})
        exts = sset({FILE_EXTS.get(file_filter.lower(), '')
                    for file_filter in filters})

        # Remove all empty strings from formats and exts
        if '' in formats:
            formats.remove('')
        if '' in exts:
            exts.remove('')

        # Combine all exts together to a single string
        exts = ' '.join(exts)

        # Convert formats to a list
        formats = list(formats)

        # Add 'All Supported Files' to formats
        formats.append("All supported files (%s)" % (exts))

        # Add 'All Files' to formats
        formats.append("All files (*)")

        # Combine all formats into a single string
        filters = ';;'.join(formats)

        # Process given initial_filter
        if "*"+initial_filter.lower() in exts.split():
            # If initial_filter is in the filters, set it to the proper format
            initial_filter = FILE_FORMATS[initial_filter.lower()]
        else:
            # Else, set to 'All Supported Files'
            initial_filter = formats[-2]

    # Do not use native dialog on Linux, as it is pretty bad
    if platform.startswith('linux'):
        if options is None:
            options = GW.QFileDialog.DontUseNativeDialog
        else:
            options = options | GW.QFileDialog.DontUseNativeDialog

    # Create dict with all arguments
    args_dict = {
        'parent': parent,
        'caption': caption,
        'directory': basedir,
        'filter': filters,
        'initialFilter': initial_filter}

    # If options is not None, add it as well
    if options is not None:
        args_dict['options'] = options

    # Return args_dict
    return(args_dict)


# %% FUNCTION DEFINITIONS
# Define custom getOpenFileName function that automatically applies filters
@e13.docstring_substitute(optional=optional_doc)
def getOpenFileName(*args, **kwargs):
    """
    Wrapper for the :func:`~PyQt5.QtWidgets.QFileDialog.getOpenFileName`
    function, which automatically applies several standard options and makes
    using filters easier.

    %(optional)s

    Returns
    -------
    filename : str
        The filename that was chosen by the user.
    selected_filter : str
        The filter that was used by the user.

    """

    # Process the input arguments
    args_dict = _processFileDialogArguments(*args, **kwargs)

    # Open the file opening system and return the result
    return(GW.QFileDialog.getOpenFileName(**args_dict))


# Define custom getOpenFileNames function that automatically applies filters
@e13.docstring_substitute(optional=optional_doc)
def getOpenFileNames(*args, **kwargs):
    """
    Wrapper for the :func:`~PyQt5.QtWidgets.QFileDialog.getOpenFileNames`
    function, which automatically applies several standard options and makes
    using filters easier.

    %(optional)s

    Returns
    -------
    filenames : list of str
        The filenames that were chosen by the user.
    selected_filter : str
        The filter that was used by the user.

    """

    # Process the input arguments
    args_dict = _processFileDialogArguments(*args, **kwargs)

    # Open the file opening system and return the result
    return(GW.QFileDialog.getOpenFileNames(**args_dict))


# Define custom getSaveFileName function that automatically applies filters
@e13.docstring_substitute(optional=optional_doc)
def getSaveFileName(*args, **kwargs):
    """
    Wrapper for the :func:`~PyQt5.QtWidgets.QFileDialog.getSaveFileName`
    function, which automatically applies several standard options and makes
    using filters easier.

    %(optional)s

    Returns
    -------
    filename : str
        The filename that was chosen by the user.
    selected_filter : str
        The filter that was used by the user.

    """

    # Process the input arguments
    args_dict = _processFileDialogArguments(*args, **kwargs)

    # Open the file saving system and return the result
    return(GW.QFileDialog.getSaveFileName(**args_dict))
