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
from guipy import INT_TYPES
from guipy import layouts as GL, widgets as GW
from guipy.widgets import get_box_value, get_modified_signal, set_box_value

# All declaration
__all__ = ['GenericItemsBox', 'ItemsBox']


# %% CLASS DEFINITIONS
# Make class for creating item lists
class GenericItemsBox(GW.BaseBox):
    """
    Defines the :class:`~GenericItemsBox` class.

    This widget allows for a series of generic 'list' items to be maintained
    within a single box, and is basically a Qt-version of a Python list.
    Unlike :class:`~ItemsBox`, this widget allows for an unlimited number of
    boxes to be created.

    """

    # Signals
    modified = QC.Signal([], [list])

    # Initialize the ItemsBox class
    def __init__(self, item_type=None, parent=None):
        """
        Initialize an instance of the :class:`~GenericItemsBox` class.

        Optional
        --------
        item_type : callable or None. Default: None
            A callable that returns the :obj:`~PyQt5.QtWidgets.QWidget` object
            that must be used for all items in this items box.
            The types found in :obj:`~guipy.widgets.type_box_dict` can be given
            instead of a callable as well.
            If *None*, the type is unspecified.
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
            The parent widget to use for this items box or *None* for no
            parent.

        """

        # Call super constructor
        super().__init__(parent, auto_connect=False)

        # Create the items box
        self.init(item_type)

    # This property returns the default 'modified' signal
    @property
    def default_modified_signal(self):
        return(self.modified[list])

    # This property returns the number of items in the box
    def itemCount(self):
        return(self.items_layout.count())

    # This function creates the items box
    def init(self, item_type):
        """
        Sets up the items box after it has been initialized.

        """

        # Obtain the item_box
        if item_type is None:
            self.item_box = GW.LongGenericBox
        else:
            self.item_box = GW.type_box_dict.get(item_type, item_type)

        # Set the height of a single item
        self.entry_height = 24

        # Create the box_layout
        box_layout = GL.QVBoxLayout(self)
        box_layout.setContentsMargins(0, 0, 0, 0)

        # Create the items_layout
        items_layout = GL.QVBoxLayout()
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

        # Set size policy
        self.setSizePolicy(QW.QSizePolicy.Preferred, QW.QSizePolicy.Fixed)

    # This function is automatically called whenever 'modified' is emitted
    @QC.Slot()
    def modified_signal_slot(self):
        self.modified[list].emit(GenericItemsBox.get_box_value(self))

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
        item_box = self.item_box()
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
        self.items_layout.addLayout(item_layout)

        # Emit signal if item_box is not LongGenericBox
        if not isinstance(item_box, GW.LongGenericBox):
            self.modified.emit()

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
        self.items_layout.removeItem(item_layout)

        # Remove the two items in item_layout
        for _ in range(2):
            # Remove the current item at index 0
            item = item_layout.takeAt(0)

            # Close the widget in this item and delete it
            item.widget().close()
            del item

        # Emit modified signal if required
        if emit_signal:
            self.modified.emit()

    # This function retrieves the values of the items in this items box
    def get_box_value(self, *value_sig):
        """
        Returns the current values of this items box as a list.

        Returns
        -------
        value_list : list
            A list with the values of all items currently in this items box.

        """

        # Create an empty list to hold the item values in
        value_list = []

        # Loop over all items in the items form and save them to the list
        for i in range(self.itemCount()):
            # Obtain the value of this entry
            item_layout = self.items_layout.itemAt(i)
            item_box = item_layout.itemAt(1).widget()
            item_value = get_box_value(item_box)

            # Add this item to the list if it is not None
            if item_value is not None:
                value_list.append(item_value)

        # Return value_list
        return(value_list)

    # This function sets the values of the items in this items box
    def set_box_value(self, value_list, *value_sig):
        """
        Sets the values of the items in this items box to the provided
        `value_list`.

        Parameters
        ----------
        value_list : list
            A list containing the values of all items that must be set in this
            items box.

        """

        # Hide the items box to allow for its values to be set properly
        self.hide()

        # Remove all items from the items box, registering their values
        cur_items_dict = {}
        for _ in range(self.itemCount()):
            # Remove this item and obtain its value
            layout = self.items_layout.takeAt(0)
            value = get_box_value(layout.itemAt(1).widget())

            # Check if it is required later
            if value in value_list:
                # If so, store for later
                cur_items_dict[value] = layout
            else:
                # If not, delete it
                self.remove_item(layout)

        # Add all items in value_list
        for row, value in enumerate(value_list):
            # Check if this value is in cur_items_dict
            if value in cur_items_dict:
                # If so, put it back into the items box
                self.items_layout.insertLayout(row, cur_items_dict.pop(value))
            else:
                # If not, add a new item
                self.add_item()

                # Set the value of this item
                item_layout = self.items_layout.itemAt(row)
                item_box = item_layout.itemAt(1).widget()
                set_box_value(item_box, value)

        # Show the items box again now that its values have been set
        self.show()


