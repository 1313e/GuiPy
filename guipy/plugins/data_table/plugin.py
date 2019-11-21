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
from guipy.plugins.base import BasePluginWidget
from guipy.plugins.data_table.formatters import import_from_npz, export_to_npz
from guipy.plugins.data_table.widgets import DataTableWidget
from guipy.widgets import (
    QW_QAction, QW_QMenu, QW_QTabWidget, getOpenFileNames, getSaveFileName)
from guipy.widgets.utils import FILE_TYPES

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
        tab_widget = QW_QTabWidget()
        tab_widget.setElideMode(QC.Qt.ElideNone)
        tab_widget.setMovable(True)
        tab_widget.setTabsClosable(True)
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
        """


        """

        # Add new tab action to file menu/toolbar
        new_tab_act = QW_QAction(
            self, '&New...',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_N,
            tooltip="New data table",
            triggered=self.add_tab,
            role=QW_QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File'].append(new_tab_act)
        self.TOOLBAR_ACTIONS['File'].append(new_tab_act)

        # Add separator to file menu
        self.MENU_ACTIONS['File'].append(None)

        # Add open tabs action to file menu/toolbar
        open_tabs_act = QW_QAction(
            self, '&Open...',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_O,
            tooltip="Open data table",
            triggered=self.open_tabs,
            role=QW_QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File'].append(open_tabs_act)
        self.TOOLBAR_ACTIONS['File'].append(open_tabs_act)

        # Add import tabs action to file menu
        import_tabs_act = QW_QAction(
            self, '&Import...',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_I,
            tooltip="Import data table",
            triggered=self.import_tabs,
            role=QW_QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File'].append(import_tabs_act)

        # Add separator to file menu
        self.MENU_ACTIONS['File'].append(None)

        # Add save tab action to file menu/toolbar
        save_tab_act = QW_QAction(
            self, '&Save',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_S,
            tooltip="Save current data table",
            triggered=self.save_tab,
            role=QW_QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File'].append(save_tab_act)
        self.TOOLBAR_ACTIONS['File'].append(save_tab_act)

        # Add save_as tab action to file menu
        save_as_tab_act = QW_QAction(
            self, 'Save &as...',
            shortcut=QC.Qt.CTRL + QC.Qt.SHIFT + QC.Qt.Key_S,
            tooltip="Save current data table as...",
            triggered=self.save_as_tab,
            role=QW_QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File'].append(save_as_tab_act)

        # Add save_all tab action to file menu/toolbar
        save_all_tabs_act = QW_QAction(
            self, 'Sav&e all',
            shortcut=QC.Qt.CTRL + QC.Qt.ALT + QC.Qt.Key_S,
            tooltip="Save all data tables",
            triggered=self.save_all_tabs,
            role=QW_QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File'].append(save_all_tabs_act)
        self.TOOLBAR_ACTIONS['File'].append(save_all_tabs_act)

        # Add export tab menu to file menu
        export_tab_menu = self.create_export_tab_menu()
        self.MENU_ACTIONS['File'].append(export_tab_menu)

    # This function creates the export_tab menu
    def create_export_tab_menu(self):
        # Create the menu
        export_tab_menu = QW_QMenu('Export', '&Export to...')

        # Define list with all export-formats
        formats = ['npz']

        # Make sure formats is sorted
        formats.sort()

        # For every format, add an action to the export menu
        for ext in formats:
            # Obtain type of this file format
            file_type = FILE_TYPES[ext]

            # Create an action for this format
            act = QW_QAction(
                self, "*.%s (%s)" % (ext, file_type),
                tooltip="Export current data table to a .%s-file" % (ext),
                triggered=getattr(self, 'export_to_%s' % (ext)),
                role=QW_QAction.ApplicationSpecificRole)

            # Add it to the menu
            export_tab_menu.addAction(act)

        # Return the menu
        return(export_tab_menu)

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
        self.tab_widget.setCurrentIndex(index)

    # This function closes a data table widget
    # TODO: Warn the user about closing a tab if it has unsaved changes
    @QC.Slot(int)
    def close_tab(self, index):
        # Obtain the DataTableWidget object associated with this index
        data_table = self.tab_widget.widget(index)

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
            filters=['npz'])

        # Loop over filepaths and make a tab for every entry
        for filepath in filepaths:
            # Obtain the name of this data table
            name = path.splitext(path.basename(filepath))[0]

            # Add a new tab
            self.add_tab(name, lambda x: import_from_npz(filepath, x))

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

    # This function exports a data table to a NumPy Binary Archive file
    @QC.Slot()
    def export_to_npz(self):
        # Get name of this data table
        name = self.tabName()

        # Open the file saving system
        filepath, _ = getSaveFileName(
            parent=self,
            caption="Export data table %r to *.npz-file..." % (name),
            basedir=name+'.npz',
            filters=['npz'],
            initial_filter='npz')

        # If filepath is not empty, export data table
        if filepath:
            export_to_npz(self.dataTable(), filepath)

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
