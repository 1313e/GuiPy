# -*- coding: utf-8 -*-

"""
Widgets Core
============
Provides a collection of utility functions and the :class:`~BaseBox` class
definition, which are core to the functioning of all widgets.

"""


# %% IMPORTS
# Package imports
import numpy as np
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy.widgets.base import QW_QLabel, QW_QTabWidget, QW_QWidget

# All declaration
__all__ = ['BaseBox', 'get_box_value', 'get_modified_box_signal',
           'set_box_value']


# %% CLASS DEFINITIONS
# Make base class for custom boxes
# As QW.QWidget is a strict class (in C++), this cannot be an ABC
# TODO: Create a DualBaseBox class for dual widgets?
class BaseBox(QW_QWidget):
    """
    Defines the :class:`~BaseBox` base class.

    This class is used by many custom :class:`~PyQt5.QtWidgets.QWidget` classes
    as their base. It defines the :attr:`~modified` signal, which is
    automatically connected to any widget that changes its state.

    """

    # Define modified signal
    modified = QC.Signal()

    # Initialize the BaseBox class
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(*args, **kwargs)

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
        if(event.type() == QC.QEvent.ChildAdded):
            # Obtain child object
            child = event.child()

            # Try to obtain the modified signal of this child
            try:
                signal = get_modified_box_signal(child)
            # If this fails, it does not have one
            except NotImplementedError:
                pass
            # If this succeeds, connect it to the 'modified' signal
            else:
                signal.connect(self.modified)

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
        signal = get_modified_box_signal(box)

        # Connect the signals
        signal.connect(self.modified)

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

    # Bools/Buttons (QAbstractButton)
    elif isinstance(box, QW.QAbstractButton):
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
def get_modified_box_signal(box, *signal_sig):
    """
    Retrieves a signal of the provided widget `box` that indicates that `box`
    has been modified and returns it.

    If `box` has the `modified` signal defined (always the case for instances
    of :class:`~BaseBox`), it will be returned instead.

    Parameters
    ----------
    box : :obj:`~PyQt5.QtWidgets.QWidget` object
        The widget whose modified signal must be retrieved.
    signal_sig : positional arguments of object
        The signature of the modified signal that is requested.
        If empty or invalid, the default modified signal is returned.
        If `box` has the `modified` signal defined, this argument has no
        effect.

    Returns
    -------
    modified_signal : :obj:`~PyQt5.QtCore.pyqtBoundSignal` object
        The requested modified signal of `box`.

    """

    # Custom boxes (modified signal)
    if hasattr(box, 'modified'):
        return(box.modified)

    # Values (QAbstractSpinBox)
    elif isinstance(box, QW.QAbstractSpinBox):
        return(box.valueChanged)

    # Bools/Buttons (QAbstractButton)
    elif isinstance(box, QW.QAbstractButton):
        return(box.toggled if box.isCheckable() else box.clicked)

    # Items (QComboBox)
    elif isinstance(box, QW.QComboBox):
        return(box.currentIndexChanged if int in signal_sig else
               box.currentTextChanged)

    # Tabs (QTabWidget)
    elif isinstance(box, QW_QTabWidget):
        if int in signal_sig:
            return(box.currentIndexChanged)
        elif str in signal_sig:
            return(box.currentTextChanged)
        elif QW.QWidget in signal_sig:
            return(box.currentWidgetChanged)
        else:
            return(box.currentChanged)
    elif isinstance(box, QW.QTabWidget):
        return(box.currentChanged)

    # Strings (QLineEdit)
    elif isinstance(box, QW.QLineEdit):
        return(box.textChanged)

    # Labels (QLabel)
    elif isinstance(box, QW_QLabel):
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

    # Bools/Buttons (QAbstractButton)
    elif isinstance(box, QW.QAbstractButton):
        if isinstance(value, str):
            box.setText(value)
        else:
            box.setChecked(value)

    # Items (QComboBox)
    elif isinstance(box, QW.QComboBox):
        if isinstance(value, int):
            box.setCurrentIndex(value)
        else:
            index = box.findText(value)
            if(index != -1):
                box.setCurrentIndex(index)
            else:
                box.setCurrentText(value)

    # Tabs (QTabWidget)
    elif isinstance(box, QW.QTabWidget):
        if isinstance(value, int):
            box.setCurrentIndex(value)
        elif isinstance(value, str) and isinstance(box, QW_QTabWidget):
            index = box.tabNames.index(value)
            box.setCurrentIndex(index)
        else:
            box.setCurrentWidget(value)

    # Strings (QLineEdit)
    elif isinstance(box, QW.QLineEdit):
        box.setText(value)

    # Labels (QLabel)
    elif isinstance(box, QW.QLabel):
        if isinstance(value, str):
            box.setText(value)
        elif isinstance(value, (int, float, np.integer, np.floating)):
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
