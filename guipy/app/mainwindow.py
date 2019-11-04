# -*- coding: utf-8 -*-

"""
Main
====


"""


# % IMPORTS
# Built-in imports


# Package imports
from PyQt5 import QtCore as QC, QtWidgets as QW

# <THIS PACKAGE> imports


# All declaration
__all__ = ['MainWindow']


# % GLOBALS



# % CLASS DEFINITIONS
# Define class for main window
class MainWindow(QW.QMainWindow):
    def __init__(self, *args, **kwargs):
        """
        Initialize an instance of the :class:`~MainViewerWindow` class.

        """

        # Call super constructor
        super().__init__(*args, **kwargs)

        # Set up the main window
        self.init()

    # This function sets up the main window
    def init(self):
        # Make sure that the viewer is deleted when window is closed
        self.setAttribute(QC.Qt.WA_DeleteOnClose)

        # Make a central widget
        self.main_widget = QW.QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Make a layout for the mainwindow
        layout = QW.QHBoxLayout(self.main_widget)

        # Make a button
        button = QW.QPushButton("Pointless button")
        layout.addWidget(button)
