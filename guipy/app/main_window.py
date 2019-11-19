# -*- coding: utf-8 -*-

"""
Main Window
===========
Provides the definition of the main window of the *GuiPy* application.

"""


# %% IMPORTS
# Built-in imports
from textwrap import dedent

# Package imports
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy import __version__, APP_NAME
from guipy.plugins import DataTable
from guipy.widgets import BaseDockWidget, QW_QAction

# All declaration
__all__ = ['MainWindow']


# %% CLASS DEFINITIONS
# Define class for main window
class MainWindow(QW.QMainWindow):
    """
    Defines the :class:`~MainWindow` class for *GuiPy*.

    This class provides the main window for the GUI and combines all other
    widgets; layouts; and elements together.

    """

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

        # Make sure that the viewer is deleted when window is closed
        self.setAttribute(QC.Qt.WA_DeleteOnClose)

        # Set window title
        self.setWindowTitle(APP_NAME)

        # Disable the default context menu (right-click menu)
        self.setContextMenuPolicy(QC.Qt.NoContextMenu)

        # Initialize empty list with plugins
        self.plugin_list = []

        # Create statusbar
        self.create_statusbar()

        # Create menubar
        self.create_menubar()

        # Create toolbars
        self.create_toolbars()

        # Set resolution of window
        self.resize(800, 600)

        # Add all required plugins
        self.add_plugins()

        # Add all remaining core actions
        self.add_core_actions()

    # Override closeEvent to automatically close all plugins
    def closeEvent(self, *args, **kwargs):
        # Close all plugins in plugin_list
        for plugin in self.plugin_list:
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

    # This function creates the menubar in the viewer
    def create_menubar(self):
        """
        Creates the top-level menubar of the main window.

        Other widgets can modify this menubar to add additional actions to it.

        """

        # Make empty dict of menus
        self.menus = {}

        # Obtain menubar
        self.menubar = self.menuBar()

        # FILE
        # Create file menu
        file_menu = self.menubar.addMenu('&File')
        self.menus['File'] = file_menu

        # HELP
        # Create help menu
        help_menu = self.menubar.addMenu('&Help')
        self.menus['Help'] = help_menu

    # This function creates the toolbars in the viewer
    def create_toolbars(self):
        """
        Creates the toolbars of the main window.

        Other widgets can modify these toolbars to add additional actions to
        it.

        """

        # Make empty dict of toolbars
        self.toolbars = {}

        # FILE
        # Create file toolbar
        file_toolbar = self.addToolBar('File')
        self.toolbars['File'] = file_toolbar

    # This function adds all core actions to the menubar
    def add_core_actions(self):
        """
        Adds all core *GuiPy* actions to the top-level menubar, which are not
        related to any plugin or widget.

        """

        # Create dict of actions
        actions = {
            'File': [],
            'Help': []}

        # Add quit action to file menu
        quit_act = QW_QAction(
            self, '&Quit',
            shortcut=QG.QKeySequence.Quit,
            statustip="Quit %s" % (APP_NAME),
            triggered=self.close,
            role=QW_QAction.QuitRole)
        actions['File'].append(quit_act)

        # Add about action to help menu
        about_act = QW_QAction(
            self, '&About...',
            statustip="About %s" % (APP_NAME),
            triggered=self.about,
            role=QW_QAction.AboutRole)
        actions['Help'].append(about_act)

        # Add aboutQt action to help menu
        aboutqt_act = QW_QAction(
            self, 'About &Qt...',
            statustip="About Qt framework",
            triggered=QW.QApplication.aboutQt,
            role=QW_QAction.AboutQtRole)
        actions['Help'].append(aboutqt_act)

        # Add all actions to the top-level menu
        self.add_menu_actions(actions)

    # This function adds all plugins to the main window
    def add_plugins(self):
        """
        Adds all plugins to the main window.

        """

        # Create the DataTable plugin
        data_table = DataTable(self)
        self.add_dockwidget(data_table)

    # This function adds a dock widget to the main window
    def add_dockwidget(self, plugin):
        """
        Adds a provided `plugin` as a dock widget to this main window.

        """

        # Create a dock widget object
        dock_widget = BaseDockWidget(plugin.title, self)

        # Add provided plugin as a widget to it
        dock_widget.setWidget(plugin)

        # Add dock_widget to the main window
        self.addDockWidget(plugin.location, dock_widget)

        # Add plugin to list of all current plugins
        self.plugin_list.append(plugin)

        # Add all menu actions of this plugin to the proper menus
        self.add_menu_actions(plugin.menu_actions)

        # Add all toolbar actions of this plugin to the proper toolbars
        self.add_toolbar_actions(plugin.toolbar_actions)

    # This function adds all actions defined in a dict to the proper menus
    def add_menu_actions(self, actions_dict):
        """
        Adds all menu actions defined in the provided `actions_dict` to the
        associated menus.

        Parameters
        ----------
        actions_dict : dict of lists
            Dict containing the actions that need to be added to what menu.

        """

        # Loop over all menus in actions_dict
        for menu_name, actions in actions_dict.items():
            # Obtain the corresponding menu
            menu = self.menus[menu_name]

            # Loop over all actions that must be added to this menu
            for action in actions:
                # If action is None, add a menu separator
                if action is None:
                    menu.addSeparator()
                # Else, if action is a menu, add a new menu
                elif isinstance(action, QW.QMenu):
                    menu.addMenu(action)
                # Else, if action is a string, add a new section
                elif isinstance(action, str):
                    menu.addSection(action)
                # Else, add the action to the menu
                else:
                    menu.addAction(action)

            # Add a final separator
            menu.addSeparator()

    # This function adds all actions defined in a dict to the proper toolbars
    def add_toolbar_actions(self, actions_dict):
        """
        Adds all toolbar actions defined in the provided `actions_dict` to the
        associated toolbars.

        Parameters
        ----------
        actions_dict : dict of lists
            Dict containing the actions that need to be added to what toolbar.

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
            Copyright &copy; 2019 Ellert van der Velden<br>
            Distributed under the
            <a href="{github}/raw/master/LICENSE">BSD-3 License</a>.
            """.format(name=APP_NAME,
                       version=__version__,
                       github=github_repo))

        # Create the 'about' dialog
        QW.QMessageBox.about(self, "About %s" % (APP_NAME), text)
