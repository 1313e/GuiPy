# -*- coding: utf-8 -*-

"""
Spinboxes
=========

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy import INT_TYPES
from guipy import layouts as GL, widgets as GW
from guipy.widgets import get_box_value, set_box_value

# All declaration
__all__ = ['DualSpinBox']


# %% CLASS DEFINITIONS
# Make class with two spinboxes
class DualSpinBox(GW.BaseBox):
    """
    Defines the :class:`~DualSpinBox` class.

    """

    # Signals
    modified = QC.Signal([], [int, int], [int, float], [float, int],
                         [float, float])

    # Initialize the DualSpinBox class
    def __init__(self, types=(int, int), sep=None, parent=None, *args,
                 **kwargs):
        """
        Initialize an instance of the :class:`~DualSpinBox` class.

        Optional
        --------
        types : tuple of types ({int; float}). Default: (int, int)
            A tuple containing the type of each spinbox.
        sep : str or None. Default: None
            The string that must be used as a separator between the two
            spinboxes. If *None*, no separator is used.
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
            The parent widget to use for this dual spinbox or *None* for no
            parent.

        """

        # Call super constructor
        super().__init__(parent)

        # Create the dual spinbox
        self.init(types, sep, *args, **kwargs)

    # Override __getitem__ to return the left and/or right spinbox
    def __getitem__(self, key):
        # If key is an integer, return the corresponding spinbox
        if isinstance(key, INT_TYPES):
            # If key is 0 or -2, return left_box
            if key in (0, -2):
                return(self.left_box)
            # Else, if key is 1 or -1, return right_box
            elif key in (1, -1):
                return(self.right_box)
            # Else, raise IndexError
            else:
                raise IndexError("Index out of range")

        # If key is a slice object, return everything that is requested
        elif isinstance(key, slice):
            return(*map(self.__getitem__, range(*key.indices(2))),)

        # Else, raise TypeError
        else:
            raise TypeError("Index must be of type 'int' or 'slice', not type "
                            "%r" % (type(key).__name__))

    # This function creates the dual spinbox
    def init(self, types, sep):
        """
        Sets up the dual spinbox after it has been initialized.

        """

        # Save provided types
        self.types = types

        # Create the box_layout
        box_layout = GL.QHBoxLayout(self)
        box_layout.setContentsMargins(0, 0, 0, 0)

        # Create two spinboxes with the provided types
        # LEFT
        left_box = GW.QSpinBox() if types[0] is int else GW.QDoubleSpinBox()
        box_layout.addWidget(left_box)
        self.left_box = left_box

        # RIGHT
        right_box = GW.QSpinBox() if types[1] is int else GW.QDoubleSpinBox()
        box_layout.addWidget(right_box)
        self.right_box = right_box

        # If sep is not None, create label and add it
        if sep is not None:
            sep_label = GW.QLabel(sep)
            sep_label.setSizePolicy(QW.QSizePolicy.Fixed, QW.QSizePolicy.Fixed)
            box_layout.insertWidget(1, sep_label)

    # This function is automatically called whenever 'modified' is emitted
    @QC.Slot()
    def modified_signal_slot(self):
        # Emit modified signal with proper types
        self.modified[self.types[0], self.types[1]].emit(
            *DualSpinBox.get_box_value(self))

    # This function retrieves a value of this special box
    def get_box_value(self, *args, **kwargs):
        """
        Returns the current values of this dual spinbox as a tuple.

        Returns
        -------
        value : tuple
            A tuple containing the values of the spinboxes, formatted as
            `(left, right)`.

        """

        return(get_box_value(self.left_box, *args, **kwargs),
               get_box_value(self.right_box, *args, **kwargs))

    # This function sets the value of this special box
    def set_box_value(self, value, *args, **kwargs):
        """
        Sets the current value of the dual spinbox to `value`.

        Parameters
        ----------
        value : tuple
            A tuple containing the values of the spinboxes, formatted as
            `(left, right)`.

        """

        set_box_value(self.left_box, value[0], *args, **kwargs)
        set_box_value(self.right_box, value[1], *args, **kwargs)
