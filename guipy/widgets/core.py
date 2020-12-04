# -*- coding: utf-8 -*-

"""
Widgets Core
============
Provides a collection of utility functions and the :class:`~BaseBox` class
definition, which are core to the functioning of all widgets.

"""


# %% IMPORTS
# Built-in import
from inspect import isclass

# Package imports
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy import FLOAT_TYPES, INT_TYPES, STR_TYPES
from guipy.widgets.base import (
    QLabel as GW_QLabel, QTabWidget as GW_QTabWidget, QWidget as GW_QWidget)

# All declaration
__all__ = ['BaseBox', 'DualBaseBox', 'get_box_value', 'get_modified_signal',
           'set_box_value']


# %% CLASS DEFINITIONS
# Make base class for custom boxes
# As QW.QWidget is a strict class (in C++), this cannot be an ABC
class BaseBox(GW_QWidget):
    """
    Defines the :class:`~BaseBox` base class.

    This class is used by many custom :class:`~PyQt5.QtWidgets.QWidget` classes
    as their base. It defines the :attr:`~modified` signal, which is
    automatically connected to any widget that changes its state, unless
    `auto_connect` is set set *False*.

    """

    # Define modified signal
    modified = QC.Signal()

    # Initialize the BaseBox class
    def __init__(self, *args, auto_connect=True, **kwargs):
        # Call super constructor
        super().__init__(*args, **kwargs)

        # Store auto_connect
        self.auto_connect = auto_connect

        # If the 'modified_signal_slot' slot is available, connect it
        if hasattr(self, 'modified_signal_slot'):
            self.modified.connect(self.modified_signal_slot)

    # Override childEvent to connect signals if child has a modified signal
    def childEvent(self, event):
        """
        Special :meth:`~PyQt5.QtCore.QObject.childEvent` event that
        automatically connects the default modified signal of any widget that
        becomes a child of this widget.

        """

        # If this event involved a child being added, check child object
        if self.auto_connect and (event.type() == QC.QEvent.ChildAdded):
            # Obtain child object
            child = event.child()

            # Try to obtain the modified signal of this child
            try:
                signal = get_modified_signal(child)
            # If this fails, it does not have one
            except NotImplementedError:
                pass
            # If this succeeds, connect it to the 'modified' signal
            else:
                signal.connect(self.modified[()])

        # Call and return super method
        return(super().childEvent(event))

    # This function connects a given box to the modified signal
    def connect_box(self, box):
        """
        Connect the default modified signal of the provided `box` to this
        widget's :attr:`~modified` signal.

        """

        # Check if the given box is a child of this box and skip if so
        if box in self.children():
            return

        # Obtain the modified signal of the given box
        signal = get_modified_signal(box)

        # Connect the signals
        signal.connect(self.modified[()])

    # Define get_box_value method
    def get_box_value(self, *value_sig):
        """
        Obtain the value of this widget and return it.

        """

        raise NotImplementedError(self.__class__)

    # Define set_box_value method
    def set_box_value(self, value, *value_sig):
        """
        Set the value of this widget to `value`.

        """

        raise NotImplementedError(self.__class__)


# Define DualBaseBox class for making dual widgets
class DualBaseBox(BaseBox):
    # Override __getitem__ to return the left and/or right widget
    def __getitem__(self, key):
        # If key is an integer, return the corresponding widget
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

    # This function retrieves a value of this special box
    def get_box_value(self, *value_sig):
        """
        Returns the current values of this dual widget as a tuple.

        Returns
        -------
        value : tuple
            A tuple containing the values of the widgets, formatted as
            `(left, right)`.

        """

        # Get values of both widgets
        if(len(value_sig) == 2):
            # If value_sig contains exactly 2 elements, use them separately
            left_sig, right_sig = value_sig

            # Make sure that left_sig and right_sig are iterables to unpack
            if not isinstance(left_sig, (list, tuple, set)):
                left_sig = (left_sig,)
            if not isinstance(right_sig, (list, tuple, set)):
                right_sig = (right_sig,)

            # Get values
            return(get_box_value(self.left_box, *left_sig),
                   get_box_value(self.right_box, *right_sig))
        else:
            # Else, use value_sig for both
            return(get_box_value(self.left_box, *value_sig),
                   get_box_value(self.right_box, *value_sig))

    # This function sets the value of this special box
    def set_box_value(self, value, *value_sig):
        """
        Sets the current value of the dual widget to `value`.

        Parameters
        ----------
        value : tuple
            A tuple containing the values of the widgets, formatted as
            `(left, right)`.

        """

        # Set values of both widgets
        if(len(value_sig) == 2):
            # If value_sig contains exactly 2 elements, use them separately
            left_sig, right_sig = value_sig

            # Make sure that left_sig and right_sig are iterables to unpack
            if not isinstance(left_sig, (list, tuple, set)):
                left_sig = (left_sig,)
            if not isinstance(right_sig, (list, tuple, set)):
                right_sig = (right_sig,)

            # Set values
            set_box_value(self.left_box, *left_sig)
            set_box_value(self.right_box, *right_sig)
        else:
            # Else, use value_sig for both
            set_box_value(self.left_box, value[0], *value_sig)
            set_box_value(self.right_box, value[1], *value_sig)

    # Override closeEvent to make sure both widgets are deleted when closed
    def closeEvent(self, event):
        # Close both widgets
        self.left_box.close()
        self.right_box.close()

        # Call super method
        return(super().closeEvent(event))


