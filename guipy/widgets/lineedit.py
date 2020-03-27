# -*- coding: utf-8 -*-

"""
LineEdits
=========

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy import widgets as GW
from guipy.config import CONFIG
from guipy.widgets import get_box_value, set_box_value

# All declaration
__all__ = ['IntLineEdit']


# %% CLASS DEFINITIONS
# Make class for setting an integer in a lineedit
class IntLineEdit(GW.QLineEdit):
    """
    Defines the :class:`~IntLineEdit` class.

    """

    # Initialize the IntLineEdit class
    def __init__(self, parent=None, *args, **kwargs):
        """
        Initialize an instance of the :class:`~IntLineEdit` class.

        Optional
        --------
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
            The parent widget to use for this integer lineedit box or *None*
            for no parent.

        """

        # Call super constructor
        super().__init__(parent)

        # Create the integer lineedit box
        self.init(*args, **kwargs)

    # This function creates the figure label box
    def init(self):
        """
        Sets up the figure label box after it has been initialized.

        """

        # Initialize the validator
        validator = QG.QIntValidator(self)
        self.setValidator(validator)

    # This function retrieves a value of this special box
    def get_box_value(self, *args, **kwargs):
        """
        Returns the current values of this figure label box as a tuple.

        Returns
        -------
        value : tuple
            A tuple containing the values of the figure label box, formatted as
            `(label, {'fontsize': size})`.

        """

        return(CONFIG.locale.toInt(get_box_value(self, *args, **kwargs)))

    # This function sets the value of this special box
    def set_box_value(self, value, *args, **kwargs):
        """
        Sets the current value of the figure label box to `value`.

        Parameters
        ----------
        value : tuple
            A tuple containing the values of the figure label box, formatted as
            `(label, {'fontsize': size})`.

        """

        set_box_value(self, CONFIG.locale.toString(value, *args, **kwargs))
