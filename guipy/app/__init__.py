# -*- coding: utf-8 -*-

"""
Application
===========
Contains the core application function for using *GuiPy*.

"""


# %% IMPORTS
# Import base modules
from . import main_window
from .main_window import *
from .start import main

# All declaration
__all__ = ['main_window', 'main']
__all__.extend(main_window.__all__)

# Author declaration
__author__ = "Ellert van der Velden (@1313e)"