# %% FUNCTION DEFINITIONS
# This function gets the value of a provided box
def get_box_value(box, *value_sig):
    """
    Retrieves the value of the provided widget `box` and returns it.

    If `box` has the `get_box_value()` method defined (always the case for
    instances of :class:`~BaseBox`), it will be used instead. If this raises a
    :class:`~NotImplementedError`, the method is skipped.

    Parameters
    ----------
    box : :obj:`~PyQt5.QtWidgets.QWidget` object
        The widget whose value must be returned.
    value_sig : positional arguments of object
        The signature of the value of `box` that must be returned.
        If empty or invalid, the default value is returned.
        If `box` has the `get_box_value()` method defined, this argument is
        passed to it.

    Returns
    -------
    box_value : obj
        The value of the requested `box`.

    """

    # Custom boxes (get_box_value()-method)
    if hasattr(box, 'get_box_value'):
        # Try to use the custom get_box_value()-method
        try:
            return(box.get_box_value(*value_sig))
        # If that fails, proceed to use a normal function
        except NotImplementedError:
            pass

    # Values (QAbstractSpinBox)
    if isinstance(box, QW.QAbstractSpinBox):
        return(box.value())

    # Actions, Bools/Buttons (QAction, QAbstractButton)
    elif isinstance(box, (QW.QAction, QW.QAbstractButton)):
        if box.isCheckable() and str not in value_sig:
            return(box.isChecked())
        else:
            return(box.text())

    # Items (QComboBox)
    elif isinstance(box, QW.QComboBox):
        return(box.currentIndex() if int in value_sig else box.currentText())

    # Tabs (QTabWidget)
    elif isinstance(box, QW.QTabWidget):
        if int in value_sig:
            return(box.currentIndex())
        elif str in value_sig:
            return(box.tabText(box.currentIndex()))
        else:
            return(box.currentWidget())

    # Strings (QLineEdit)
    elif isinstance(box, QW.QLineEdit):
        return(box.text())

    # Labels (QLabel)
    elif isinstance(box, QW.QLabel):
        for attr in ['movie', 'picture', 'pixmap']:
            if getattr(box, attr)() is not None:
                return(getattr(box, attr)())
        else:
            return(box.text())

    # If none applies, raise error
    else:
        raise NotImplementedError("Custom boxes must provide their own "
                                  "'get_box_value()'-method! (%s)"
                                  % (box.__class__))


# This function gets the emitted signal when a provided box is modified
def get_modified_signal(box, *signal_sig):
    """
    Retrieves a signal of the provided widget `box` that indicates that `box`
    has been modified and returns it.

    If `box` has the `default_modified_signal` attribute defined, it will be
    returned if `signal_sig` is empty.
    If `box` has the `modified` signal defined (always the case for instances
    of :class:`~BaseBox`), it will be returned instead.

    Parameters
    ----------
    box : :obj:`~PyQt5.QtWidgets.QWidget` object
        The widget whose modified signal must be retrieved.
    signal_sig : positional arguments of object
        The signature of the modified signal that is requested.
        If empty or invalid, the default modified signal is returned.

    Returns
    -------
    modified_signal : :obj:`~PyQt5.QtCore.pyqtBoundSignal` object
        The requested modified signal of `box`.

    """

    # Custom boxes (default_modified_signal attribute)
    if hasattr(box, 'default_modified_signal') and not signal_sig:
        return(box.default_modified_signal)

    # Custom boxes (modified signal)
    elif hasattr(box, 'modified'):
        return(box.modified.__getitem__(signal_sig))

    # Values (QAbstractSpinBox)
    elif isinstance(box, QW.QAbstractSpinBox):
        return(box.valueChanged)

    # Actions (QAction)
    elif isinstance(box, QW.QAction):
        return(box.toggled if box.isCheckable() else box.triggered)

    # Bools/Buttons (QAbstractButton)
    elif isinstance(box, QW.QAbstractButton):
        return(box.toggled if box.isCheckable() else box.clicked)

    # Items (QComboBox)
    elif isinstance(box, QW.QComboBox):
        return(box.currentIndexChanged if int in signal_sig else
               box.currentTextChanged)

    # Strings (QLineEdit)
    elif isinstance(box, QW.QLineEdit):
        return(box.textChanged)

    # Labels (QLabel)
    elif isinstance(box, GW_QLabel):
        return(box.contentsChanged)
    elif isinstance(box, QW.QLabel):
        raise NotImplementedError("Default QW.QLabel has no modified signal "
                                  "defined. Use QW_QLabel instead!")

    # If none applies, raise error
    else:
        raise NotImplementedError("Custom boxes must provide their own "
                                  "'modified' signal! (%s)" % (box.__class__))


