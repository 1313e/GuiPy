# -*- coding utf-8 -*-

"""
Data Table Widgets
==================

"""


# %% IMPORTS
# Import base modules
from . import data_table, headers, model, selection_model, tab_bar, view
from .data_table import *
from .headers import *
from .model import *
from .selection_model import *
from .tab_bar import *
from .view import *

# All declaration
__all__ = ['data_table', 'headers', 'model', 'selection_model', 'tab_bar',
           'view']
__all__.extend(data_table.__all__)
__all__.extend(headers.__all__)
__all__.extend(model.__all__)
__all__.extend(selection_model.__all__)
__all__.extend(tab_bar.__all__)
__all__.extend(view.__all__)

# Author declaration
__author__ = "Ellert van der Velden (@1313e)"