# Make class for creating item lists
class ItemsBox(GW.BaseBox):
    """
    Defines the :class:`~ItemsBox` class.

    This widget allows for a series of 'list' items to be maintained within a
    single box, and is basically a Qt-version of a Python list.
    Unlike :class:`~GenericItemsBox`, this widget is provided with a
    pre-determined set of boxes that it will use.

    """

    # Signals
    modified = QC.Signal([], [list])

    # Initialize the ItemsBox class
    def __init__(self, item_types, layout='horizontal', parent=None):
        """
        Initialize an instance of the :class:`~ItemsBox` class.

        Parameters
        ----------
        item_types : list of callables
            A list of callables that each return the
            :obj:`~PyQt5.QtWidgets.QWidget` object that must be used in this
            items box.
            The types found in :obj:`~guipy.widgets.type_box_dict` can be given
            instead of a callable as well.

        Optional
        --------
        layout : {'horizontal'; 'vertical'}. Default: 'horizontal'
            The layout that this items box must have.
            If 'horizontal' all items will be aligned on a single row.
            If 'vertical', all items will be aligned on a single column.
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
            The parent widget to use for this items box or *None* for no
            parent.

        """

        # Call super constructor
        super().__init__(parent)

        # Create the items box
        self.init(item_types, layout)

    # Override __getitem__ to return the requested item
    def __getitem__(self, key):
        # If key is an integer, return the corresponding item
        if isinstance(key, INT_TYPES):
            # Try to return the requested item
            try:
                return(self.items[key])
            # If that cannot be done, raise IndexError
            except IndexError:
                raise IndexError("Index out of range")

        # If key is a slice object, return everything that is requested
        elif isinstance(key, slice):
            return(*map(self.__getitem__, range(*key.indices(self.N))),)

        # Else, raise TypeError
        else:
            raise TypeError("Index must be of type 'int' or 'slice', "
                            "not type %r" % (type(key).__name__))

    # This property returns the default 'modified' signal
    @property
    def default_modified_signal(self):
        return(self.modified[list])

    # This property returns the number of items in the box
    def itemCount(self):
        return(self.N)

    # This function creates the items box
    def init(self, item_types, layout):
        """
        Sets up the items box after it has been initialized.

        """

        # Set the height of a single entry
        self.entry_height = 24

        # Create empty list of items
        self.items = []

        # Obtain the proper layout
        if layout in ('h', 'horizontal', 'r', 'row'):
            layout = GL.QHBoxLayout(self)
        elif layout in ('v', 'vertical', 'c', 'col', 'column'):
            layout = GL.QVBoxLayout(self)
        else:
            raise ValueError
        layout.setContentsMargins(0, 0, 0, 0)

        # Initialize all items
        for item_type in item_types:
            # Create item
            item = GW.type_box_dict.get(item_type, item_type)()

            # Add item to items list and layout
            self.items.append(item)
            layout.addWidget(item)

        # Save the number of items
        self.N = len(self.items)

    # This function is automatically called whenever 'modified' is emitted
    @QC.Slot()
    def modified_signal_slot(self):
        self.modified[list].emit(ItemsBox.get_box_value(self))

    # This function retrieves the values of the items in this items box
    def get_box_value(self, *value_sig):
        """
        Returns the current values of this items box as a list.

        Returns
        -------
        items_list : object or list
            If `value_sig` contains a single index, the value of the
            corresponding item.
            Otherwise, a list with the values of all items in this items box.

        """

        # Check if value_sig contains an integer
        if value_sig and isinstance(value_sig[0], INT_TYPES):
            # If so, return the value of that specific item
            return(get_box_value(self.items[value_sig[0]], *value_sig[1:]))
        else:
            # If not, return the values of all items
            return(list(map(get_box_value, self.items)))

    # This function sets the values of the items in this items box
    def set_box_value(self, value_list, *value_sig):
        """
        Sets the values of the items in this items box to the provided
        `items_list`.

        Parameters
        ----------
        value_list : object of list
            If `value_sig` contains a single index, the value that must be set
            for corresponding item.
            Otherwise, a list containing the values for all items that must be
            set in this items box.

        """

        # Check if value_sig contains an integer
        if value_sig and isinstance(value_sig[0], INT_TYPES):
            # If so, set the value of that specific item
            set_box_value(self.items[value_sig[0]], value_list, *value_sig[1:])
        else:
            # If not, set the values of all items
            for item, value in zip(self.items, value_list):
                set_box_value(item, value)
