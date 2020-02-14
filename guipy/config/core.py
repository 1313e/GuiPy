# -*- coding: utf-8 -*-

"""
Config Core
===========
Provides a collection of core definitions that are required for all
configurations in *GuiPy*.

"""


# %% IMPORTS
# Built-in imports
from ast import literal_eval
from configparser import ConfigParser
import os
from os import path

# Package imports
import cycler
from sortedcontainers import SortedDict as sdict

# GuiPy imports
from guipy import CONFIG_DIR, CONFIG_NAME

# All declaration
__all__ = ['CONFIG', 'FILE_EXTS', 'FILE_FILTERS', 'FILE_FORMATS', 'FILE_TYPES',
           'read_config', 'ntr', 'register_file_format', 'tr', 'write_config']


# %% GLOBALS
# Define GuiPy configuration settings dict
CONFIG = sdict()

# Define dicts of file extensions, filters, formats and types
FILE_EXTS = sdict()
FILE_FILTERS = sdict()
FILE_FORMATS = sdict()
FILE_TYPES = sdict()


# %% HIDDEN FUNCTION DEFINITIONS
# This function retrieves the config folder, or creates it if it does not exist
def _get_config_dir():
    """
    Determines the directory that contains the configuration files of *GuiPy*,
    located in the user's home directory, and returns it.
    If it does not exist yet, it will be created first.

    Returns
    -------
    config_dir : str
        Path to the configuration directory of *GuiPy*.

    """

    # Determine the directory that should contain the GuiPy config
    config_dir = path.join(path.expanduser('~'), CONFIG_DIR)

    # If this directory does not exist, make it
    if not path.exists(config_dir):
        os.mkdir(config_dir)

    # Return config_dir
    return(config_dir)


# This function retrieves the config file
def _get_config_file():
    """
    Determines the main configuration file of *GuiPy*, located in the
    configuration directory, and returns it.

    Returns
    -------
    config_file : str
        Path to the main configuration file of *GuiPy*.

    """

    # Obtain the configuration directory
    config_dir = _get_config_dir()

    # Determine the file that should contain the GuiPy main config
    config_file = path.join(config_dir, CONFIG_NAME)

    # If the config file does not exist, make it
    if not path.exists(config_file):
        _init_config_file(config_file)

    # Return config_file
    return(config_file)


# This function initializes the config file
def _init_config_file(config_file):
    """
    Initializes a new *GuiPy* configuration file in the provided `config_file`.

    Parameters
    ----------
    config_file : str
        Path to the configuration file that must be initialized.

    """

    # Import the MPL rcParams
    from matplotlib import rcParams

    # Add these to the CONFIG
    CONFIG['rcParams'] = rcParams

    # Write them to file
    write_config(config_file)


# %% FUNCTION DEFINITIONS
# This function marks a string to not be automatically translated
def ntr(text):
    """
    Marks the provided `text` to not be automatically translated if it would be
    passed to the :func:`~tr` function.

    Parameters
    ----------
    text : str
        The text string that should not be automatically translated by
        :func:`~tr`.

    Returns
    -------
    marked_text : str
        The text string `text`, but marked for no auto-translation.

    """

    # For now, just return the text again
    return(text)


# This function reads in the configuration dictionary from the config folder
def read_config(config_file=None):
    """
    Reads the main configuration file of *GuiPy* given by `config_file` into
    the global `CONFIG` :obj:`~configparser.ConfigParser` object.

    Optional
    --------
    config_file : str or None. Default: None
        The path to the configuration file to read. If *None*, the default is
        used.

    """

    # Retrieve the configuration file of GuiPy if required
    if config_file is None:
        config_file = _get_config_file()

    # Read configuration
    parser = ConfigParser(interpolation=None)
    parser.read(config_file)

    # Convert the arguments in parser to the dict
    for cat, config in parser.items():
        # Add cat to CONFIG
        CONFIG[cat] = sdict()

        # Loop over all arguments in config and parse them in
        for key, value in config.items():
            if(key == 'axes.prop_cycle'):
                CONFIG[cat][key] = cycler.cycler(**literal_eval(value))
            else:
                CONFIG[cat][key] = literal_eval(value)


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


# This function automatically translates a text string that is given to it
def tr(text):
    """
    Translates the provided `text` from English to the current language
    setting.

    If no translation exists for `text`, it is returned instead.

    Parameters
    ----------
    text : str
        The text string that needs to be translated to the current language set
        for *GuiPy*.

    Returns
    -------
    translation : str
        The translation of `text` to the current language. If no translation
        exists, `text` is returned instead.

    """

    # For now, just return the text again
    return(text)


# This function write the current config to the configuration directory
def write_config(config_file=None):
    """
    Writes the global `CONFIG` :obj:`~configparser.ConfigParser` object to the
    main configuration file of *GuiPy* given by `config_file`.

    Optional
    --------
    config_file : str or None. Default: None
        The path to the configuration file to write. If *None*, the default is
        used.

    """

    # Retrieve the configuration file if required
    if config_file is None:
        config_file = _get_config_file()

    # Convert the entire CONFIG to a dict with solely strings
    parser = ConfigParser(interpolation=None)
    for cat, config in CONFIG.items():
        # Add cat to parser
        parser[cat] = {}

        # Loop over all arguments in config and parse them in
        for key, value in config.items():
            if(key == 'axes.prop_cycle'):
                value = value.by_key()
            parser[cat][key] = '{!r}'.format(value)

    # Write current config to this file
    with open(config_file, 'w') as config_file:
        parser.write(config_file)
