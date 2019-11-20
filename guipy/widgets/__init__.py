# -*- coding utf-8 -*-

"""
Widgets
=======
Contains the various different :class:`~PyQt5.QtWidgets.QWidget` subclasses
created for *GuiPy*.

"""


# %% IMPORTS
# Import base modules
from . import base
from .base import *
from . import core
from .core import *
from . import dock, utils
from .dock import *
from .utils import *

# All declaration
__all__ = ['base', 'core', 'dock', 'utils']
__all__.extend(base.__all__)
__all__.extend(core.__all__)
__all__.extend(dock.__all__)
__all__.extend(utils.__all__)

# Author declaration
__author__ = "Ellert van der Velden (@1313e)"
