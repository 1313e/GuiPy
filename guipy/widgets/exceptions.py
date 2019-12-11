# -*- coding: utf-8 -*-

"""
Exception Widgets
=================
Provides all definitions required for handling exceptions in *GuiPy*.

"""


# %% IMPORTS
# Built-in imports
from traceback import format_exception_only, format_tb

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.layouts import QW_QGridLayout, QW_QVBoxLayout
from guipy.widgets import (
    QW_QDialog, QW_QLabel, QW_QMessageBox, QW_QTextEdit, QW_QWidget)


# All declaration
__all__ = ['ExceptionDialog', 'create_exception_handler']


# %% CLASS DEFINITIONS
# Make special class for showing exception details
class ExceptionDialog(QW_QDialog):
    """
    Defines the :class:`~ExceptionDialog` class.

    This class takes a set of exception details and converts it into a format
    that can be shown using a dialog.

    """

    def __init__(self, etype, value, tb, parent=None):
        """
        Initialize an instance of the :class:`~ExceptionDialog` class.

        Parameters
        ----------
        etype : :class:`~Exception` class
            The :class:`~Exception` class that is associated with this error.
        value : :obj:`~Exception` object
            The :class:`~Exception` instance that is associated with this
            error.
        tb : traceback object
            The corresponding traceback object.

        Optional
        --------
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
            The parent widget for this dialog or *None* for no parent.

        """

        # Save the provided values
        self.etype = etype
        self.value = value
        self.tb = tb

        # Call the super constructor
        super().__init__(parent)

        # Initialize the exception dialog
        self.init()

    # This function creates the exception dialog
    def init(self):
        """
        Sets up the exception dialog after it has been initialized.

        This function is mainly responsible for gathering all required
        information; formatting it; and drawing the dialog.

        """

        # Create a window layout
        grid_layout = QW_QGridLayout(self)
        grid_layout.setColumnStretch(2, 1)
        grid_layout.setRowStretch(3, 1)

        # Set properties of message box
        self.setWindowModality(QC.Qt.ApplicationModal)
        self.setAttribute(QC.Qt.WA_DeleteOnClose)
        self.setWindowTitle("ERROR")
        self.setWindowFlags(
            QC.Qt.MSWindowsOwnDC |
            QC.Qt.Dialog |
            QC.Qt.WindowTitleHint |
            QC.Qt.WindowSystemMenuHint |
            QC.Qt.WindowCloseButtonHint)

        # Set the icon of the exception on the left
        icon_label = QW_QLabel()
        pixmap = QW_QMessageBox.standardIcon(QW_QMessageBox.Critical)
        icon_label.setPixmap(pixmap)
        grid_layout.addWidget(icon_label, 0, 0, 2, 1, QC.Qt.AlignTop)

        # Add a spacer item
        spacer_item = QW.QSpacerItem(7, 1, QW.QSizePolicy.Fixed,
                                     QW.QSizePolicy.Fixed)
        grid_layout.addItem(spacer_item, 0, 1, 2, 1)

        # Set the text of the exception
        exc_str = self.format_exception()
        exc_label = QW_QLabel(exc_str)
        grid_layout.addWidget(exc_label, 0, 2, 1, 1)

        # Create a button box for the buttons
        button_box = QW.QDialogButtonBox()
        grid_layout.addWidget(button_box, 2, 0, 1, grid_layout.columnCount())

        # Create traceback box
        self.tb_box = self.create_traceback_box()
        grid_layout.addWidget(self.tb_box, 3, 0, 1, grid_layout.columnCount())

        # Create traceback button
        self.tb_but =\
            button_box.addButton(self.tb_labels[self.tb_box.isHidden()],
                                 button_box.ActionRole)
        self.tb_but.clicked.connect(self.toggle_traceback_box)

        # Create an 'ok' button
        ok_but = button_box.addButton(button_box.Ok)
        ok_but.clicked.connect(self.close)
        ok_but.setDefault(True)

        # Update the size
        self.update_size()

    # This function formats the exception string
    def format_exception(self):
        """
        Formats the exception provided during initialization and returns it.

        """

        # Format the exception
        exc_list = format_exception_only(self.etype, self.value)
        exc_str = ''.join(exc_list)

        # Return it
        return(exc_str)

    # This function formats the traceback string
    def format_traceback(self):
        """
        Formats the traceback provided during initialization and returns it.

        """

        # Format the traceback
        tb_list = format_tb(self.tb)
        tb_str = ''.join(tb_list)

        # Return it
        return(tb_str)

    # This function creates the traceback box
    def create_traceback_box(self):
        """
        Creates a special box for the exception dialog that contains the
        traceback information and returns it.

        """

        # Create a traceback box
        traceback_box = QW_QWidget(self)
        traceback_box.setHidden(True)

        # Create layout
        layout = QW_QVBoxLayout()
        layout.setContentsMargins(QC.QMargins())
        traceback_box.setLayout(layout)

        # Add a horizontal line to the layout
        layout.addSeparator()

        # Format the traceback
        tb_str = self.format_traceback()

        # Add a textedit to the layout
        tb_text_box = QW_QTextEdit(traceback_box)
        tb_text_box.setMinimumHeight(100)
        tb_text_box.setFocusPolicy(QC.Qt.NoFocus)
        tb_text_box.setReadOnly(True)
        tb_text_box.setText(tb_str)
        layout.addWidget(tb_text_box)

        # Create a 'show traceback' button
        self.tb_labels = ['Hide Traceback...', 'Show Traceback...']

        # Return traceback box
        return(traceback_box)

    # This function shows or hides the traceback box
    @QC.Slot()
    def toggle_traceback_box(self):
        """
        Toggles the visibility of the traceback box and updates the dimensions
        of the exception dialog accordingly.

        """

        # Toggle the visibility of the traceback box
        self.tb_box.setVisible(self.tb_box.isHidden())
        self.tb_but.setText(self.tb_labels[self.tb_box.isHidden()])

        # Update the size of the message box
        self.update_size()

    # This function updates the size of the dialog
    def update_size(self):
        """
        Updates the dimensions of the exception dialog depending on its current
        state (traceback box visibility).

        """

        # Determine the minimum/maximum size required for making the dialog
        min_size = self.layout().minimumSize()
        max_size = self.layout().maximumSize()

        # Set the fixed width
        self.setFixedWidth(min_size.width())

        # If the traceback box is shown, set minimum/maximum height
        if self.tb_box.isVisible():
            self.setMinimumHeight(min_size.height())
            self.setMaximumHeight(max_size.height())
        # Else, set fixed height
        else:
            self.setFixedHeight(min_size.height())


