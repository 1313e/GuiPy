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
class DualSpinBox(GW.DualBaseBox):
    """
    Defines the :class:`~DualSpinBox` class.

    """

    # Signals
    modified = QC.Signal([], [int, int], [int, float], [float, int],
                         [float, float])

    # Initialize the DualSpinBox class
    def __init__(self, types=(int, int), sep=None, parent=None):
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
        self.init(types, sep)

    # This property returns the default 'modified' signal
    @property
    def default_modified_signal(self):
        return(self.modified.__getitem__(self.types))

    # This function creates the dual spinbox
    def init(self, types, sep):
        """
        Sets up the dual spinbox after it has been initialized.

        """

        # Make dict with different line-edits
        box_types = {
            float: GW.QDoubleSpinBox,
            int: GW.QSpinBox}

        # Save provided types
        self.types = types

        # Create the box_layout
        box_layout = GL.QHBoxLayout(self)
        box_layout.setContentsMargins(0, 0, 0, 0)

        # Create two spinboxes with the provided types
        # LEFT
        left_box = box_types[types[0]]()
        box_layout.addWidget(left_box)
        self.left_box = left_box

        # RIGHT
        right_box = box_types[types[1]]()
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
