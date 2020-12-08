# -*- coding: utf-8 -*-

"""
GenericBoxes
============

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy import layouts as GL, widgets as GW
from guipy.widgets import get_box_value, get_modified_signal, set_box_value

# All declaration
__all__ = ['GenericBox', 'LongGenericBox']


# %% CLASS DEFINITIONS
# Define class for creating generic value boxes
class GenericBox(GW.BaseBox):
    """
    Defines the :class:`~GenericBox` class.

    This class is used for making a generic value box that only accepts single
    values, unlike :class:`~LongGenericBox`.
    It currently supports inputs of type bool; float; int; and str.

    """

    # Signals
    modified = QC.Signal([], [object])

    # Initialize the GenericBox class
    def __init__(self, parent=None):
        """
        Initialize an instance of the :class:`~GenericBox` class.

        """

        # Call super constructor
        super().__init__(parent)

        # Create the generic box
        self.init()

    # This property returns the default 'modified' signal
    @property
    def default_modified_signal(self):
        return(self.modified[object])

    # This property returns the types that this box supports
    @property
    def supported_types(self):
        return([bool, float, int, str])

    # This function creates the generic box
    def init(self):
        """
        Sets up the generic value box after it has been initialized.

        """

        # Create the box_layout
        box_layout = GL.QHBoxLayout(self)
        box_layout.setContentsMargins(0, 0, 0, 0)
        self.box_layout = box_layout

        # Create a combobox for the type
        type_box = GW.QComboBox()
        type_box.addItems(sorted([x.__name__ for x in self.supported_types]))
        type_box.setSizePolicy(QW.QSizePolicy.Fixed, QW.QSizePolicy.Fixed)
        set_box_value(type_box, -1)
        get_modified_signal(type_box).connect(self.create_value_box)
        box_layout.addWidget(type_box)
        self.type_box = type_box

        # Create a default value box
        value_box = GW.QWidget()
        box_layout.addWidget(value_box)
        self.value_box = value_box

    # This function is automatically called whenever 'modified' is emitted
    @QC.Slot()
    def modified_signal_slot(self):
        # Emit modified signal
        self.modified[object].emit(get_box_value(self.value_box))

    # This function creates a value_box depending on the type that was selected
    @QC.Slot(str)
    def create_value_box(self, value_type):
        """
        Creates a value box for the provided type `value_type` and replaces the
        current value box with it.

        Parameters
        ----------
        value_type : {'bool'; 'float'; 'int'; 'str'}
            The string of the type of value box that is requested.

        """

        # Create a widget box for the specified value_type
        value_box = GW.type_box_dict[eval(value_type)]()
        value_box.setSizePolicy(QW.QSizePolicy.Expanding, QW.QSizePolicy.Fixed)

        # Set this value_box in the layout
        cur_item = self.box_layout.replaceWidget(self.value_box, value_box)
        cur_item.widget().close()
        del cur_item

        # Save new value_box
        self.value_box = value_box

    # This function retrieves a value of this special box
    def get_box_value(self, *value_sig):
        """
        Returns the current value of the value box.

        Returns
        -------
        value : bool, float, int or str
            The current value of this generic value box.

        """

        # If value_box is currently a QWidget, return None
        if type(self.value_box) is GW.QWidget:
            return(None)
        # Else, return its actual value
        else:
            return(get_box_value(self.value_box, *value_sig))

    # This function sets the value of this special box
    def set_box_value(self, value, *value_sig):
        """
        Sets the value type to `type(value)` and the value to `value`.

        Parameters
        ----------
        value : bool, float, int or str
            The value to use for this generic value box. The type of `value`
            determines which value box must be used.

        """

        set_box_value(self.type_box, type(value).__name__)
        set_box_value(self.value_box, value, *value_sig)


# Define class for creating generic value boxes that supports all types
class LongGenericBox(GenericBox):
    """
    Defines the :class:`~LongGenericBox` class.

    This class is used for making a generic value box that also accepts
    iterables, unlike :class:`~GenericBox`.
    It currently supports inputs of all types found in :obj:`~type_box_dict`.

    """

    # This property returns the types that this box supports
    @property
    def supported_types(self):
        return(GW.type_box_dict.keys())
