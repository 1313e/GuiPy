# -*- coding: utf-8 -*-

"""
Figure Plugin
=============

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.layouts import QW_QVBoxLayout
from guipy.plugins.base import BasePluginWidget
from guipy.plugins.figure.widgets import FigureWidget
from guipy.widgets import QW_QAction, QW_QTabWidget

# All declaration
__all__ = ['Figure']


# %% CLASS DEFINITIONS
# Define class for the Figure plugin
class Figure(BasePluginWidget):
    # Properties
    TITLE = "Figure"
    LOCATION = QC.Qt.RightDockWidgetArea

    # Initialize Figure plugin
    def __init__(self, data_table_obj, parent=None, *args, **kwargs):
        # Save provided data table object
        self.data_table = data_table_obj

        # Call super constructor
        super().__init__(parent)

        # Set up the figure plugin
        self.init(*args, **kwargs)

    # This function sets up the figure plugin
    def init(self):
        # Create a layout
        layout = QW_QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Create a tab widget
        tab_widget = QW_QTabWidget()
        tab_widget.setElideMode(QC.Qt.ElideNone)
        tab_widget.setMovable(True)
        tab_widget.setTabsClosable(True)

        # Connect tab widget signals
        tab_widget.tabCloseRequested.connect(self.close_tab)

        # Add tab widget to layout
        self.tab_widget = tab_widget
        layout.addWidget(self.tab_widget)

        # Add all actions to the proper menus and toolbars
        self.add_actions()

        # Add a tab to the plugin
        self.add_tab()

    # Override closeEvent to do automatic clean-up
    def closeEvent(self, *args, **kwargs):
        # Close all tabs
        for index in reversed(range(self.tab_widget.count())):
            self.close_tab(index)

        # Call super event
        super().closeEvent(*args, **kwargs)

    # This function adds all associated actions to the menus and toolbars
    def add_actions(self):
        # Initialize empty action lists for this plugin
        self.MENU_ACTIONS = {
            'File/New': []}

        # Add new figure action to file/new menu
        # TODO: Should shortcut be CTRL+F? Might clash with expectations
        new_tab_act = QW_QAction(
            self, '&Figure',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_F,
            tooltip="New figure",
            triggered=self.add_tab,
            role=QW_QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File/New'].append(new_tab_act)

    # This function adds a new figure widget
    @QC.Slot()
    def add_tab(self, name=None):
        # Create a new FigureWidget
        figure = FigureWidget(self.data_table, self)

        # If name is None, set it to default
        if name is None:
            name = "figure_%i" % (self.tab_widget.count())

        # Add figure to the tab widget
        index = self.tab_widget.addTab(figure, name)

        # Switch focus to the new tab
        self.tab_widget.setCurrentIndex(index)

    # This function closes a figure widget
    @QC.Slot(int)
    def close_tab(self, index):
        # Obtain the FigureWidget object associated with this index
        figure = self.tab_widget.widget(index)

        # Close this figure
        figure.close()

        # Remove this figure from the tab widget
        self.tab_widget.removeTab(index)
