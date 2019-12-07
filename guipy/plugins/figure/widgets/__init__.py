# -*- coding utf-8 -*-

"""
Figure Widgets
==============

"""


# %% IMPORTS
# Import base modules
from . import figure, options
from .figure import *
from .options import *

# All declaration
__all__ = ['figure', 'options']
__all__.extend(figure.__all__)
__all__.extend(options.__all__)

# Author declaration
__author__ = "Ellert van der Velden (@1313e)"
