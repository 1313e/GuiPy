# -*- coding: utf-8 -*-

"""
Miscellaneous
=============

"""


# %% IMPORTS
# Built-in imports

# Package imports

# GuiPy imports
from guipy import widgets as GW

# All declaration
__all__ = ['type_box_dict']


# %% INSTANCES
# Make a look-up dict for types
type_box_dict = {
    bool: GW.QCheckBox,
    float: GW.FloatLineEdit,
    int: GW.IntLineEdit,
    str: GW.QLineEdit,
    dict: GW.EditableEntriesBox,
    list: GW.GenericItemsBox}
