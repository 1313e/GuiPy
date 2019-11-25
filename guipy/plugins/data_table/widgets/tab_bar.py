# -*- coding: utf-8 -*-

"""
Data Table Tab Bar
==================

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy.widgets import QW_QLineEdit, QW_QTabBar, get_box_value

# All declaration
__all__ = ['DataTableNameEditor', 'DataTableTabBar']


# %% CLASS DEFINITIONS
# Custom QLineEdit used for renaming a data table
class DataTableNameEditor(QW_QLineEdit):
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(*args, **kwargs)

        # Set up name editor
        self.init()

    # This function allows a specified tab's name to be edited
    def __call__(self, index):
        # Save this index
        self.index = index

        # Set the focus to this lineedit
        self.setFocus(True)

        # Obtain the size of the tab
        rect = self.parent().tabRect(index)

        # Adjust lineedit size to perfectly match underlying tab
        if(index != self.parent().count()-1):
            rect.adjust(1, 1, 0, -1)
        else:
            rect.adjust(1, 1, -1, -1)

        # Set size of editor
        self.setFixedSize(rect.size())

        # Move the editor on top of the tab
        self.move(self.parent().mapToGlobal(rect.topLeft()))

        # Obtain the name of the tab
        name = self.parent().tabText(index)

        # Set the current name in the editor and select it
        self.setText(name)
        self.selectAll()

        # Show the editor
        self.show()

    # This function sets up the name editor
    def init(self):
        # Install event filter to catch events that should close the popup
        self.installEventFilter(self)

        # Set dialog flags
        self.setWindowFlags(
            QC.Qt.Popup |
            QC.Qt.FramelessWindowHint)

        # Turn frame off
        self.setFrame(False)

        # Set text margins to line up perfectly with tab
        self.setTextMargins(9, 0, 0, 0)

        # Connect signals
        self.editingFinished.connect(self.set_tab_name)

    # Override eventFilter to filter out clicks, ESC and Enter
    def eventFilter(self, widget, event):
        # Check if the event involves anything for which the popup should close
        if (((event.type() == QC.QEvent.MouseButtonPress) and
             not self.geometry().contains(event.globalPos())) or
            ((event.type() == QC.QEvent.KeyPress) and
             event.key() in (QC.Qt.Key_Escape,
                             QC.Qt.Key_Enter,
                             QC.Qt.Key_Return))):
            # Exit the editor
            self.hide()
            self.setFocus(False)
            return(True)

        # Else, process events as normal
        else:
            return(super().eventFilter(widget, event))

    # This function sets the name of a data table tab
    @QC.Slot()
    def set_tab_name(self):
        """
        Sets the name of the tab that was being edited when this
        :obj:`~DataTableNameEditor` was called.

        """

        # Obtain the current text in the lineedit
        name = get_box_value(self)

        # Set the name of the tab indicated with index
        self.parent().setTabText(self.index, name)

        # Emit signal of parent
        self.parent().dataTableNameChanged.emit(self.index, name)


# Custom QTabBar definition for the DataTable plugin
class DataTableTabBar(QW_QTabBar):
    # Signals
    dataTableNameChanged = QC.Signal([int, str])

    # Initialize DataTableTabBar class
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(*args, **kwargs)

        # Set up the tab bar
        self.init()

    # This function sets up the data table tab bar
    def init(self):
        # Connecting signals
        self.tabBarDoubleClicked.connect(self.edit_tab_name)

        # Initialize a tab name editor
        self.name_editor = DataTableNameEditor(self)

    # This function edits the name of a data table tab
    @QC.Slot(int)
    def edit_tab_name(self, index):
        """
        Edits the name of the data table tab given by the provided `index`.

        """

        # Open tab name editor
        self.name_editor(index)