# %% FUNCTION DEFINITIONS
# This function factory creates a function for handling exceptions
def create_exception_handler(parent=None):
    """
    Function factory that returns a function definition
    ``show_exception_details(*args, **kwargs)``.

    Calling the returned definition will automatically initialize an
    :obj:`~guipy.widgets.exceptions.ExceptionDialog` object using the provided
    `parent`, `args` and `kwargs`; and show the dialog.

    Optional
    --------
    parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
        The parent widget to use for the exception dialog or *None* for no
        parent.

    """

    # This function creates a message box with exception information
    def show_exception_details(*args, **kwargs):
        """
        Creates an instance of the :class:`~ExceptionDialog` class and shows
        it.

        Optional
        --------
        args : positional arguments
            The positional arguments that must be passed to the constructor of
            the :class:`~guipy.widgets.exceptions.ExceptionDialog` class.
        kwargs : keyword arguments
            The keyword arguments that must be passed to the constructor of the
            :class:`~guipy.widgets.exceptions.ExceptionDialog` class.

        """

        # Create exception message box
        exception_box = ExceptionDialog(*args, parent=parent, **kwargs)

        # Emit the exception signal of the parent if it has it
        if hasattr(parent, 'exception'):
            parent.exception.emit()

        # Show the exception message box
        exception_box.show()

    # Return function definition
    return(show_exception_details)
