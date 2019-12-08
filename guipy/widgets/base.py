# -*- coding: utf-8 -*-

"""
Base Widgets
============
Provides a collection of custom :class:`~PyQt5.QtWidgets.QWidget` base classes
that allow for certain widgets to be standardized.

"""


# %% IMPORTS
# Built-in imports
from sys import platform

# Package imports
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy.config import tr

# All declaration
__all__ = ['QW_QAction', 'QW_QComboBox', 'QW_QDialog', 'QW_QDockWidget',
           'QW_QDoubleSpinBox', 'QW_QEditableComboBox', 'QW_QFileDialog',
           'QW_QHeaderView', 'QW_QLabel', 'QW_QLineEdit', 'QW_QMainWindow',
           'QW_QMenu', 'QW_QMessageBox', 'QW_QPushButton', 'QW_QSpinBox',
           'QW_QTabBar', 'QW_QTableView', 'QW_QTabWidget', 'QW_QTextEdit',
           'QW_QToolBar', 'QW_QToolTip', 'QW_QWidget']


# %% BASE CLASS DEFINITION
# Make subclass of QWidget to provide certain functionality to all widgets
class QW_QWidget(QW.QWidget):
    """
    Defines the :class:`~QW_QWidget` class.

    This class provides default settings and extra options for the
    :class:`~PyQt5.QtWidgets.QWidget` class and is inherited by all other
    custom :class:`~PyQt5.QtWidgets.QWidget` classes.

    """

    # Override setStatusTip to auto translate
    def setStatusTip(self, text):
        super().setStatusTip(tr(text))

    # Override setToolTip to auto translate
    def setToolTip(self, text):
        super().setToolTip(tr(text))


# %% CLASS DEFINITIONS
# Make subclass of QW.QAction that automatically sets details based on status
class QW_QAction(QW.QAction):
    """
    Defines the :class:`~QW_QAction` class.

    This class provides default settings and extra options for the
    :class:`~PyQt5.QtWidgets.QAction` class.

    """

    # Override constructor
    def __init__(self, parent, text, *, shortcut=None, tooltip=None,
                 statustip=None, icon=None, triggered=None, role=None):
        """
        Initializes the :class:`~QW_QAction` class.

        Parameters
        ----------
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None
            The parent widget for this dialog or *None* for no parent.
        text : str
            The label that this action must have.

        Optional
        --------
        shortcut : :obj:`~PyQt5.QtGui.QKeySequence` or None. Default: None
            The key sequence that must be set as the shortcut for this action.
            If *None*, no shortcut will be set.
        tooltip : str or None. Default: None
            The text that must be set as the tooltip for this action.
            If *None*, the tooltip is set to `text`.
            If `shortcut` is not *None*, the tooltip will also include the
            shortcut.
        statustip : str or None. Default: None
            The text that must be set as the statustip for this action.
            If *None*, the statustip is set to `tooltip`.
        icon : :obj:`~PyQt5.QtGui.QIcon` object or None. Default: None
            The icon that must be set as the icon for this action.
            If *None*, no icon will be set.
        triggered : function or None. Default: None
            The Qt slot function that must be called whenever this action is
            triggered.
            If *None*, no slot will connected to this action's signal.
        role : :obj:`~PyQt5.QtWidgets.QAction.MenuRole` object or None. \
            Default: None
            The menu role that must be set as the role of this action.
            If *None*, it is set to :obj:`~PyQt5.QtWidgets.NoRole`.

        """

        # Translate text
        text = tr(text)

        # Call super constructor
        if icon is None:
            super().__init__(text, parent)
        else:
            super().__init__(icon, text, parent)

        # Set all the details
        self.setDetails(shortcut=shortcut,
                        tooltip=tooltip,
                        statustip=statustip)

        # Set the signal trigger
        if triggered is not None:
            self.triggered.connect(triggered)

        # Set the action menu role
        self.setMenuRole(self.NoRole if role is None else role)

    # Make new method that automatically sets Shortcut, ToolTip and StatusTip
    def setDetails(self, *, shortcut=None, tooltip=None, statustip=None):
        """
        Uses the provided `shortcut`; `tooltip`; and `statustip` to set the
        details of this action.

        Parameters
        ----------
        shortcut : :obj:`~PyQt5.QtGui.QKeySequence` or None. Default: None
            The key sequence that must be set as the shortcut for this action.
            If *None*, no shortcut will be set.
        tooltip : str or None. Default: None
            The text that must be set as the tooltip for this action.
            If *None*, the tooltip is set to `text`.
            If `shortcut` is not *None*, the tooltip will also include the
            shortcut.
        statustip : str or None. Default: None
            The text that must be set as the statustip for this action.
            If *None*, the statustip is set to `tooltip`.

        """

        # Translate tooltip and statustip
        tooltip = tr(tooltip) if tooltip is not None else None
        statustip = tr(statustip) if statustip is not None else None

        # If shortcut is not None, set it
        if shortcut is not None:
            super().setShortcut(shortcut)
            shortcut = self.shortcut().toString()

        # If tooltip is None, its base is set to the action's name
        if tooltip is None:
            base_tooltip = self.text().replace('&', '')
            tooltip = base_tooltip
        # Else, provided tooltip is used as the base
        else:
            base_tooltip = tooltip

        # If shortcut is not None, add it to the tooltip
        if shortcut is not None:
            tooltip = "%s (%s)" % (base_tooltip, shortcut)

        # Set tooltip
        super().setToolTip(tooltip)

        # If statustip is None, it is set to base_tooltip
        if statustip is None:
            statustip = base_tooltip

        # Set statustip
        super().setStatusTip(statustip)

    # Override setShortcut to raise an error when used
    def setShortcut(self, *args, **kwargs):
        raise AttributeError("Using this method is not allowed! Use "
                             "'setDetails()' instead!")

    # Override setToolTip to raise an error when used
    def setToolTip(self, *args, **kwargs):
        raise AttributeError("Using this method is not allowed! Use "
                             "'setDetails()' instead!")

    # Override setStatusTip to raise an error when used
    def setStatusTip(self, *args, **kwargs):
        raise AttributeError("Using this method is not allowed! Use "
                             "'setDetails()' instead!")


