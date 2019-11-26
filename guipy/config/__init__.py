# -*- coding: utf-8 -*-

"""
Configuration
=============
Contains all the configuration files and functions of *GuiPy*.

"""


# %% IMPORTS
# Import core modules
from . import base, core
from .base import *
from .core import *

# All declaration
__all__ = ['base', 'core']
__all__.extend(base.__all__)
__all__.extend(core.__all__)

# Author declaration
__author__ = "Ellert van der Velden (@1313e)"
