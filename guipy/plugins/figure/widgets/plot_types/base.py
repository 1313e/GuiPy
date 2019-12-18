# -*- coding: utf-8 -*-

"""
Base Plot Types
===============

"""


# %% IMPORTS
# Built-in imports
import abc


# All declaration
__all__ = ['BasePlotType']


# %% CLASS DEFINITIONS
# Define BasePlotType abstract base class
class BasePlotType(object, metaclass=abc.ABCMeta):
    """
    Provides an abstract base class definition that must be subclassed by all
    figure plot types.

    """

    pass
