# -*- coding: utf-8 -*-

"""
Comboboxes
==========

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy import layouts as GL, widgets as GW

# All declaration
__all__ = ['ComboBoxValidator', 'DualComboBox', 'EditableComboBox']


# %% CLASS DEFINITIONS
# Define the ComboBoxValidator class
class ComboBoxValidator(QG.QRegularExpressionValidator):
    # Initialize the ComboBoxValidator class
    def __init__(self, combobox_obj, regexp=None, parent=None):
        """
        Initialize an instance of the :class:`~ComboBoxValidator` class.

        Parameters
        ----------
        combobox_obj : :obj:`~PyQt5.QtWidgets.ComboBox` object
            Combobox object for which the editable line must be validated.

        Optional
        --------
        regexp : str or None. Default: None
            The regular expression pattern to use for validating an input
            string if it is not found in `combobox_obj`.
            If *None*, no regular expression is used.
        parent : :obj:`~PyQt5.QtCore.QObject` object or None. Default: None
            The parent object to use for this validator or *None* for no
            parent.

        """

        # Save the completer of the provided combobox
        self.completer = combobox_obj.completer()

        # Check provided regexp
        if regexp is None:
            # If regexp is None, set the pattern to one that rejects all
            regexp = r"$.^"

        # Call super constructor
        super().__init__(QC.QRegularExpression(regexp), parent)

    # Override validate to first check the combobox completer
    def validate(self, string, pos):
        # Check if string is already in the completions list
        index = self.completer.completionModel().index(0, 0)
        match = self.completer.completionModel().match(
            index, QC.Qt.EditRole, string, flags=QC.Qt.MatchExactly)

        # Check if there is a match
        if not match:
            # If not, set the completion prefix in the completer
            self.completer.setCompletionPrefix(string)

        # Obtain the current completion string
        completion = self.completer.currentCompletion()

        # Check the completion string against the given one and act accordingly
        if completion:
            # If the completion string is not empty, check if it matches
            if match and string:
                # If so, it is acceptable
                state = self.Acceptable
            else:
                # Else, it is intermediate
                state = self.Intermediate

            # Return the state, string and pos
            return(state, string, pos)
        else:
            # If the completion string is empty, use the regular expression
            return(super().validate(string, pos))


# Make class with two comboboxes
class DualComboBox(GW.DualBaseBox):
    """
    Defines the :class:`~DualComboBox` class.

    """

    # Signals
    modified = QC.Signal([], [int, int], [int, str], [str, int],
                         [str, str])

    # Initialize the DualComboBox class
    def __init__(self, editable=(False, False), sep=None, parent=None):
        """
        Initialize an instance of the :class:`~DualComboBox` class.

        Optional
        --------
        editable : tuple of bool. Default: (False, False)
            A tuple containing the editability of each combobox.
        sep : str or None. Default: None
            The string that must be used as a separator between the two
            comboboxes. If *None*, no separator is used.
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
            The parent widget to use for this dual combobox or *None* for no
            parent.

        """

        # Call super constructor
        super().__init__(parent)

        # Create the dual combobox
        self.init(editable, sep)

    # This property returns the default 'modified' signal
    @property
    def default_modified_signal(self):
        return(self.modified[str, str])

    # This function sets up the dual combobox
    def init(self, editable, sep):
        """
        Sets up the dual combobox after it has been initialized.

        """

        # Create the box_layout
        box_layout = GL.QHBoxLayout(self)
        box_layout.setContentsMargins(0, 0, 0, 0)

        # Create two comboboxes with the provided editability
        # LEFT
        left_box = EditableComboBox() if editable[0] else GW.QComboBox()
        box_layout.addWidget(left_box)
        self.left_box = left_box

        # RIGHT
        right_box = EditableComboBox() if editable[1] else GW.QComboBox()
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
        for types in [(int, int), (int, str), (str, int), (str, str)]:
            self.modified[types[0], types[1]].emit(
                *DualComboBox.get_box_value(self, *types))


# Create custom QComboBox class that is editable
class EditableComboBox(GW.QComboBox):
    """
    Defines the :class:`~QEditableComboBox` class.

    This class makes the :class:`~guipy.widgets.QComboBox` class editable.

    """

    # Create focusLost signal
    focusLost = QC.Signal([int], [str])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setEditable(True)
        self.setInsertPolicy(self.NoInsert)
        self.completer().setCompletionMode(QW.QCompleter.PopupCompletion)
        self.completer().setFilterMode(QC.Qt.MatchContains)

    # Override focusOutEvent to emit signal whenever triggered
    def focusOutEvent(self, event):
        # Emit focusLost signal
        self.focusLost[int].emit(self.currentIndex())
        self.focusLost[str].emit(self.currentText())

        # Call super method
        return(super().focusOutEvent(event))
