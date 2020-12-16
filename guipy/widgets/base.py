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

# All declaration
__all__ = ['QAbstractButton', 'QAction', 'QCheckBox', 'QComboBox', 'QDialog',
           'QDockWidget', 'QDoubleSpinBox', 'QFileDialog', 'QFontComboBox',
           'QGroupBox', 'QHeaderView', 'QLabel', 'QLineEdit', 'QListView',
           'QListWidget', 'QMainWindow', 'QMenu', 'QMessageBox', 'QPushButton',
           'QRadioButton', 'QSpinBox', 'QSplitter', 'QScrollArea',
           'QStackedWidget', 'QTabBar', 'QTableView', 'QTabWidget',
           'QTextEdit', 'QToolBar', 'QToolButton', 'QToolTip', 'QWidget']


# %% BASE CLASS DEFINITION
# Make subclass of QWidget to provide certain functionality to all widgets
class QWidget(QW.QWidget):
    """
    Defines the :class:`~QWidget` class.

    This class provides default settings and extra options for the
    :class:`~PyQt5.QtWidgets.QWidget` class and is inherited by all other
    custom :class:`~PyQt5.QtWidgets.QWidget` classes.

    """

    # Initialize QWidget
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(*args, **kwargs)

        # Retrieve certain methods from parent
        self.get_parent_methods()

    # This function retrieves a set of methods from the parent if possible
    def get_parent_methods(self):
        # Obtain parent widget
        parent = self.parentWidget()

        # If this widget has a parent, retrieve a few methods if possible
        if parent is not None:
            # Retrieve the 'get_option' method if it exists
            if(not hasattr(self, 'get_option') and
               hasattr(parent, 'get_option')):
                self.get_option = parent.get_option

    # Override setStatusTip to auto translate
    def setStatusTip(self, text):
        super().setStatusTip(text)

    # Override setToolTip to auto translate
    def setToolTip(self, text):
        super().setToolTip(text)

    # Override childEvent to add 'get_option' if it exists to all children
    def childEvent(self, event):
        """
        Special :meth:`~PyQt5.QtCore.QObject.childEvent` event that
        automatically calls the :meth:`~get_parent_methods` method on any
        widget that becomes a child of this widget.

        """

        # If this event involved a child being added, check child object
        if(event.type() == QC.QEvent.ChildAdded):
            # Obtain child object
            child = event.child()

            # If this child has the 'get_parent_methods' method, call it
            if hasattr(child, 'get_parent_methods'):
                child.get_parent_methods()

        # Call and return super method
        return(super().childEvent(event))

    # Override setLocale to also set it for all children
    def setLocale(self, locale):
        # Set locale for this object
        super().setLocale(locale)

        # Also set this locale for all children that are widgets
        for child in self.children():
            if isinstance(child, QWidget):
                child.setLocale(locale)


# %% CLASS DEFINITIONS
# Create custom QAbstractButton
class QAbstractButton(QW.QAbstractButton, QWidget):
    # Override constructor to set some default settings
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(*args, **kwargs)

        # Use default settings
        self.setSizePolicy(QW.QSizePolicy.Fixed, QW.QSizePolicy.Fixed)


# Make subclass of QW.QAction that automatically sets details based on status
class QAction(QW.QAction):
    """
    Defines the :class:`~QAction` class.

    This class provides default settings and extra options for the
    :class:`~PyQt5.QtWidgets.QAction` class.

    """

    # Override constructor
    def __init__(self, parent, text, *, shortcut=None, tooltip=None,
                 statustip=None, icon=None, triggered=None, toggled=None,
                 role=None):
        """
        Initializes the :class:`~QAction` class.

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
            If *None*, no slot will be connected to this action's `triggered`
            signal.
        toggled : function or None. Default: None
            The Qt slot function that must be called whenever this action is
            toggled.
            If *None*, no slot will be connected to this action's `toggled`
            signal.
        role : :obj:`~PyQt5.QtWidgets.QAction.MenuRole` object or None. \
            Default: None
            The menu role that must be set as the role of this action.
            If *None*, it is set to :obj:`~PyQt5.QtWidgets.NoRole`.

        """

        # Call super constructor
        if icon is None:
            super().__init__(text, parent)
        else:
            super().__init__(icon, text, parent)

        # Set all the details
        self.setDetails(shortcut=shortcut,
                        tooltip=tooltip,
                        statustip=statustip)

        # Set the triggered signal
        if triggered is not None:
            self.triggered.connect(triggered)

        # Set the toggled signal
        if toggled is not None:
            self.toggled.connect(toggled)
            self.setCheckable(True)

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


# Create custom QCheckBox
class QCheckBox(QW.QCheckBox, QAbstractButton):
    pass