# Create custom combobox class with more signals
class QW_QComboBox(QW.QComboBox, QW_QWidget):
    """
    Defines the :class:`~QW_QComboBox` class.

    This class provides default settings and extra options for the
    :class:`~PyQt5.QtWidgets.QComboBox` class.

    """

    # Signals
    popup_shown = QC.Signal([int], [str])
    popup_hidden = QC.Signal([int], [str])

    # Override the showPopup to emit a signal whenever it is triggered
    def showPopup(self, *args, **kwargs):
        self.popup_shown[int].emit(self.currentIndex())
        self.popup_shown[str].emit(self.currentText())
        return(super().showPopup(*args, **kwargs))

    # Override the hidePopup to emit a signal whenever it is triggered.
    def hidePopup(self, *args, **kwargs):
        self.popup_hidden[int].emit(self.currentIndex())
        self.popup_hidden[str].emit(self.currentText())
        return(super().hidePopup(*args, **kwargs))


# Create custom QComboBox class that is editable
class QW_QEditableComboBox(QW_QComboBox):
    """
    Defines the :class:`~QW_QEditableComboBox` class.

    This class makes the :class:`~QW_QComboBox` class editable.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setEditable(True)
        self.setInsertPolicy(self.NoInsert)
        self.completer().setCompletionMode(QW.QCompleter.PopupCompletion)
        self.completer().setFilterMode(QC.Qt.MatchContains)


# Create custom QDialog
class QW_QDialog(QW.QDialog, QW_QWidget):
    pass


# Create custom QDockWidget
class QW_QDockWidget(QW.QDockWidget, QW_QWidget):
    pass


# Create custom QFileDialog class
class QW_QFileDialog(QW.QFileDialog, QW_QDialog):
    pass


# Create custom QHeaderView class
class QW_QHeaderView(QW.QHeaderView, QW_QWidget):
    pass


# Create custom QAbstractSpinBox that automatically sets some properties
class QW_QAbstractSpinBox(QW.QAbstractSpinBox, QW_QWidget):
    """
    Defines the :class:`~QW_QAbstractSpinBox` class.

    This class provides default settings and extra options for the
    :class:`~PyQt5.QtWidgets.QAbstractSpinBox` class.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStepType(self.AdaptiveDecimalStepType)
        self.setAccelerated(True)
        self.setGroupSeparatorShown(True)
        self.setStyleSheet(
            """
            QAbstractSpinBox {{
                margin: {0}px 0px {0}px 0px;
                max-height: 24px;}}
            """.format("-1" if platform.startswith('linux') else '0'))


