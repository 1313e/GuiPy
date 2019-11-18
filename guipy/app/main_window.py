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
        self.menubar.setFocus()

        # Set resolution of window
        self.resize(800, 600)

        # Add all required plugins
        self.add_plugins()

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

        # Obtain menubar
        self.menubar = self.menuBar()

        # FILE
        # Create file menu
        file_menu = self.menubar.addMenu('&File')

        # Add quit action to menu
        quit_act = QW_QAction(
            self, '&Quit',
            shortcut=QG.QKeySequence.Quit,
            statustip="Quit %s" % (APP_NAME),
            triggered=self.close,
            role=QW_QAction.QuitRole)
        file_menu.addAction(quit_act)

        # HELP
        # Create help menu
        help_menu = self.menubar.addMenu('&Help')

        # Add about action to help menu
        about_act = QW_QAction(
            self, '&About...',
            statustip="About %s" % (APP_NAME),
            triggered=self.about,
            role=QW_QAction.AboutRole)
        help_menu.addAction(about_act)

        # Add aboutQt action to help menu
        aboutqt_act = QW_QAction(
            self, 'About &Qt...',
            statustip="About Qt framework",
            triggered=QW.QApplication.aboutQt,
            role=QW_QAction.AboutQtRole)
        help_menu.addAction(aboutqt_act)

    # This function adds all plugins to the main window
    def add_plugins(self):
        """
        Add all plugins to the main window.

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