# Create custom combobox class with more signals
class QComboBox(QW.QComboBox, QWidget):
    """
    Defines the :class:`~QComboBox` class.

    This class provides default settings and extra options for the
    :class:`~PyQt5.QtWidgets.QComboBox` class.

    """

    # Signals
    popup_shown = QC.Signal([int], [str])
    popup_hidden = QC.Signal([int], [str])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizeAdjustPolicy(self.AdjustToContents)

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


# Create custom QFontComboBox class
class QFontComboBox(QW.QFontComboBox, QWidget):
    # Signals
    popup_shown = QC.Signal([int], [str])
    popup_hidden = QC.Signal([int], [str])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizeAdjustPolicy(self.AdjustToContents)

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


# Create custom QDialog
class QDialog(QW.QDialog, QWidget):
    pass


# Create custom QDockWidget
# TODO: Add a context menu button to all dockwidgets by default?
class QDockWidget(QW.QDockWidget, QWidget):
    pass


# Create custom QFileDialog class
class QFileDialog(QW.QFileDialog, QDialog):
    pass


# Create custom QGroupBox class
class QGroupBox(QW.QGroupBox, QWidget):
    pass


# Create custom QHeaderView class
class QHeaderView(QW.QHeaderView, QWidget):
    pass


# Create custom QAbstractSpinBox that automatically sets some properties
class QAbstractSpinBox(QW.QAbstractSpinBox, QWidget):
    """
    Defines the :class:`~QAbstractSpinBox` class.

    This class provides default settings and extra options for the
    :class:`~PyQt5.QtWidgets.QAbstractSpinBox` class.

    """

    # Override constructor to set some default settings
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(*args, **kwargs)

        # Use default settings
        self.setStepType(self.AdaptiveDecimalStepType)
        self.setAccelerated(True)
        self.setGroupSeparatorShown(True)
        self.setStyleSheet(
            """
            QAbstractSpinBox {{
                margin: {0}px 0px {0}px 0px;
                max-height: 24px;}}
            """.format("-1" if platform.startswith('linux') else '0'))

    # Auto translate any special value text that is set
    def setSpecialValueText(self, text):
        super().setSpecialValueText(text)


# Create custom QDoubleSpinBox
class QDoubleSpinBox(QW.QDoubleSpinBox, QAbstractSpinBox):
    pass


# Create custom QSpinBox
class QSpinBox(QW.QSpinBox, QAbstractSpinBox):
    pass


# Create custom QLabel class with more signals
class QLabel(QW.QLabel, QWidget):
    """
    Defines the :class:`~QLabel` class.

    This class provides default settings and extra options for the
    :class:`~PyQt5.QtWidgets.QLabel` class.

    """

    # Signals
    contentsChanged = QC.Signal([str], [QG.QMovie], [QG.QPicture],
                                [QG.QPixmap])
    mousePressed = QC.Signal()

    def __init__(self, text=None, *args, **kwargs):
        # Call super constructor
        if text is None:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(text, *args, **kwargs)

        # Set some settings
        self.setWordWrap(True)
        self.setOpenExternalLinks(True)

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
        super().setText(text)
        self.contentsChanged[str].emit(self.text())


# Create custom QLineEdit class
class QLineEdit(QW.QLineEdit, QWidget):
    pass


# Create custom QListView class
class QListView(QW.QListView, QWidget):
    pass


# Create custom QListWidget class
class QListWidget(QW.QListWidget, QWidget):
    pass


# Create custom QMainWindow class
class QMainWindow(QW.QMainWindow, QWidget):
    pass


