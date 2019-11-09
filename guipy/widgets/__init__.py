# -*- coding utf-8 -*-

"""
Widgets
=======
Contains the various different :class:`~PyQt5.QtWidgets.QWidget` subclasses
created for *GuiPy*.

"""


# %% IMPORTS
# Import base modules
from . import core
from .core import *
from . import base
from .base import *
from . import dock
from .dock import *

# All declaration
__all__ = ['base', 'core', 'dock']
__all__.extend(base.__all__)
__all__.extend(core.__all__)
__all__.extend(dock.__all__)
