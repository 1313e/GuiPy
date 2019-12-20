# -*- coding: utf-8 -*-

"""
Radiobuttons
============

"""


# %% IMPORTS
# Built-in imports

# Package imports
import numpy as np
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.layouts import QW_QGridLayout, QW_QHBoxLayout, QW_QVBoxLayout
from guipy.widgets import (
    BaseBox, QW_QRadioButton, get_box_value, set_box_value)

# All declaration
__all__ = ['MultiRadioButton']


# %% CLASS DEFINITIONS
# Make class with N RadioButtons
class MultiRadioButton(BaseBox):
    """
    Defines the :class:`~MultiRadioButton` class.

    """

    # Signals
    modified = QC.Signal([], [int], [str])

    # Initialize the DualComboBox class
    def __init__(self, n=2, layout='horizontal', parent=None, *args,
                 **kwargs):
        """
        Initialize an instance of the :class:`~MultiRadioButton` class.

        Optional
        --------
        n : int or list of str. Default: 2
            The number of radiobuttons this multi-radiobutton must have.
            If list of str, the list contains the names of all radiobuttons
            that must be created.
        layout : {'horizontal'; 'vertical'} or tuple of (n_rows, n_cols). \
            Default: 'horizontal'
            The layout that this multi-radiobutton must have.
            If 'horizontal' or 'vertical', all radiobuttons will be aligned on
            a single row or column, respectively.
            If tuple, the given `n_rows` and `n_cols` determine the shape of
            the grid. If `n` is greater than `n_rows`*`n_cols`, it will be
            clipped.
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
            The parent widget to use for this multi-radiobutton or *None* for
            no parent.

        """

        # Call super constructor
        super().__init__(parent)

        # Create the dual combobox
        self.init(n, layout, *args, **kwargs)

    # Override __getitem__ to return the left and/or right combobox
    def __getitem__(self, key):
        # If key is a slice object, return everything that is requested
        if isinstance(key, slice):
            return(tuple([self[i] for i in range(*key.indices(2))]))

        # If key is an integer, return the corresponding combobox
        elif isinstance(key, int):
            # If key is zero, return left_box
            if(key == 0):
                return(self.left_box)
            # Else, if key is one, return right_box
            elif(key == 1):
                return(self.right_box)
            # Else, raise IndexError
            else:
                raise IndexError("Index out of range")

        # Else, raise TypeError
        else:
            raise TypeError("Index must be of type 'int' or 'slice', not type "
                            "%r" % (type(key).__name__))

    # This function sets up the dual combobox
    def init(self, n, layout):
        """
        Sets up the multi-radiobutton after it has been initialized.

        """

        # Check what type of n has been provided
        if isinstance(n, int):
            # If n is an integer, set all names to empty strings
            names = ['']*n
        elif hasattr(n, '__iter__'):
            # Else, n must be an iterable of names
            names = n
            n = len(n)
        else:
            raise TypeError

        # Check what type of layout has been provided
        if isinstance(layout, str):
            # If layout is a string, it is either 'horizontal' or 'vertical'
            if layout in ('h', 'horizontal', 'r', 'row'):
                layout = QW_QHBoxLayout(self)
            elif layout in ('v', 'vertical', 'c', 'col', 'column'):
                layout = QW_QVBoxLayout(self)
            else:
                raise ValueError
        else:
            # Else, layout is a tuple specifying the number of rows and columns
            n_rows, n_cols = layout
            layout = QW_QGridLayout(self)

        # Set contents margins of layout
        layout.setContentsMargins(0, 0, 0, 0)

        # Initialize empty list of radiobuttons
        self.buttons = []

        # If layout is an instance of QBoxLayout, add all buttons one-by-one
        if isinstance(layout, QW.QBoxLayout):
            # Create all requested radiobuttons
            for name in names:
                # Create radiobutton
                button = QW_QRadioButton(name)

                # Add button to list and layout
                self.buttons.append(button)
                layout.addWidget(button)

        # Else, add radiobuttons in order to the grid
        else:
            # Create all requested radiobuttons
            for name, index in zip(names, np.ndindex(n_rows, n_cols)):
                # Create radiobutton
                button = QW_QRadioButton(name)

                # Add button to list and layout
                self.buttons.append(button)
                layout.addWidget(button, *index)

    # This function is automatically called whenever 'modified' is emitted
    @QC.Slot()
    def modified_signal_slot(self):
        # Emit modified signal with proper types
        self.modified[int].emit(self.get_box_value(int))
        self.modified[str].emit(self.get_box_value(str))

    # This function retrieves a value of this special box
    def get_box_value(self, *value_sig):
        """
        Returns the index or text of the current radiobutton that is set to
        *True*.

        Returns
        -------
        value : int or str
            The index or text of the current radiobutton that is set to *True*.

        """

        # Obtain the index of the current radiobutton
        index = np.argmax(list(map(get_box_value, self.buttons)))

        # If value_sig is not int, return its value signature
        if int not in value_sig:
            return(get_box_value(self.buttons[index], *value_sig))
        # Else, return its index
        else:
            return(index)

    # This function sets the value of this special box
    def set_box_value(self, value):
        """
        Sets the radiobutton with index `value` to *True*.

        Parameters
        ----------
        value : int
            The index of the radiobutton that must be set to *True*.

        """

        set_box_value(self.buttons[value], True)
