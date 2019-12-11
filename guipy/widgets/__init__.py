# -*- coding utf-8 -*-

"""
Widgets
=======
Contains the various different :class:`~PyQt5.QtWidgets.QWidget` subclasses
created for *GuiPy*.

"""


# %% IMPORTS
# Import core modules
from . import base, core
from .base import *
from .core import *

# Import base modules
from . import color, combobox, dock, exceptions, spinbox, tabbar, utils
from .color import *
from .combobox import *
from .dock import *
from .exceptions import *
from .spinbox import *
from .tabbar import *
from .utils import *

# All declaration
__all__ = ['base', 'color', 'combobox', 'core', 'dock', 'exceptions',
           'spinbox', 'tabbar', 'utils']
__all__.extend(base.__all__)
__all__.extend(color.__all__)
__all__.extend(combobox.__all__)
__all__.extend(core.__all__)
__all__.extend(dock.__all__)
__all__.extend(exceptions.__all__)
__all__.extend(spinbox.__all__)
__all__.extend(tabbar.__all__)
__all__.extend(utils.__all__)

# Author declaration
__author__ = "Ellert van der Velden (@1313e)"