# This function sets the value of a provided box
def set_box_value(box, value, *value_sig):
    """
    Sets the value of the provided widget `box` to `value`.

    If `box` has the `set_box_value()` method defined (always the case for
    instances of :class:`~BaseBox`), it will be used instead. If this raises a
    :class:`~NotImplementedError`, the method is skipped.

    Parameters
    ----------
    box : :obj:`~PyQt5.QtWidgets.QWidget` object
        The widget whose value must be set.
    value : obj
        The value that must be set in the provided `box`.
        If `box` has the `set_box_value()` method defined, this argument is
        passed it.
    value_sig : positional arguments of object
        The signature of the value that must be set in the provided `box`.
        This argument is only used if the signature cannot be derived from
        `value`.
        If `box` has the `set_box_value()` method defined, this argument is
        passed to it.

    """

    # Custom boxes (set_box_value()-method)
    if hasattr(box, 'set_box_value'):
        # Try to use the custom set_box_value()-method
        try:
            box.set_box_value(value, *value_sig)
        # If that fails, proceed to use a normal function
        except NotImplementedError:
            pass
        # If that succeeds, return
        else:
            return

    # Values (QAbstractSpinBox)
    if isinstance(box, QW.QAbstractSpinBox):
        box.setValue(value)

    # Actions, Bools/Buttons (QAction, QAbstractButton)
    elif isinstance(box, (QW.QAction, QW.QAbstractButton)):
        if isinstance(value, STR_TYPES):
            box.setText(value)
        else:
            box.setChecked(value)

    # Items (QComboBox)
    elif isinstance(box, QW.QComboBox):
        if isinstance(value, INT_TYPES):
            box.setCurrentIndex(value)
        else:
            index = box.findText(value)
            if(index != -1):
                box.setCurrentIndex(index)
            elif box.isEditable():
                # Obtain current index and text of this combobox
                index = box.currentIndex()
                text = box.currentText()

                # Block all signals coming from this combobox
                blocked = box.blockSignals(True)

                # Set the current index to -1 and set the text to value
                box.setCurrentIndex(-1)
                box.setCurrentText(value)

                # No longer block signals (unless they were blocked before)
                box.blockSignals(blocked)

                # Emit the proper signals if their values actually changed
                if(text != value):
                    box.currentTextChanged.emit(value)
                if(index != -1):
                    box.currentIndexChanged.emit(-1)

    # Tabs (QTabWidget)
    elif isinstance(box, QW.QTabWidget):
        if isinstance(value, INT_TYPES):
            box.setCurrentIndex(value)
        elif isinstance(value, STR_TYPES) and isinstance(box, GW_QTabWidget):
            index = box.tabNames.index(value)
            box.setCurrentIndex(index)
        else:
            box.setCurrentWidget(value)

    # Strings (QLineEdit)
    elif isinstance(box, QW.QLineEdit):
        box.setText(value)

    # Labels (QLabel)
    elif isinstance(box, QW.QLabel):
        if isinstance(value, STR_TYPES):
            box.setText(value)
        elif isinstance(value, FLOAT_TYPES):
            box.setNum(value)
        elif isinstance(value, QG.QMovie):
            box.setMovie(value)
        elif isinstance(value, QG.QPicture):
            box.setPicture(value)
        elif isinstance(value, QG.QPixmap):
            box.setPixmap(value)
        else:
            raise TypeError("QLabel does not support the given type")

    # If none applies, raise error
    else:
        raise NotImplementedError("Custom boxes must provide their own "
                                  "'set_box_value()'-method! (%s)"
                                  % (box.__class__))