# Create custom QMenu class
class QMenu(QW.QMenu, QWidget):
    """
    Defines the :class:`~QMenu` class.

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
        super().__init__(title, parent)

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
        # Call super method
        if icon is None:
            return(super().addSection(text))
        else:
            return(super().addSection(icon, text))


# Create custom QMessageBox class
class QMessageBox(QW.QMessageBox, QDialog):
    pass


# Create custom QPushButton class
class QPushButton(QW.QPushButton, QAbstractButton):
    pass


# Create custom QRadioButton class
class QRadioButton(QW.QRadioButton, QAbstractButton):
    pass


# Create custom QScrollArea class
class QScrollArea(QW.QScrollArea, QWidget):
    pass


# Create custom QSplitter class
class QSplitter(QW.QSplitter, QWidget):
    pass


# Create custom QStackedWidget class
class QStackedWidget(QW.QStackedWidget, QWidget):
    pass


# Create custom QTabBar class
class QTabBar(QW.QTabBar, QWidget):
    # Signals
    tabTextChanged = QC.Signal(int, str)

    # Override constructor to set some default settings
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(*args, **kwargs)

        # Use default settings
        self.setElideMode(QC.Qt.ElideNone)

    # Override setTabText to emit a signal whenever it is called
    def setTabText(self, index, text):
        # Emit signal
        self.tabTextChanged.emit(index, text)

        # Call super method
        return(super().setTabText(index, text))


# Create custom QTableView class
class QTableView(QW.QTableView, QWidget):
    pass


# Create custom QTabWidget class
class QTabWidget(QW.QTabWidget, QWidget):
    """
    Defines the :class:`~QTabWidget` class.

    This class provides default settings and extra options for the
    :class:`~PyQt5.QtWidgets.QTabWidget` class.

    """

    # Signals
    currentIndexChanged = QC.Signal(int)
    currentTextChanged = QC.Signal(str)
    currentWidgetChanged = QC.Signal(QW.QWidget)
    tabTextChanged = QC.Signal(int, str)
    tabWasInserted = QC.Signal([int], [int, str], [int, QW.QWidget])
    tabWasRemoved = QC.Signal(int)

    # Override constructor to connect some signals
    def __init__(self, *args, browse_tabs=False, **kwargs):
        # Call super constructor
        super().__init__(*args, **kwargs)

        # Set up the tab widget
        self.init(browse_tabs)

    # This function sets up the tab widget
    def init(self, browse_tabs):
        # Set default tabbar
        self.setTabBar(QTabBar())

        # Connect signals
        self.currentChanged.connect(self.currentIndexChanged)
        self.currentChanged.connect(
            lambda index: self.currentTextChanged.emit(self.tabText(index)))
        self.currentChanged.connect(
            lambda index: self.currentWidgetChanged.emit(self.widget(index)))

        # Check if a browse menu was requested
        if browse_tabs:
            # Create a menu containing all available tabs
            browse_menu = QMenu('Browse', parent=self)
            browse_menu.aboutToShow.connect(self.update_browse_menu)
            self.browse_menu = browse_menu

            # Create a toolbutton for browsing all available tabs
            browse_but = QToolButton()
            browse_but.setText('V')
            browse_but.setToolTip("Browse tabs")
            browse_but.setMenu(browse_menu)
            browse_but.setPopupMode(browse_but.InstantPopup)
            self.browse_but = browse_but

            # Set browse button as the left corner widget
            self.setCornerWidget(browse_but, QC.Qt.TopLeftCorner)

    # This function updates the browse menu
    def update_browse_menu(self):
        """
        Updates the browse menu that shows all available tabs.

        """

        # Remove all actions currently in the browse menu
        self.browse_menu.clear()

        # Loop over all available tabs
        for i, name in enumerate(self.tabNames()):
            # Create a toggleable action for this tab
            tab_act = QAction(
                self, name,
                icon=self.tabIcon(i),
                tooltip=self.tabToolTip(i),
                toggled=lambda *args, index=i: self.setCurrentIndex(index))

            # If this tab is currently selected, check it
            tab_act.setChecked(self.currentIndex() == i)

            # Add action to menu
            self.browse_menu.addAction(tab_act)

    # Override addTab to automatically translate the given tab name
    def addTab(self, widget, label, icon=None):
        # Call super method
        if icon is None:
            return(super().addTab(widget, label))
        else:
            return(super().addTab(widget, icon, label))

    # Override setTabBar to automatically connect some signals
    def setTabBar(self, tabbar):
        # Connect the tabTextChanged signals
        tabbar.tabTextChanged.connect(self.tabTextChanged)

        # Call super method
        return(super().setTabBar(tabbar))

    # Override tabInserted to emit a signal whenever it is called
    def tabInserted(self, index):
        # Emit tabWasInserted signal
        self.tabWasInserted[int].emit(index)
        self.tabWasInserted[int, str].emit(index, self.tabText(index))
        self.tabWasInserted[int, QW.QWidget].emit(index, self.widget(index))

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

    # Define function that returns a list of all tab widgets
    def tabWidgets(self):
        return(list(map(self.widget, range(self.count()))))


# Create custom QTextEdit class
class QTextEdit(QW.QTextEdit, QWidget):
    pass


# Create custom QToolbar class
class QToolBar(QW.QToolBar, QWidget):
    """
    Defines the :class:`~QToolBar` class.

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
        super().__init__(title, parent)

    # This function retrieves the action of a menu and adds it to the toolbar
    def addMenu(self, menu):
        # Obtain the action associated with this menu
        action = menu.menuAction()

        # Add this action
        self.addAction(action)


# Create custom QToolButton class
class QToolButton(QW.QToolButton, QAbstractButton):
    # Override constructor to set some default settings
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(*args, **kwargs)

        # Use default settings
        self.setAutoRaise(True)


# Create custom QToolTip class
class QToolTip(QW.QToolTip):
    pass
