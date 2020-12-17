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
from guipy import layouts as GL, plugins as GP, widgets as GW
from guipy.config import FILE_FILTERS
from guipy.plugins.data_table.formatters import import_formatters, FORMATTERS
from guipy.plugins.data_table.widgets import DataTableWidget
from guipy.widgets import set_box_value

# All declaration
__all__ = ['DataTable']


# %% CLASS DEFINITIONS
# Define class for the DataTable plugin
class DataTable(GP.BasePluginWidget):
    # Properties
    TITLE = "Data table"
    LOCATION = QC.Qt.LeftDockWidgetArea

    # Initialize DataTable plugin
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(*args, **kwargs)

        # Set up the data table plugin
        self.init()

    # This function sets up the data table plugin
    def init(self):
        # Import all DataTable formatters
        import_formatters()

        # Create a layout
        layout = GL.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a tab widget
        tab_widget = GW.QTabWidget(browse_tabs=True)
        tab_widget.setTabBar(GW.EditableTabBar())
        tab_widget.setMovable(True)
        tab_widget.setTabsClosable(True)

        # Connect tab widget signals
        tab_widget.tabTextChanged.connect(self.set_tab_name)
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
        # Block all signals emitted by the tab widget while removing tabs
        self.tab_widget.blockSignals(True)

        # Close all tabs
        for index in reversed(range(self.tab_widget.count())):
            self.close_tab(index)

        # Call super event
        super().closeEvent(*args, **kwargs)

    # This function adds all associated actions to the menus and toolbars
    def add_actions(self):
        # Initialize empty action lists for this plugin
        self.MENU_ACTIONS = {
            **GP.BasePluginWidget.MENU_ACTIONS,
            'File': [],
            'File/New': []}
        self.TOOLBAR_ACTIONS = {
            **GP.BasePluginWidget.TOOLBAR_ACTIONS,
            'File': []}

        # Add new tab action to file/new menu
        new_tab_act = GW.QAction(
            self, 'Data &table',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_T,
            tooltip="New data table",
            triggered=self.add_tab,
            role=GW.QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File/New'].append(new_tab_act)
        self.MENU_ACTIONS['File/New'].append(self.add_tab)

        # Add open tabs action to file menu/toolbar
        open_tabs_act = GW.QAction(
            self, '&Open...',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_O,
            tooltip="Open data table",
            triggered=self.open_tabs,
            role=GW.QAction.ApplicationSpecificRole)
        open_tabs_act.setEnabled(False)
        self.MENU_ACTIONS['File'].append(open_tabs_act)
        self.TOOLBAR_ACTIONS['File'].append(open_tabs_act)

        # Add import tabs action to file menu/toolbar
        import_tabs_act = GW.QAction(
            self, '&Import...',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_I,
            tooltip="Import data tables",
            triggered=self.import_tabs,
            role=GW.QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File'].append(import_tabs_act)
        self.TOOLBAR_ACTIONS['File'].append(import_tabs_act)

        # Add separator to file menu
        self.MENU_ACTIONS['File'].append(None)

        # Add save tab action to file menu/toolbar
        save_tab_act = GW.QAction(
            self, '&Save',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_S,
            tooltip="Save current data table",
            triggered=self.save_tab,
            role=GW.QAction.ApplicationSpecificRole)
        save_tab_act.setEnabled(False)
        self.MENU_ACTIONS['File'].append(save_tab_act)
        self.TOOLBAR_ACTIONS['File'].append(save_tab_act)

        # Add save_as tab action to file menu
        save_as_tab_act = GW.QAction(
            self, 'Save &as...',
            shortcut=QC.Qt.CTRL + QC.Qt.SHIFT + QC.Qt.Key_S,
            tooltip="Save current data table as...",
            triggered=self.save_as_tab,
            role=GW.QAction.ApplicationSpecificRole)
        save_as_tab_act.setEnabled(False)
        self.MENU_ACTIONS['File'].append(save_as_tab_act)

        # Add save_all tab action to file menu/toolbar
        save_all_tabs_act = GW.QAction(
            self, 'Sav&e all',
            shortcut=QC.Qt.CTRL + QC.Qt.ALT + QC.Qt.Key_S,
            tooltip="Save all data tables",
            triggered=self.save_all_tabs,
            role=GW.QAction.ApplicationSpecificRole)
        save_all_tabs_act.setEnabled(False)
        self.MENU_ACTIONS['File'].append(save_all_tabs_act)
        self.TOOLBAR_ACTIONS['File'].append(save_all_tabs_act)

        # Add export tab action to file menu/toolbar
        export_tab_act = GW.QAction(
            self, '&Export...',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_E,
            tooltip="Export current data table",
            triggered=self.export_tab,
            role=GW.QAction.ApplicationSpecificRole)
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
        data_table.tab_name = name

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
        filepaths, _ = GW.getOpenFileNames(
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
        # Get data table
        data_table = self.dataTable()
        name = data_table.tab_name

        # Open the file saving system
        filepath, selected_filter = GW.getSaveFileName(
            parent=self,
            caption="Export data table %r to..." % (name),
            basedir=name,
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
            FORMATTERS[ext].exporter(data_table, filepath)

    # This function sets the name of a given tab
    @QC.Slot(int, str)
    def set_tab_name(self, index, name):
        # Obtain the data_table belonging to index
        data_table = self.tab_widget.widget(index)

        # Set its name
        data_table.tab_name = name

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

    # This function returns the text of the tab belonging to the specified int
    @QC.Slot(int)
    def tabText(self, index=None):
        """
        Returns the text of the tab with the provided tab `index`.

        Optional
        --------
        index : int or None. Default: None
            If int, the index of the tab whose text is requested.
            If *None*, the current tab text is requested.

        Returns
        -------
        text : str
            The text of the tab specified by the provided `index`.

        """

        # If index is None, return current tab text
        if index is None:
            index = self.tab_widget.currentIndex()

        # Return the text of the tab with the provided index
        return(self.tab_widget.tabText(index))
