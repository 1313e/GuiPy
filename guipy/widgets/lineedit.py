# -*- coding: utf-8 -*-

"""
LineEdits
=========

"""


# %% IMPORTS
# Package imports
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy import layouts as GL, widgets as GW
from guipy.config import CONFIG

# All declaration
__all__ = ['DualLineEdit', 'NumLineEdit']


# %% CLASS DEFINITIONS
# Make class with two line-edits
class DualLineEdit(GW.DualBaseBox):
    """
    Defines the :class:`~DualLineEdit` class.

    """

    # Signals
    modified = QC.Signal([], [int, int], [int, float], [int, str],
                         [float, int], [float, float], [float, str],
                         [str, int], [str, float], [str, str])

    # Initialize the DualLineEdit class
    def __init__(self, types=(str, str), sep=None, parent=None):
        """
        Initialize an instance of the :class:`~DualLineEdit` class.

        Optional
        --------
        types : tuple of types ({int; float; str}). Default: (str, str)
            A tuple containing the type of each line-edit.
        sep : str or None. Default: None
            The string that must be used as a separator between the two
            line-edits. If *None*, no separator is used.
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
            The parent widget to use for this dual line-edit or *None* for no
            parent.

        """

        # Call super constructor
        super().__init__(parent)

        # Create the dual line-edit
        self.init(types, sep)

    # This property returns the default 'modified' signal
    @property
    def default_modified_signal(self):
        return(self.modified.__getitem__(self.types))

    # This function creates the dual line-edit
    def init(self, types, sep):
        """
        Sets up the dual line-edit after it has been initialized.

        """

        # Make dict with different line-edits
        box_types = {
            float: lambda: NumLineEdit(float),
            int: lambda: NumLineEdit(int),
            str: GW.QLineEdit}

        # Save provided types
        self.types = types

        # Create the box_layout
        box_layout = GL.QHBoxLayout(self)
        box_layout.setContentsMargins(0, 0, 0, 0)

        # Create two line-edits with the provided types
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
            *DualLineEdit.get_box_value(self))


# Make class for setting a number in a line-edit
class NumLineEdit(GW.QLineEdit):
    # Signals
    modified = QC.Signal([float], [int])

    # Initialize the FloatLineEdit class
    def __init__(self, numtype, parent=None):
        """
        Initialize an instance of the :class:`~NumLineEdit` class.

        Parameters
        ----------
        numtype : {float; int}
            The type of number line-edit to use.

        Optional
        --------
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
            The parent widget to use for this number line-edit box or *None*
            for no parent.

        """

        # Call super constructor
        super().__init__(parent)

        # Create the number line-edit box
        self.init(numtype)

    # This property returns the default 'modified' signal
    @property
    def default_modified_signal(self):
        return(self.modified.__getitem__(self.numtype))

    # This function creates the number line-edit box
    def init(self, numtype):
        """
        Sets up the number line-edit box after it has been initialized.

        """

        # Save provided numtype
        self.numtype = numtype

        # Obtain the proper validator and value getter
        if numtype is int:
            validator = QG.QIntValidator(self)
            self.num_getter = CONFIG.locale.toInt
        else:
            validator = QG.QDoubleValidator(self)
            self.num_getter = CONFIG.locale.toDouble

        # Set the validator
        self.setValidator(validator)

        # Set initial value
        self.value = 0

    # Override focusInEvent to format text when it is triggered
    def focusInEvent(self, event):
        # Obtain a normal string version of the current number
        num = str(self.value)
        num = num.replace('.', CONFIG.locale.decimalPoint())

        # Set this as the current text
        self.setText(num)

        # Call and return super method
        return(super().focusInEvent(event))

    # Override focusOutEvent to format text when it is triggered
    def focusOutEvent(self, event):
        # Set current number in its formatted version
        self.set_box_value(self.num_getter(self.text())[0])

        # Call and return super method
        return(super().focusOutEvent(event))

    # This function calls the validator's setRange
    def setRange(self, bottom, top):
        self.validator().setRange(bottom, top)

    # This function calls the validator's setBottom
    def setBottom(self, bottom):
        self.validator().setBottom(bottom)

    # This function calls the validator's setTop
    def setTop(self, top):
        self.validator().setTop(top)

    # This function retrieves a value of this special box
    def get_box_value(self, *value_sig):
        """
        Returns the current number value of this line-edit box.

        Returns
        -------
        value : int, float
            The value contained in this line-edit bbox.

        """

        return(self.value)

    # This function sets the value of this special box
    def set_box_value(self, value, *value_sig):
        """
        Sets the current number value of this line-edit box to `value`.

        Parameters
        ----------
        value : int, float
            A value that must be set for this line-edit box.

        """

        # Save the current value
        cur_value = self.value

        # Save value
        self.value = value
        self.setText(CONFIG.locale.toString(value))

        # Emit modified signal if value was changed
        if(cur_value != self.value):
            self.default_modified_signal.emit(value)