# Create custom QDoubleSpinBox
class QW_QDoubleSpinBox(QW.QDoubleSpinBox, QW_QAbstractSpinBox):
    pass


# Create custom QSpinBox
class QW_QSpinBox(QW.QSpinBox, QW_QAbstractSpinBox):
    pass


# Create custom QLabel class with more signals
class QW_QLabel(QW.QLabel, QW_QWidget):
    """
    Defines the :class:`~QW_QLabel` class.

    This class provides default settings and extra options for the
    :class:`~PyQt5.QtWidgets.QLabel` class.

    """

    # Signals
    contentsChanged = QC.Signal([str], [QG.QMovie], [QG.QPicture],
                                [QG.QPixmap])
    mousePressed = QC.Signal()

    def __init__(self, text=None, *args, **kwargs):
        # Translate text
        text = tr(text) if text is not None else None

        # Call super constructor
        if text is None:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(text, *args, **kwargs)

    # Override the mousePressEvent to emit a signal whenever it is triggered
    def mousePressEvent(self, event):
        self.mousePressed.emit()
        event.accept()

    # Override setMovie to emit a signal whenever it is called
    def setMovie(self, movie):
        super().setMovie(movie)
        self.contentsChanged[QG.QMovie].emit(self.movie())

    # Override setNum to emit a signal whenever it is called
    def setNum(self, num):
        super().setNum(num)
        self.contentsChanged[str].emit(self.text())

    # Override setPicture to emit a signal whenever it is called
    def setPicture(self, picture):
        super().setPicture(picture)
        self.contentsChanged[QG.QPicture].emit(self.picture())

    # Override setPixmap to emit a signal whenever it is called
    def setPixmap(self, pixmap):
        super().setPixmap(pixmap)
        self.contentsChanged[QG.QPixmap].emit(self.pixmap())

    # Override setText to emit a signal whenever it is called
    def setText(self, text):
        super().setText(tr(text))
        self.contentsChanged[str].emit(self.text())


# Create custom QLineEdit class
class QW_QLineEdit(QW.QLineEdit, QW_QWidget):
    pass


# Create custom QMainWindow class
class QW_QMainWindow(QW.QMainWindow, QW_QWidget):
    pass


# Create custom QMenu class
class QW_QMenu(QW.QMenu, QW_QWidget):
    """
    Defines the :class:`~QW_QMenu` class.

    This class provides default settings and extra options for the
    :class:`~PyQt5.QtWidgets.QMenu` class.

    """

    def __init__(self, name, title=None, parent=None, *, tooltip=None,
                 statustip=None):
        # Save name
        self.name = name

        # If title is None, set it to name
        if title is None:
            title = name

        # Call super constructor
        super().__init__(tr(title), parent)

        # Set all the details
        self.setDetails(tooltip=tooltip,
                        statustip=statustip)

    # Make new method that automatically sets ToolTip and StatusTip
    def setDetails(self, *, tooltip=None, statustip=None):
        """
        Uses the provided `tooltip` and `statustip` to set the details of this
        menu action.

        Parameters
        ----------
        tooltip : str or None. Default: None
            The text that must be set as the tooltip for this menu.
            If *None*, the tooltip is set to `title`.
        statustip : str or None. Default: None
            The text that must be set as the statustip for this menu.
            If *None*, the statustip is set to `tooltip`.

        """

        # Obtain the action that triggers this menu
        menu_action = self.menuAction()

        # Translate tooltip and statustip
        tooltip = tr(tooltip) if tooltip is not None else None
        statustip = tr(statustip) if statustip is not None else None

        # If tooltip is None, it is set to the menu's name
        if tooltip is None:
            tooltip = self.title().replace('&', '')

        # Set tooltip
        menu_action.setToolTip(tooltip)

        # If statustip is None, it is set to tooltip
        if statustip is None:
            statustip = tooltip

        # Set statustip
        menu_action.setStatusTip(statustip)

    # Override setToolTip to raise an error when used
    def setToolTip(self, *args, **kwargs):
        raise AttributeError("Using this method is not allowed! Use "
                             "'setDetails()' instead!")

    # Override setStatusTip to raise an error when used
    def setStatusTip(self, *args, **kwargs):
        raise AttributeError("Using this method is not allowed! Use "
                             "'setDetails()' instead!")

    # Override addSection to automatically translate the given section name
    def addSection(self, text, icon=None):
        # Translate text
        text = tr(text)

        # Call super method
        if icon is None:
            return(super().addSection(text))
        else:
            return(super().addSection(icon, text))


