# -*- coding: utf-8 -*-

"""
Configuration
=============
Contains all the configuration files and functions of *GuiPy*.

"""


# %% IMPORTS
# Import core modules
from . import core
from .core import *
from . import base, manager
from .base import *
from .manager import *

# All declaration
__all__ = ['base', 'core', 'manager']
__all__.extend(base.__all__)
__all__.extend(core.__all__)
__all__.extend(manager.__all__)

# Author declaration
__author__ = "Ellert van der Velden (@1313e)"
