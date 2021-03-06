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
from guipy import layouts as GL, widgets as GW
from guipy.widgets import get_box_value, get_modified_signal, set_box_value

# All declaration
__all__ = ['ToggleBox']


# %% CLASS DEFINITIONS
# Make class that toggles a widget
class ToggleBox(GW.DualBaseBox):
    """
    Defines the :class:`~ToggleBox` class.

    This widget allows for a provided widget to be toggled on and off.

    """

    # Signals
    modified = QC.Signal([], [bool])

    # Initialize the ToggleBox class
    def __init__(self, widget, text=None, tooltip=None, parent=None):
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
        self.init(widget, text, tooltip)

    # This property returns the default 'modified' signal
    @property
    def default_modified_signal(self):
        return(self.modified[bool])

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
        self.left_box = checkbox

        # Set tooltip
        if tooltip is not None:
            checkbox.setToolTip(tooltip)

        # Add the widget to it
        box_layout.addWidget(widget)
        self.widget = widget
        self.right_box = widget

        # Connect some signals
        get_modified_signal(checkbox).connect(widget.setEnabled)

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
        value : bool or tuple
            A tuple containing the values of the checkbox and widget, formatted
            as `(checkbox, widget)`.
            If `value_sig` contains type 'bool', only the value of `checkbox`
            is returned.

        """

        # If solely the value of the checkbox was requested, return it
        if bool in value_sig:
            return(get_box_value(self.checkbox))
        # Else, return the checkbox and widget values
        else:
            return(get_box_value(self.checkbox),
                   get_box_value(self.widget, *value_sig))

    # This function sets the value of this special box
    def set_box_value(self, value, *value_sig):
        """
        Sets the current value of the togglebox to `value`.

        Parameters
        ----------
        value : tuple
            A tuple containing the values of the checkbox and widget, formatted
            as `(checkbox, widget)`.

        """

        set_box_value(self.checkbox, value[0])
        set_box_value(self.widget, value[1], *value_sig)
