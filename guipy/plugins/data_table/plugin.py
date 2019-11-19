# -*- coding: utf-8 -*-

"""
Data Table Plugin
=================

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.plugins.base import BasePluginWidget
from guipy.plugins.data_table.widgets import DataTableWidget
from guipy.widgets import QW_QAction

# All declaration
__all__ = ['DataTable']


# %% CLASS DEFINITIONS
# Define class for the DataTable plugin
class DataTable(BasePluginWidget):
    # Properties
    TITLE = "Data table"
    MENU_ACTIONS = {
        'File': []}
    TOOLBAR_ACTIONS = {
        'File': []}

    # Initialize DataTable plugin
    def __init__(self, parent=None, *args, **kwargs):
        # Call super constructor
        super().__init__(parent)

        # Set up the data table plugin
        self.init(*args, **kwargs)

    # This function sets up the data table plugin
    def init(self):
        # Create a layout
        layout = QW.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Create a tab widget
        tab_widget = QW.QTabWidget()
        tab_widget.setElideMode(QC.Qt.ElideNone)
        tab_widget.setMovable(True)
        tab_widget.setTabsClosable(True)
        tab_widget.tabCloseRequested.connect(self.close_tab)

        # Add tab widget to layout
        self.tab_widget = tab_widget
        layout.addWidget(self.tab_widget)

        # Add new tab action to file menu
        new_tab_act = QW_QAction(
            self, '&New table...',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_N,
            statustip="New data table",
            triggered=self.add_tab,
            role=QW_QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File'].append(new_tab_act)
        self.TOOLBAR_ACTIONS['File'].append(new_tab_act)

        # Add a tab to the plugin
        self.add_tab()

    # Override closeEvent to do automatic clean-up
    def closeEvent(self, *args, **kwargs):
        # Close all tabs
        for index in reversed(range(self.tab_widget.count())):
            self.close_tab(index)

        # Call super event
        super().closeEvent(*args, **kwargs)

    # This function adds a new data table widget
    @QC.Slot()
    def add_tab(self):
        # Create a DataTableWidget
        widget = DataTableWidget()

        # Add widget to the tab widget
        self.tab_widget.addTab(widget, "Table %i" % (self.tab_widget.count()))

    # This function closes a data table widget
    @QC.Slot(int)
    def close_tab(self, index):
        # Obtain the DataTableWidget object associated with this widget
        widget = self.tab_widget.widget(index)

        # Close this widget
        widget.close()

        # Remove this widget from the tab widget
        self.tab_widget.removeTab(index)
