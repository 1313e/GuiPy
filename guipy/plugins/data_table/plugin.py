# -*- coding: utf-8 -*-

"""
Data Table Plugin
=================

"""


# %% IMPORTS
# Built-in imports
from os import path

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.config import FILE_FILTERS
from guipy.layouts import QW_QVBoxLayout
from guipy.plugins.base import BasePluginWidget
from guipy.plugins.data_table.formatters import FORMATTERS
from guipy.plugins.data_table.widgets import DataTableWidget
from guipy.widgets import (
    EditableTabBar, QW_QAction, QW_QTabWidget, getOpenFileNames,
    getSaveFileName, set_box_value)

# All declaration
__all__ = ['DataTable']


# %% CLASS DEFINITIONS
# Define class for the DataTable plugin
class DataTable(BasePluginWidget):
    # Properties
    TITLE = "Data table"
    LOCATION = QC.Qt.LeftDockWidgetArea

    # Initialize DataTable plugin
    def __init__(self, parent=None, *args, **kwargs):
        # Call super constructor
        super().__init__(parent)

        # Set up the data table plugin
        self.init(*args, **kwargs)

    # This function sets up the data table plugin
    def init(self):
        # Create a layout
        layout = QW_QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a tab widget
        tab_widget = QW_QTabWidget()
        tab_widget.setTabBar(EditableTabBar())
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
            'File': [],
            'File/New': []}
        self.TOOLBAR_ACTIONS = {
            'File': []}

        # Add new tab action to file/new menu
        new_tab_act = QW_QAction(
            self, 'Data &table',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_T,
            tooltip="New data table",
            triggered=self.add_tab,
            role=QW_QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File/New'].append(new_tab_act)
        self.MENU_ACTIONS['File/New'].append(self.add_tab)

        # Add open tabs action to file menu/toolbar
        open_tabs_act = QW_QAction(
            self, '&Open...',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_O,
            tooltip="Open data table",
            triggered=self.open_tabs,
            role=QW_QAction.ApplicationSpecificRole)
        open_tabs_act.setEnabled(False)
        self.MENU_ACTIONS['File'].append(open_tabs_act)
        self.TOOLBAR_ACTIONS['File'].append(open_tabs_act)

        # Add import tabs action to file menu/toolbar
        import_tabs_act = QW_QAction(
            self, '&Import...',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_I,
            tooltip="Import data tables",
            triggered=self.import_tabs,
            role=QW_QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File'].append(import_tabs_act)
        self.TOOLBAR_ACTIONS['File'].append(import_tabs_act)

        # Add separator to file menu
        self.MENU_ACTIONS['File'].append(None)

        # Add save tab action to file menu/toolbar
        save_tab_act = QW_QAction(
            self, '&Save',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_S,
            tooltip="Save current data table",
            triggered=self.save_tab,
            role=QW_QAction.ApplicationSpecificRole)
        save_tab_act.setEnabled(False)
        self.MENU_ACTIONS['File'].append(save_tab_act)
        self.TOOLBAR_ACTIONS['File'].append(save_tab_act)

        # Add save_as tab action to file menu
        save_as_tab_act = QW_QAction(
            self, 'Save &as...',
            shortcut=QC.Qt.CTRL + QC.Qt.SHIFT + QC.Qt.Key_S,
            tooltip="Save current data table as...",
            triggered=self.save_as_tab,
            role=QW_QAction.ApplicationSpecificRole)
        save_as_tab_act.setEnabled(False)
        self.MENU_ACTIONS['File'].append(save_as_tab_act)

        # Add save_all tab action to file menu/toolbar
        save_all_tabs_act = QW_QAction(
            self, 'Sav&e all',
            shortcut=QC.Qt.CTRL + QC.Qt.ALT + QC.Qt.Key_S,
            tooltip="Save all data tables",
            triggered=self.save_all_tabs,
            role=QW_QAction.ApplicationSpecificRole)
        save_all_tabs_act.setEnabled(False)
        self.MENU_ACTIONS['File'].append(save_all_tabs_act)
        self.TOOLBAR_ACTIONS['File'].append(save_all_tabs_act)

        # Add export tab action to file menu/toolbar
        export_tab_act = QW_QAction(
            self, '&Export...',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_E,
            tooltip="Export current data table",
            triggered=self.export_tab,
            role=QW_QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File'].append(export_tab_act)
        self.TOOLBAR_ACTIONS['File'].append(export_tab_act)

        # Add separator to file menu
        self.MENU_ACTIONS['File'].append(None)

    # This function adds a new data table widget
    @QC.Slot()
    def add_tab(self, name=None, import_func=None):
        # Create a new DataTableWidget
        data_table = DataTableWidget(self, import_func)

        # If name is None, set it to default
        if name is None:
            name = "table_%i" % (self.tab_widget.count())

        # Add data_table to the tab widget
        index = self.tab_widget.addTab(data_table, name)

        # Switch focus to the new tab
        set_box_value(self.tab_widget, index)

    # This function closes a data table widget
    # TODO: Warn the user about closing a tab if it has unsaved changes
    @QC.Slot(int)
    def close_tab(self, index):
        # Obtain the DataTableWidget object associated with this index
        data_table = self.dataTable(index)

        # Close this data_table
        data_table.close()

        # Remove this data_table from the tab widget
        self.tab_widget.removeTab(index)

    # This function opens a data table widget
    @QC.Slot()
    def open_tabs(self):
        pass

    # This function imports a data table widget
    @QC.Slot()
    def import_tabs(self):
        # Open the file opening system
        filepaths, _ = getOpenFileNames(
            parent=self,
            caption="Import data tables",
            filters=FORMATTERS.keys())

        # Loop over filepaths and make a tab for every entry
        for filepath in filepaths:
            # Obtain the name and extension of this data table
            name, ext = path.splitext(path.basename(filepath))

            # Add a new tab
            self.add_tab(name, lambda x: FORMATTERS[ext].importer(filepath, x))

    # This function saves a data table widget
    @QC.Slot()
    def save_tab(self):
        pass

    # This function saves a data table widget with chosen name
    @QC.Slot()
    def save_as_tab(self):
        pass

    # This function saves all data table widgets
    @QC.Slot()
    def save_all_tabs(self):
        pass

    # This function exports a data table
    @QC.Slot()
    def export_tab(self):
        # Get name of this data table
        name = self.tabName()

        # Open the file saving system
        filepath, selected_filter = getSaveFileName(
            parent=self,
            caption="Export data table %r to..." % (name),
            basedir=name+'.npz',
            filters=FORMATTERS.keys())

        # If filepath is not empty, export data table
        if filepath:
            # Obtain the ext of the filepath
            ext = path.splitext(filepath)[1]

            # If ext is empty, check what filter was used
            if not ext:
                # If "All (Supported) Files" was not used, get ext from filter
                if not selected_filter.startswith("All "):
                    ext = FILE_FILTERS[selected_filter]
                # Else, set it to '.npz'
                else:
                    ext = '.npz'

                # Add extension to filepath
                filepath += ext

            # Export data table
            FORMATTERS[ext].exporter(self.dataTable(), filepath)

    # This function returns the data table belonging to a specified int
    @QC.Slot(int)
    def dataTable(self, index=None):
        """
        Returns the :obj:`~DataTableWidget` object that belongs to the table
        with the provided tab `index`.

        Optional
        --------
        index : int or None. Default: None
            If int, the index of the tab whose table is requested.
            If *None*, the current table is requested.

        Returns
        -------
        data_table : :obj:`~DataTableWidget` object
            The data table that belongs to the tab specified by the
            provided `index`.

        """

        # If index is None, return current data table widget
        if index is None:
            index = self.tab_widget.currentIndex()

        # Return the data table widget with the provided index
        return(self.tab_widget.widget(index))

    # This function returns the name of the tab belonging to the specified int
    @QC.Slot(int)
    def tabName(self, index=None):
        """
        Returns the name of the tab with the provided tab `index`.

        Optional
        --------
        index : int or None. Default: None
            If int, the index of the tab whose name is requested.
            If *None*, the current tab name is requested.

        Returns
        -------
        name : str
            The name of the tab specified by the provided `index`.

        """

        # If index is None, return current tab name
        if index is None:
            index = self.tab_widget.currentIndex()

        # Return the name of the tab with the provided index
        return(self.tab_widget.tabText(index))
