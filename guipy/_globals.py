# -*- coding utf-8 -*-

"""
Globals
=======
Provides a collection of all global variables for *GuiPy* that must be
available.

"""


# %% IMPORTS
# Package imports
import numpy as np
from os import path

# All declaration
__all__ = ['APP_NAME', 'DIR_PATH', 'FLOAT_TYPES', 'INT_TYPES', 'STR_TYPES']


# %% GUI GLOBALS
APP_NAME = 'GuiPy'                                  # Name of application
DIR_PATH = path.abspath(path.dirname(__file__))     # Path to GUI directory


# %% TYPE GLOBALS
INT_TYPES = (int, np.integer)
FLOAT_TYPES = (float, np.floating, *INT_TYPES)
STR_TYPES = (str,)
