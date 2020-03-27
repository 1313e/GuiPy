# -*- coding: utf-8 -*-

"""
Configuration
=============
Contains all the configuration files and functions of *GuiPy*.

"""


# %% IMPORTS
# Import core modules
from . import core, manager
from .core import *
from .manager import *
from . import base
from .base import *

# Import config pages
from . import general
from .general import *

# All declaration
__all__ = ['base', 'core', 'general', 'manager']
__all__.extend(base.__all__)
__all__.extend(core.__all__)
__all__.extend(general.__all__)
__all__.extend(manager.__all__)

# Author declaration
__author__ = "Ellert van der Velden (@1313e)"
