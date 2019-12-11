# -*- coding: utf-8 -*-

"""
Tab Bars
========

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy.widgets import QW_QLineEdit, QW_QTabBar, get_box_value

# All declaration
__all__ = ['EditableTabBar', 'TabNameEditor']


# %% CLASS DEFINITIONS
# Custom QTabBar definition that allows for tab names to be edited
class EditableTabBar(QW_QTabBar):
    # Initialize EditableTabBar class
    def __init__(self, parent=None, *args, **kwargs):
        # Call super constructor
        super().__init__(parent)

        # Set up the tab bar
        self.init(*args, **kwargs)

    # This function sets up the editable tab bar
    def init(self):
        # Connecting signals
        self.tabBarDoubleClicked.connect(self.edit_tab_name)

        # Initialize a tab name editor
        self.name_editor = TabNameEditor(self)

    # This function edits the name of a tab
    @QC.Slot(int)
    def edit_tab_name(self, index):
        """
        Edits the name of the tab given by the provided `index`.

        """

        # Open tab name editor
        self.name_editor(index)


# Custom QLineEdit used for renaming a tab
class TabNameEditor(QW_QLineEdit):
    def __init__(self, tabbar_obj, *args, **kwargs):
        # Save provided tabbar_obj
        self.tabbar = tabbar_obj

        # Call super constructor
        super().__init__(tabbar_obj)

        # Set up name editor
        self.init(*args, **kwargs)

    # This function allows a specified tab's name to be edited
    def __call__(self, index):
        # Save this index
        self.index = index

        # Set the focus to this lineedit
        self.setFocus(True)

        # Obtain the size of the tab
        rect = self.tabbar.tabRect(index)

        # Adjust lineedit size to perfectly match underlying tab
        if(index != self.tabbar.count()-1):
            rect.adjust(1, 1, 0, -1)
        else:
            rect.adjust(1, 1, -1, -1)

        # Set size of editor
        self.setFixedSize(rect.size())

        # Move the editor on top of the tab
        self.move(self.tabbar.mapToGlobal(rect.topLeft()))

        # Obtain the name of the tab
        name = self.tabbar.tabText(index)

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
            QC.Qt.FramelessWindowHint |
            QC.Qt.NoDropShadowWindowHint)

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
        :obj:`~TabNameEditor` was called.

        """

        # Obtain the current text in the lineedit
        name = get_box_value(self)

        # If name is not empty, set name
        if name:
            # Set the name of the tab indicated with index
            self.tabbar.setTabText(self.index, name)
