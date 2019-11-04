# -*- coding utf-8 -*-

"""
Widgets
=======
Contains the various different :class:`~PyQt5.QtWidgets.QWidget` subclasses
created for *GuiPy*.

"""


# %% IMPORTS
# Import base modules
from . import base_layouts, base_widgets
from .base_layouts import *
from .base_widgets import *

# All declaration
__all__ = ['base_layouts', 'base_widgets']
__all__.extend(base_layouts.__all__)
__all__.extend(base_widgets.__all__)
