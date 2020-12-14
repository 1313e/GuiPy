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
from . import (
    checkbox, color, combobox, dock, entriesbox, exceptions, genericbox,
    itemsbox, lineedit, radiobutton, spinbox, style, tabbar, text, utils)
from .checkbox import *
from .color import *
from .combobox import *
from .dock import *
from .entriesbox import *
from .exceptions import *
from .genericbox import *
from .itemsbox import *
from .lineedit import *
from .radiobutton import *
from .spinbox import *
from .style import *
from .tabbar import *
from .text import *
from .utils import *

# Import misc module
from . import misc
from .misc import *

# All declaration
__all__ = ['base', 'checkbox', 'color', 'combobox', 'core', 'dock',
           'entriesbox', 'exceptions', 'genericbox', 'itemsbox', 'lineedit',
           'misc', 'radiobutton', 'spinbox', 'style', 'tabbar', 'text',
           'utils']
__all__.extend(base.__all__)
__all__.extend(checkbox.__all__)
__all__.extend(color.__all__)
__all__.extend(combobox.__all__)
__all__.extend(core.__all__)
__all__.extend(dock.__all__)
__all__.extend(entriesbox.__all__)
__all__.extend(exceptions.__all__)
__all__.extend(genericbox.__all__)
__all__.extend(itemsbox.__all__)
__all__.extend(lineedit.__all__)
__all__.extend(misc.__all__)
__all__.extend(radiobutton.__all__)
__all__.extend(spinbox.__all__)
__all__.extend(style.__all__)
__all__.extend(tabbar.__all__)
__all__.extend(text.__all__)
__all__.extend(utils.__all__)

# Author declaration
__author__ = "Ellert van der Velden (@1313e)"
