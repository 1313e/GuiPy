# -*- coding: utf-8 -*-

"""
ItemsBoxes
==========

"""


# %% IMPORTS
# Built-in imports


# Package imports
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy import layouts as GL, widgets as GW
from guipy.widgets import get_box_value, get_modified_signal, set_box_value

# All declaration
__all__ = ['ItemsBox']


# %% CLASS DEFINITIONS
# Make class for creating item lists
class ItemsBox(GW.BaseBox):
    """
    Defines the :class:`~ItemsBox` class.

    This widget allows for a series of 'list' items to be maintained within a
    single box, and is basically a Qt-version of a Python list.

    """

    # Signals
    modified = QC.Signal([], [list])

    # Initialize the ItemsBox class
    def __init__(self, types=None, parent=None):
        """
        Initialize an instance of the :class:`~ItemsBox` class.

        Optional
        --------
        types : tuple of types ({bool; float; int; str; dict; list}) or None. \
            Default: None
            A tuple containing the type of each item in the items box.
            If *None*, this items box instead has no pre-defined number of
            items.
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
            The parent widget to use for this items box or *None* for no
            parent.

        """

        # Call super constructor
        super().__init__(parent, auto_connect=False)

        # Create the entries box
        self.init(types)

    # This property returns the default 'modified' signal
    @property
    def default_modified_signal(self):
        return(self.modified[list])

    # This property returns the number of items in the box
    def itemCount(self):
        return(self.items_layout.rowCount())

    # This function creates the items box
    def init(self, types):
        """
        Sets up the items box after it has been initialized.

        """

        # Set the height of a single entry
        self.entry_height = 24

        # Create empty list of items
        self.items = []

        # Create the box_layout
        box_layout = GL.QVBoxLayout(self)
        box_layout.setContentsMargins(0, 0, 0, 0)

        # Create the items_layout
        items_layout = GL.QFormLayout(self)
        items_layout.setContentsMargins(0, 0, 0, 0)
        box_layout.addLayout(items_layout)
        self.items_layout = items_layout

        # Add an 'Add'-button
        add_but = GW.QToolButton()
        add_but.setFixedSize(self.entry_height, self.entry_height)
        add_but.setToolTip("Add new item")
        get_modified_signal(add_but).connect(self.add_item)
        box_layout.addWidget(add_but)

        # If this theme has an 'add' icon, use it
        if QG.QIcon.hasThemeIcon('add'):
            add_but.setIcon(QG.QIcon.fromTheme('add'))
        # Else, use a simple plus
        else:
            add_but.setText('+')

        # Add a stretch
        box_layout.addStretch()

    # This function is automatically called whenever 'modified' is emitted
    @QC.Slot()
    def modified_signal_slot(self):
        self.modified[list].emit(ItemsBox.get_box_value(self))

    # This function is called whenever a new item is added
    @QC.Slot()
    def add_item(self):
        """
        Adds a new item to the items box.

        """

        # Create an item layout
        item_layout = GL.QHBoxLayout()
        item_layout.setContentsMargins(0, 0, 0, 0)

        # Create a generic box for this item
        item_box = GW.GenericBox()
        item_box.setToolTip("Set value of this item")
        get_modified_signal(item_box).connect(self.modified)

        # Create a 'Delete'-button
        del_but = GW.QToolButton()
        del_but.setFixedSize(self.entry_height, self.entry_height)
        del_but.setToolTip("Delete this item")
        get_modified_signal(del_but).connect(
            lambda: self.remove_item(item_layout))

        # If this theme has a 'remove' icon, use it
        if QG.QIcon.hasThemeIcon('remove'):
            del_but.setIcon(QG.QIcon.fromTheme('remove'))
        # Else, use a standard icon
        else:
            del_but.setIcon(del_but.style().standardIcon(
                QW.QStyle.SP_DialogCloseButton))

        # Add a new row to the items layout
        item_layout.addWidget(del_but)
        item_layout.addWidget(item_box)
        self.items_layout.addRow(item_layout)

    # This function is called whenever an item must be removed
    @QC.Slot(GW.QComboBox)
    def remove_item(self, item_layout):
        """
        Removes the item associated with the provided `item_layout` from the
        items box.

        """

        # Obtain the value in the layout
        item_box = item_layout.itemAt(1).widget()
        item_value = get_box_value(item_box)

        # If item_value is not None, a modified signal must be emitted later
        emit_signal = (item_value is not None)

        # Remove corresponding item layout
        self.items_layout.removeRow(item_layout)

        # Emit modified signal if required
        if emit_signal:
            self.modified.emit()

    # This function retrieves the values of the items in this items box
    def get_box_value(self, *value_sig):
        """
        Returns the current values of this items box as a list.

        Returns
        -------
        items_list : list
            A list with the items currently in this items box.

        """

        # Create an empty list to hold the item values in
        items_list = []

        # Loop over all items in the items form and save them to the list
        for i in range(self.itemCount()):
            # Obtain the value of this entry
            item_layout = self.items_layout.itemAt(i).layout()
            item_box = item_layout.itemAt(1).widget()
            item_value = get_box_value(item_box)

            # Add this item to the list if it is not None
            if item_value is not None:
                items_list.append(item_value)

        # Return items_list
        return(items_list)

    # This function sets the values of the items in this items box
    def set_box_value(self, items_list, *value_sig):
        """
        Sets the values of the items in this items box to the provided
        `items_list`.

        Parameters
        ----------
        items_list : items
            A list containing all items that must be set in this items box.

        """

        # Hide the items box to allow for its values to be set properly
        self.hide()

        # Remove all items from the items box
        for _ in range(self.itemCount()):
            # Remove this item
            self.items_layout.removeRow(0)

        # Add all items in items_list
        for row, value in enumerate(items_list):
            # Add a new item
            self.add_item()

            # Set the value of this item
            item_layout = self.items_layout.itemAt(row).layout()
            item_box = item_layout.itemAt(1).widget()
            set_box_value(item_box, value)

        # Show the items box again now that its values have been set
        self.show()
