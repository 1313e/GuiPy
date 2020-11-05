# -*- coding: utf-8 -*-

"""
Radiobuttons
============

"""


# %% IMPORTS
# Built-in imports
from itertools import repeat

# Package imports
import numpy as np
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy import INT_TYPES, STR_TYPES
from guipy import layouts as GL, widgets as GW
from guipy.widgets import get_box_value, set_box_value

# All declaration
__all__ = ['MultiRadioButton']


# %% CLASS DEFINITIONS
# Make class with N RadioButtons
class MultiRadioButton(GW.BaseBox):
    """
    Defines the :class:`~MultiRadioButton` class.

    """

    # Signals
    modified = QC.Signal([], [int], [str])

    # Initialize the MultiRadioButton class
    def __init__(self, n=2, layout='horizontal', parent=None):
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

        # Create the multi-radiobutton
        self.init(n, layout)

    # Override __getitem__ to return the requested radiobutton(s)
    def __getitem__(self, key):
        # If key is an integer, return the corresponding radiobutton
        if isinstance(key, INT_TYPES):
            # Try to return the requested radiobutton
            try:
                return(self.buttons[key])
            # If that cannot be done, raise IndexError
            except IndexError:
                raise IndexError("Index out of range")

        # If key is a slice object, return everything that is requested
        elif isinstance(key, slice):
            return(*map(self.__getitem__, range(*key.indices(self.N))),)

        # If key is a string, try to return the corresponding radiobutton
        elif isinstance(key, STR_TYPES):
            # Count how many times the requested name appears
            n_hits = self.names.count(key)

            # Check if this name exists
            if n_hits:
                # If so, check if it appears exactly once
                if(n_hits == 1):
                    # If so as well, return the corresponding radiobutton
                    return(self[self.names.index(key)])
                else:
                    # If not, raise error
                    raise KeyError("Key %r is not unique" % (key))
            else:
                # If name does not exist, raise error
                raise KeyError("Key %r not found" % (key))

        # Else, raise TypeError
        else:
            raise TypeError("Index must be of type 'int'; 'slice' or 'str', "
                            "not type %r" % (type(key).__name__))

    # This property returns the default 'modified' signal
    @property
    def default_modified_signal(self):
        return(self.modified[str])

    # This function sets up the multi-radiobutton
    def init(self, n, layout):
        """
        Sets up the multi-radiobutton after it has been initialized.

        """

        # Check what type of n has been provided
        if isinstance(n, INT_TYPES):
            # If n is an integer, set all names to empty strings
            names = ['']*n
        elif hasattr(n, '__iter__') and not isinstance(n, STR_TYPES):
            # Else, n must be an iterable of names
            names = list(map(str, n))
            n = len(n)
        else:
            raise TypeError

        # Check what type of layout has been provided
        if isinstance(layout, STR_TYPES):
            # If layout is a string, it is either 'horizontal' or 'vertical'
            if layout in ('h', 'horizontal', 'r', 'row'):
                layout = GL.QHBoxLayout(self)
            elif layout in ('v', 'vertical', 'c', 'col', 'column'):
                layout = GL.QVBoxLayout(self)
            else:
                raise ValueError
        else:
            # Else, layout is a tuple specifying the number of rows and columns
            n_rows, n_cols = layout
            layout = GL.QGridLayout(self)

        # Set contents margins of layout
        layout.setContentsMargins(0, 0, 0, 0)

        # Initialize empty list of radiobuttons
        self.buttons = []

        # Create buttons iterator
        if isinstance(layout, QW.QGridLayout):
            iterator = zip(names, np.ndindex(n_rows, n_cols))
        else:
            iterator = zip(names, repeat(()))

        # Create all requested radiobuttons
        for item in iterator:
            # Create radiobutton
            button = GW.QRadioButton(item[0])

            # Add button to list and layout
            self.buttons.append(button)
            layout.addWidget(button, *item[1])

        # Save the number of radiobuttons
        self.N = len(self.buttons)

        # Save the names
        self.names = names[:self.N]

    # This function is automatically called whenever 'modified' is emitted
    @QC.Slot()
    def modified_signal_slot(self):
        # Emit modified signal with proper types
        self.modified[int].emit(MultiRadioButton.get_box_value(self, int))
        self.modified[str].emit(MultiRadioButton.get_box_value(self, str))

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

        # If value_sig is not int, return its text
        if int not in value_sig:
            return(get_box_value(self[index], str))
        # Else, return its index
        else:
            return(index)

    # This function sets the value of this special box
    def set_box_value(self, value, *value_sig):
        """
        Sets the radiobutton with index `value` to *True*.

        Parameters
        ----------
        value : int
            The index of the radiobutton that must be set to *True*.

        """

        set_box_value(self[value], True)
