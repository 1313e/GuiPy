# -*- coding: utf-8 -*-

"""
Text
====
Provides a collection of :class:`~PyQt5.QtWidgets.QWidget` subclasses for
handling text and labels in :mod:`~matplotlib`.

"""


# %% IMPORTS
# Built-in imports

# Package imports
from matplotlib import rcParams
from matplotlib.font_manager import font_scalings
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy import layouts as GL, widgets as GW
from guipy.widgets import get_box_value, set_box_value

# All declaration
__all__ = ['FigureLabelBox']


# %% CLASS DEFINITIONS
# Make class for setting the label in a figure
class FigureLabelBox(GW.DualBaseBox):
    """
    Defines the :class:`~FigureLabelBox` class.

    """

    # Signals
    modified = QC.Signal([], [str], [str, dict])

    # Initialize the FigureLabelBox class
    def __init__(self, parent=None):
        """
        Initialize an instance of the :class:`~FigureLabelBox` class.

        Optional
        --------
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
            The parent widget to use for this figure label box or *None* for no
            parent.

        """

        # Call super constructor
        super().__init__(parent)

        # Create the figure label box
        self.init()

    # This property returns the default 'modified' signal
    @property
    def default_modified_signal(self):
        return(self.modified[str])

    # This function creates the figure label box
    def init(self):
        """
        Sets up the figure label box after it has been initialized.

        """

        # Create the box_layout
        box_layout = GL.QHBoxLayout(self)
        box_layout.setContentsMargins(0, 0, 0, 0)

        # Create a line-edit for setting the label
        label_box = GW.QLineEdit()
        box_layout.addWidget(label_box)
        self.left_box = label_box

        # Create a spinbox for setting the fontsize
        size_box = GW.QDoubleSpinBox()
        size_box.setDecimals(1)
        size_box.setRange(0, 999)
        size_box.setSuffix(" pts")
        box_layout.addWidget(size_box)
        self.right_box = size_box

    # This function is automatically called whenever 'modified' is emitted
    @QC.Slot()
    def modified_signal_slot(self):
        # Emit modified signals
        self.modified[str].emit(get_box_value(self.left_box))
        self.modified[str, dict].emit(*self.get_box_value())

    # This function retrieves a value of this special box
    def get_box_value(self, *value_sig):
        """
        Returns the current values of this figure label box as a tuple.

        Returns
        -------
        value : tuple
            A tuple containing the values of the figure label box, formatted as
            `(label, {'fontsize': size})`.

        """

        return(get_box_value(self.left_box),
               {'fontsize': get_box_value(self.right_box)})

    # This function sets the value of this special box
    def set_box_value(self, value, *value_sig):
        """
        Sets the current value of the figure label box to `value`.

        Parameters
        ----------
        value : tuple
            A tuple containing the values of the figure label box, formatted as
            `(label, {'fontsize': size})`.

        """

        # Set box value of label
        set_box_value(self.left_box, value[0])

        # Obtain fontsize
        fontsize = value[1]['fontsize']

        # If fontsize is a string, it is a font scaling keyword
        if isinstance(fontsize, str):
            # Obtain actual float fontsize
            fontsize = rcParams['font.size']*font_scalings[fontsize]

        # Set box value of fontsize
        set_box_value(self.right_box, fontsize)