# Create custom QMessageBox class
class QW_QMessageBox(QW.QMessageBox, QW_QDialog):
    pass


# Create custom QPushButton class
class QW_QPushButton(QW.QPushButton, QW_QWidget):
    pass


# Create custom QTabBar class
class QW_QTabBar(QW.QTabBar, QW_QWidget):
    # Signals
    tabNameChanged = QC.Signal([int, str])

    # Override setTabText to emit a signal whenever it is called
    def setTabText(self, index, name):
        # Emit signal
        self.tabNameChanged.emit(index, name)

        # Call super method
        return(super().setTabText(index, name))


# Create custom QTableView class
class QW_QTableView(QW.QTableView, QW_QWidget):
    pass


# Create custom QTabWidget class
class QW_QTabWidget(QW.QTabWidget, QW_QWidget):
    """
    Defines the :class:`~QW_QTabWidget` class.

    This class provides default settings and extra options for the
    :class:`~PyQt5.QtWidgets.QTabWidget` class.

    """

    # Signals
    tabNameChanged = QC.Signal([int, str])
    tabWasInserted = QC.Signal([int], [int, str])
    tabWasRemoved = QC.Signal([int])

    # Override addTab to automatically translate the given tab name
    def addTab(self, widget, label, icon=None):
        # Translate text
        label = tr(label)

        # Call super method
        if icon is None:
            return(super().addTab(widget, label))
        else:
            return(super().addTab(widget, icon, label))

    # Override setTabBar to automatically connect some signals
    def setTabBar(self, tabbar):
        # Connect the tabNameChanged signals
        tabbar.tabNameChanged.connect(self.tabNameChanged)

        # Call super method
        return(super().setTabBar(tabbar))

    # Override tabInserted to emit a signal whenever it is called
    def tabInserted(self, index):
        # Emit tabWasInserted signal
        self.tabWasInserted[int].emit(index)
        self.tabWasInserted[int, str].emit(index, self.tabText(index))

        # Call super method
        super().tabInserted(index)

    # Override tabRemoved to emit a signal whenever it is called
    def tabRemoved(self, index):
        # Emit tabWasRemoved signal
        self.tabWasRemoved.emit(index)

        # Call super method
        super().tabRemoved(index)

    # Define function that returns a list of all tab names
    def tabNames(self):
        return(list(map(self.tabText, range(self.count()))))


# Create custom QTextEdit class
class QW_QTextEdit(QW.QTextEdit, QW_QWidget):
    pass


# Create custom QToolbar class
class QW_QToolBar(QW.QToolBar, QW_QWidget):
    """
    Defines the :class:`~QW_QToolBar` class.

    This class provides default settings and extra options for the
    :class:`~PyQt5.QtWidgets.QToolBar` class.

    """

    def __init__(self, name, title=None, parent=None):
        # Save name
        self.name = name

        # If title is None, set it to name
        if title is None:
            title = name

        # Call super constructor
        super().__init__(tr(title), parent)

    # This function retrieves the action of a menu and adds it to the toolbar
    def addMenu(self, menu):
        # Obtain the action associated with this menu
        action = menu.menuAction()

        # Add this action
        self.addAction(action)


# Create custom QToolTip class
class QW_QToolTip(QW.QToolTip):
    pass
