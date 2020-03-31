# -*- coding: utf-8 -*-

"""
App Start
=========
Starts the *GuiPy* application.

"""


# %% IMPORTS
# Built-in imports
import signal

# Package imports
import matplotlib.pyplot as plt
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy import APP_NAME
from guipy.app.main_window import MainWindow

# All declaration
__all__ = ['main']


# %% MAIN FUNCTION
def main():
    """
    Prepares an :obj:`~PyQt5.QtWidgets.QApplication` instance and starts the
    *GuiPy* application.

    """

    # Obtain application instance
    qapp = QW.QApplication.instance()

    # If qapp is None, create a new one
    if qapp is None:
        QW.QApplication.setAttribute(QC.Qt.AA_EnableHighDpiScaling)
        qapp = QW.QApplication([APP_NAME])

    # Set name of application
    qapp.setApplicationName(APP_NAME)

    # Make sure that the application quits when last window closes
    qapp.lastWindowClosed.connect(qapp.quit, QC.Qt.QueuedConnection)

    # Initialize main window and draw (show) it
    main_window = MainWindow()
    main_window.show()
    main_window.raise_()
    main_window.activateWindow()

    # Replace KeyboardInterrupt error by system's default handler
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Set MPL's backend to 'Agg'
    plt.switch_backend('Agg')

    # Start application
    qapp.exec_()


# %% MAIN EXECUTION
if(__name__ == '__main__'):
    main()
