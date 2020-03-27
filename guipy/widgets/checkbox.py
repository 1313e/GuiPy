# -*- coding: utf-8 -*-

"""
Checkboxes
==========

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy import INT_TYPES
from guipy import layouts as GL, widgets as GW
from guipy.widgets import get_box_value, get_modified_box_signal, set_box_value

# All declaration
__all__ = ['ToggleBox']


# %% CLASS DEFINITIONS
# Make class that toggles a widget
class ToggleBox(GW.BaseBox):
    """
    Defines the :class:`~ToggleBox` class.

    This widget allows for a provided widget to be toggled on and off.

    """

    # Signals
    modified = QC.Signal([], [bool])

    # Initialize the ToggleBox class
    def __init__(self, widget, text=None, tooltip=None, parent=None, *args,
                 **kwargs):
        """
        Initialize an instance of the :class:`~ToggleBox` class.

        Parameters
        ----------
        widget : :obj:`~PyQt5.QtWidgets.QWidget` object
            The widget that must be made toggleable.

        Optional
        --------
        text : str or None. Default: None
            The text that must be used for the checkbox.
            If *None*, the checkbox has no text.
        tooltip : str or None. Default: None
            The text that must be set as the tooltip of the checkbox.
            If *None*, the checkbox has no tooltip.
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
            The parent widget to use for this togglebox or *None* for no
            parent.

        """

        # Call super constructor
        super().__init__(parent)

        # Create the togglebox
        self.init(widget, text, tooltip, *args, **kwargs)

    # Override __getitem__ to return the left and/or right widget
    def __getitem__(self, key):
        # If key is an integer, return the corresponding widget
        if isinstance(key, INT_TYPES):
            # If key is 0 or -2, return checkbox
            if key in (0, -2):
                return(self.checkbox)
            # Else, if key is 1 or -1, return widget
            elif key in (1, -1):
                return(self.widget)
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

    # This function sets up the togglebox
    def init(self, widget, text, tooltip):
        """
        Sets up the togglebox after it has been initialized.

        """

        # Create the box_layout
        box_layout = GL.QHBoxLayout(self)
        box_layout.setContentsMargins(0, 0, 0, 0)

        # Create a checkbox for toggling the widget
        if text is not None:
            checkbox = GW.QCheckBox(text)
        else:
            checkbox = GW.QCheckBox()
        box_layout.addWidget(checkbox)
        self.checkbox = checkbox

        # Set tooltip
        if tooltip is not None:
            checkbox.setToolTip(tooltip)

        # Add the widget to it
        box_layout.addWidget(widget)
        self.widget = widget

        # Connect some signals
        get_modified_box_signal(checkbox).connect(widget.setEnabled)

        # Make sure that the checkbox is unchecked
        set_box_value(checkbox, False)
        widget.setEnabled(False)

    # This function is automatically called whenever 'modified' is emitted
    @QC.Slot()
    def modified_signal_slot(self):
        # Emit modified signal with proper types
        self.modified[bool].emit(get_box_value(self.checkbox))

    # This function retrieves a value of this special box
    def get_box_value(self, *value_sig):
        """
        Returns the current values of this togglebox as a tuple.

        Returns
        -------
        value : tuple
            A tuple containing the values of the checkbox and widget, formatted
            as `(checkbox, widget)`.

        """
        return(get_box_value(self.checkbox),
               get_box_value(self.widget, *value_sig))

    # This function sets the value of this special box
    def set_box_value(self, value, *args, **kwargs):
        """
        Sets the current value of the togglebox to `value`.

        Parameters
        ----------
        value : tuple
            A tuple containing the values of the checkbox and widget, formatted
            as `(checkbox, widget)`.

        """

        set_box_value(self.checkbox, value[0])
        set_box_value(self.widget, value[1], *args, **kwargs)
