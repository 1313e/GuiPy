# -*- coding: utf-8 -*-

"""
Comboboxes
==========

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.widgets import QW_QComboBox

# All declaration
__all__ = ['EditableComboBox']


# %% CLASS DEFINITIONS
# Create custom QComboBox class that is editable
class EditableComboBox(QW_QComboBox):
    """
    Defines the :class:`~QW_QEditableComboBox` class.

    This class makes the :class:`~guipy.widgets.QW_QComboBox` class editable.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setEditable(True)
        self.setInsertPolicy(self.NoInsert)
        self.completer().setCompletionMode(QW.QCompleter.PopupCompletion)
        self.completer().setFilterMode(QC.Qt.MatchContains)
