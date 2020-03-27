# -*- coding: utf-8 -*-

"""
Main Window
===========
Provides the definition of the main window of the *GuiPy* application.

"""


# %% IMPORTS
# Built-in imports
import platform
from struct import calcsize
import sys
from textwrap import dedent

# Package imports
import qtpy
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy import __version__, APP_NAME, STR_TYPES
from guipy import plugins as GP, widgets as GW
from guipy.config import CONFIG
from guipy.widgets import create_exception_handler

# All declaration
__all__ = ['MainWindow']


# %% CLASS DEFINITIONS
# Define class for main window
# TODO: Write a lock-file system for GuiPy
class MainWindow(GW.QMainWindow):
    """
    Defines the :class:`~MainWindow` class for *GuiPy*.

    This class provides the main window for the GUI and combines all other
    widgets; layouts; and elements together.

    """

    # Signals
    exception = QC.Signal()

    # Initialize MainWindow class
    def __init__(self, *args, **kwargs):
        """
        Initialize an instance of the :class:`~MainWindow` class.

        """

        # Call super constructor
        super().__init__(*args, **kwargs)

        # Set up the main window
        self.init()

    # This function sets up the main window
    def init(self):
        """
        Sets up the main window after it has been initialized.

        This function is mainly responsible for initializing all other widgets
        that are required to make the GUI work, and connecting them together.

        """

        # Initialize the config manager
        CONFIG._init(self)

        # Make sure that the viewer is deleted when window is closed
        self.setAttribute(QC.Qt.WA_DeleteOnClose)

        # Set window title
        self.setWindowTitle(APP_NAME)

        # Disable the default context menu (right-click menu)
        self.setContextMenuPolicy(QC.Qt.NoContextMenu)

        # Create statusbar
        self.create_statusbar()

        # Create menus
        self.create_menus()

        # Create toolbars
        self.create_toolbars()

        # Add all required plugins
        self.add_plugins()

        # Add all remaining core actions
        self.add_core_actions()

        # Maximize the window
        self.setWindowState(QC.Qt.WindowMaximized)

        # Set the exception handler to an internal message window
        sys.excepthook = create_exception_handler(self)

        # Write the current GuiPy configuration to file
        CONFIG.write_config()

    # Override closeEvent to automatically close all plugins
    def closeEvent(self, *args, **kwargs):
        # Close all plugins in plugins dict
        for plugin in self.plugins.values():
            plugin.close()

        # Call super event
        super().closeEvent(*args, **kwargs)

    # This function creates the statusbar in the viewer
    def create_statusbar(self):
        """
        Creates the bottom-level statusbar of the main window, primarily used
        for displaying extended descriptions of actions.

        """

        # Obtain statusbar
        self.statusbar = self.statusBar()

    # This function adds a given menu to the top-level menu
    def addMenu(self, menu, parent_menu):
        """
        Adds a provided `menu` to the `parent_menu` and registers it.

        Parameters
        ----------
        menu : :obj:`~guipy.widgets.GW.QMenu` object
            The menu object that must be added to the top-level menubar.
        parent_menu : :obj:`~guipy.widgets.GW.QMenu` or \
            :obj:`~PyQt5.QtWidgets.QMenuBar` object
            The menu(bar) object to which the provided `menu` must be added.

        """

        # Add menu to the provided parent_menu
        parent_menu.addMenu(menu)

        # If parent_menu is the menubar, register menu as top-level
        if parent_menu is self.menuBar():
            self.menus[menu.name] = menu

        # Else, add it to the parent menu with the given name
        else:
            self.menus["%s/%s" % (parent_menu.name, menu.name)] = menu

    # This function creates the top-level menus in the viewer
    def create_menus(self):
        """
        Creates the menus in the top-level menubar of the main window.

        Other widgets can modify these menus to add additional actions to it.

        """

        # TOP-LEVEL MENUS
        # Make empty dict of top-level menus and actions
        self.menus = {}
        actions = {None: []}

        # Create file menu
        actions[None].append(GW.QMenu('File', '&File'))
        actions['File'] = []

        # Create view menu
        actions[None].append(GW.QMenu('View', '&View'))
        actions['View'] = []

        # Create help menu
        actions[None].append(GW.QMenu('Help', '&Help'))
        actions['Help'] = []

        # SUBMENUS
        # Add a New menu to file menu
        actions['File'].append(GW.QMenu('New', '&New...'))

        # Add a separator to file menu
        actions['File'].append(None)

        # Add a docks menu to view menu
        actions['View'].append(GW.QMenu('Docks', '&Docks'))

        # Add a separator to view menu
        actions['View'].append(None)

        # Add a toolbars menu to view menu
        actions['View'].append(GW.QMenu('Toolbars', '&Toolbars'))

        # Add all menus and actions
        self.add_menu_actions(actions)

    # Override addToolBar to register an action for toggling the toolbar
    def addToolBar(self, toolbar):
        """
        Adds a provided `toolbar` to the main window and registers it.

        Parameters
        ----------
        toolbar : :obj:`~guipy.widgets.GW.QToolBar` object
            The toolbar object that must be added to the main window.

        """

        # Call super method
        super().addToolBar(toolbar)

        # Register toolbar
        self.toolbars[toolbar.name] = toolbar

        # Add action for toggling the toolbar
        self.add_menu_actions({'View/Toolbars': [toolbar.toggleViewAction()]})

    # This function creates the toolbars in the viewer
    def create_toolbars(self):
        """
        Creates the toolbars of the main window.

        Other widgets can modify these toolbars to add additional actions to
        it.

        """

        # Make empty dict of toolbars and actions
        self.toolbars = {}
        actions = {}

        # FILE
        # Create file toolbar
        self.addToolBar(GW.QToolBar('File', 'File toolbar'))
        actions['File'] = []

        # ACTIONS
        # Add the File/New menu to the File toolbar
        actions['File'].append(self.menus['File/New'])

        # Add all actions
        self.add_toolbar_actions(actions)

    # This function adds all core actions to the menubar
    def add_core_actions(self):
        """
        Adds all core *GuiPy* actions to the top-level menubar, which are not
        related to any plugin or widget.

        """

        # Create dict of actions
        actions = {
            'File': [],
            'View': [],
            'Help': []}

        # FILE MENU
        # Add quit action to file menu
        quit_act = GW.QAction(
            self, '&Quit',
            shortcut=QG.QKeySequence.Quit,
            statustip="Quit %s" % (APP_NAME),
            triggered=self.close,
            role=GW.QAction.QuitRole)
        actions['File'].append(quit_act)

        # HELP MENU
        # Add about action to help menu
        about_act = GW.QAction(
            self, '&About...',
            statustip="About %s" % (APP_NAME),
            triggered=self.about,
            role=GW.QAction.AboutRole)
        actions['Help'].append(about_act)

        # Add aboutQt action to help menu
        aboutqt_act = GW.QAction(
            self, 'About &Qt...',
            statustip="About Qt framework",
            triggered=QW.QApplication.aboutQt,
            role=GW.QAction.AboutQtRole)
        actions['Help'].append(aboutqt_act)

        # Add all actions to the top-level menu
        self.add_menu_actions(actions)

    # This function adds all plugins to the main window
    def add_plugins(self):
        """
        Adds all plugins to the main window.

        """

        # Initialize empty dict with plugins
        self.plugins = {}

        # Initialize and add all the plugins
        self.add_plugin(GP.DataTable)
        self.add_plugin(GP.Figure)

    # This function adds a plugin to the main window
    def add_plugin(self, plugin_class, **kwargs):
        """
        Initializes a provided `plugin_class` using its requirements and the
        given `kwargs`, adds it as a plugin to this main window and returns it.
        If `plugin_class` is associated with a widget, it will be added as a
        dock widget to this main window as well.

        """

        # Obtain all the plugin requirements of the provided plugin_class
        req_plugins = {req: self.plugins.get(req)
                       for req in plugin_class.REQ_PLUGINS}

        # Initialize provided plugin_class
        plugin_obj = plugin_class(req_plugins=req_plugins, parent=self,
                                  **kwargs)

        # Add plugin_obj to dict of all current plugins
        self.plugins[plugin_obj.TITLE] = plugin_obj

        # Add all menu actions of this plugin_obj to the proper menus
        self.add_menu_actions(plugin_obj.MENU_ACTIONS)

        # Add all toolbars of this plugin_obj to the main window
        for toolbar in plugin_obj.TOOLBARS:
            self.addToolBar(toolbar)

        # Add all toolbar actions of this plugin_obj to the proper toolbars
        self.add_toolbar_actions(plugin_obj.TOOLBAR_ACTIONS)

        # Add all status widgets of this plugin_obj to the statusbar
        for widget in plugin_obj.STATUS_WIDGETS:
            self.statusbar.addPermanentWidget(widget)

        # Check if this plugin_obj is an instance of BasePluginWidget
        if isinstance(plugin_obj, GP.BasePluginWidget):
            # If so, add it as a dock widget as well
            self.add_dockwidget(plugin_obj)

        # Return the created plugin_obj
        return(plugin_obj)

    # This function adds a dock widget to the main window
    def add_dockwidget(self, plugin_obj):
        """
        Adds a provided `plugin_obj` as a dock widget to this main window.

        """

        # Create a dock widget object
        dock_widget = GW.BaseDockWidget(plugin_obj.TITLE, self)

        # Add provided plugin as a widget to it
        dock_widget.setWidget(plugin_obj)

        # Add dock_widget to the main window
        self.addDockWidget(plugin_obj.LOCATION, dock_widget)

        # Add action for toggling the dock widget
        self.add_menu_actions({'View/Docks': [dock_widget.toggleViewAction()]})

    # This function adds all actions defined in a dict to the proper menus
    def add_menu_actions(self, actions_dict):
        """
        Adds all menu actions defined in the provided `actions_dict` to the
        associated menus.

        Parameters
        ----------
        actions_dict : dict of lists
            Dict containing the actions that need to be added to what menu.

        Dict variables
        --------------
        keyword : str or None
            String specifying to which menu all associated actions should be
            added. If *None*, the actions are added to the top-level menubar
            instead.
        actions : list of {None; :obj:`~guipy.widgets.GW.QMenu`; str; \
                           :obj:`~PyQt5.QtWidgets.QAction`; \
                           :obj:`~PyQt5.QtCore.Slot`}
            A list containing all actions that must be added to the menu
            specified with `keyword`.
            If *None*, a separator is added.
            If :obj:`~guipy.widgets.GW.QMenu` object, the given menu is added
            and registered.
            If str, a section with the given name is added.
            If :obj:`~PyQt5.QtWidgets.QAction`, the given action is added.
            If :obj:`~PyQt5.QtCore.Slot`, the given slot is connected to the
            menu's action's :attr:`~PyQt5.QtWidgets.QAction.triggered` signal.

        """

        # Loop over all menus in actions_dict
        for menu_name, actions in actions_dict.items():
            # Obtain the corresponding menu
            if menu_name is None:
                menu = self.menuBar()
            else:
                menu = self.menus[menu_name]

            # Loop over all actions that must be added to this menu
            for action in actions:
                # If action is None, add a menu separator
                if action is None:
                    menu.addSeparator()
                # Else, if action is a menu, add a new menu
                elif isinstance(action, GW.QMenu):
                    self.addMenu(action, menu)
                # Else, if action is a string, add a new section
                elif isinstance(action, STR_TYPES):
                    menu.addSection(action)
                # Else, if action is an action, add a new action
                elif isinstance(action, QW.QAction):
                    menu.addAction(action)
                # Else, set provided function as the default action
                else:
                    menu.menuAction().triggered.connect(action)

    # This function adds all actions defined in a dict to the proper toolbars
    def add_toolbar_actions(self, actions_dict):
        """
        Adds all toolbar actions defined in the provided `actions_dict` to the
        associated toolbars.

        Parameters
        ----------
        actions_dict : dict of lists
            Dict containing the actions that need to be added to what toolbar.

        Dict variables
        --------------
        keyword : str
            String specifying to which toolbar all associated actions should be
            added.
        actions : list of {None; :obj:`~guipy.widgets.GW.QMenu`; \
                           :obj:`~PyQt5.QtWidgets.QWidget`; \
                           :obj:`~PyQt5.QtWidgets.QAction`}
            A list containing all actions that must be added to the toolbar
            specified with `keyword`.
            If *None*, a separator is added.
            If :obj:`~guipy.widgets.GW.QMenu` object, the action of the given
            menu is added.
            If :obj:`~PyQt5.QtWidgets.QWidget`, the given widget is added.
            If :obj:`~PyQt5.QtWidgets.QAction`, the given action is added.

        """

        # Loop over all toolbars in actions_dict
        for toolbar_name, actions in actions_dict.items():
            # Obtain the corresponding toolbar
            toolbar = self.toolbars[toolbar_name]

            # Loop over all actions that must be added to this toolbar
            for action in actions:
                # If action is None, add a toolbar separator
                if action is None:
                    toolbar.addSeparator()
                # Else, if action is a menu, add a new menu
                elif isinstance(action, GW.QMenu):
                    toolbar.addMenu(action)
                # Else, if action is a widget, add a new widget
                elif isinstance(action, QW.QWidget):
                    toolbar.addWidget(action)
                # Else, add the action to the toolbar
                else:
                    toolbar.addAction(action)

    # This function creates a message box with the 'about' information
    @QC.Slot()
    def about(self):
        """
        Displays a small section with information about the GUI.

        """

        # Make shortcuts for certain links
        github_repo = "https://github.com/1313e/GuiPy"

        # Create the text for the 'about' dialog
        text = dedent(r"""
            <b><a href="{github}">{name}</a> v{version}</b><br>
            Copyright &copy; 2019-2020 Ellert van der Velden<br>
            Distributed under the
            <a href="{github}/raw/master/LICENSE">BSD-3 License</a>.<br>
            <br>
            {os_name} {os_release} | Python {python_version} {memsize}-bit |
            Qt {Qt_version} | PyQt5 {PyQt5_version}
            """.format(name=APP_NAME,
                       version=__version__,
                       github=github_repo,
                       os_name=platform.system(),
                       os_release=platform.release(),
                       python_version=platform.python_version(),
                       memsize=calcsize('P')*8,
                       Qt_version=qtpy.QT_VERSION,
                       PyQt5_version=qtpy.PYQT_VERSION))

        # Create the 'about' dialog
        GW.QMessageBox.about(self, tr("About %s" % (APP_NAME)), tr(text))
