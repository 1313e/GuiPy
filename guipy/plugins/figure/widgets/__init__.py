# -*- coding utf-8 -*-

"""
Figure Widgets
==============

"""


# %% IMPORTS
# Import base modules
from . import canvas, figure, manager, options, plot_entry, toolbar
from .canvas import *
from .figure import *
from .manager import *
from .options import *
from .plot_entry import *
from .toolbar import *

# Import subpackages
from . import types

# All declaration
__all__ = ['canvas', 'figure', 'manager', 'options', 'plot_entry',
           'toolbar', 'types']
__all__.extend(canvas.__all__)
__all__.extend(figure.__all__)
__all__.extend(manager.__all__)
__all__.extend(options.__all__)
__all__.extend(plot_entry.__all__)
__all__.extend(toolbar.__all__)

# Author declaration
__author__ = "Ellert van der Velden (@1313e)"
