# -*- coding utf-8 -*-

"""
Plugins
=======
Contains the various different plugins that are used in *GuiPy*.

"""


# %% IMPORTS
# Import core modules
from . import base
from .base import *

# Import subpackages
from . import data_table
from .data_table.plugin import *

# All declaration
__all__ = ['base', 'data_table']
__all__.extend(base.__all__)
__all__.extend(data_table.plugin.__all__)

# Author declaration
__author__ = "Ellert van der Velden (@1313e)"
