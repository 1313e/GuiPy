# -*- coding: utf-8 -*-

"""
GuiPy
=====
An easy plotting GUI for Python.

"""


# %% IMPORTS AND DECLARATIONS
# Import globals
from ._globals import *

# Import base modules and definitions
from .__version__ import __version__
from .config import CONFIG

# Import subpackages
from . import app, config, layouts, plugins, widgets

# All declaration
__all__ = ['CONFIG', 'app', 'config', 'layouts', 'plugins', 'widgets']

# Author declaration
__author__ = "Ellert van der Velden (@1313e)"
