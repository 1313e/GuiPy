# -*- coding utf-8 -*-

"""
Data Table
==========

"""


# %% IMPORTS
# Import base modules
from . import plugin
from .plugin import *

# Import subpackages
from . import formatters, widgets

# All declaration
__all__ = ['formatters', 'plugin', 'widgets']
__all__.extend(plugin.__all__)

# Author declaration
__author__ = "Ellert van der Velden (@1313e)"
