# -*- coding: utf-8 -*-

"""
Config Core
===========
Provides a collection of core definitions that are required for all
configurations in *GuiPy*.

"""


# %% IMPORTS
# Package imports
from sortedcontainers import SortedDict as sdict

# All declaration
__all__ = ['FILE_EXTS', 'FILE_FILTERS', 'FILE_FORMATS', 'FILE_TYPES',
           'register_file_format']


# %% GLOBALS
# Define dicts of file extensions, filters, formats and types
FILE_EXTS = sdict()
FILE_FILTERS = sdict()
FILE_FORMATS = sdict()
FILE_TYPES = sdict()


# %% FUNCTION DEFINITIONS
# This function registers a file format
# TODO: Should the MIME type of the file also be given?
def register_file_format(file_type, file_exts):
    """
    Registers a provided file format with type `file_type` and associated
    extensions `file_exts` for use in *GuiPy*.

    All file formats must be registered with this function in order to be used.

    Parameters
    ----------
    file_type : str
        The type of file that is being registered.
        This is usually the extended acronym of the file extension, like
        `'Portable Document Format'` for PDF-files or
        `'Scalable Vector Graphics'` for SVG-files.
    file_exts : list of str
        A list of all the file extensions that are associated with this file
        format. Most of the time, file formats only have a single file
        extension, like `['.pdf']` for PDF-files or `['.py']` for Python
        scripts. However, JPG-files would for example have `['.jpg', '.jpeg']`.
        If `file_exts` contains multiple entries, the first entry is used as
        the preferred file extension for this file format.

    """

    # Convert all provided file_exts to a single string used for filters
    filter_exts = "*%s" % (' *'.join(file_exts))

    # Create a filter format for this file format
    filter_format = "%s (%s)" % (file_type, filter_exts)

    # Loop over all extensions and add to the proper dicts
    for ext in file_exts:
        FILE_EXTS[ext] = filter_exts
        FILE_FILTERS.setdefault(filter_format, ext)
        FILE_FORMATS[ext] = filter_format
        FILE_TYPES[ext] = file_type
