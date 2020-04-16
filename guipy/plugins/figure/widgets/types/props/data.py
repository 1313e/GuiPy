# -*- coding: utf-8 -*-

"""
Data Property
=============

"""


# %% IMPORTS
# Package imports
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy import widgets as GW
from guipy.plugins.figure.widgets.types.props import BasePlotProp
from guipy.widgets import get_box_value, get_modified_signal, set_box_value

# All declaration
__all__ = ['Data1DProp', 'Data2DProp', 'Data1or2DProp', 'Data3DProp',
           'MultiData1DProp', 'MultiData2DProp', 'MultiData3DProp']


# %% CLASS DEFINITIONS
# Define 'Data1D' plot property
class Data1DProp(BasePlotProp):
    """
    Provides the definition of the :class:`~Data1DProp` plot property.

    This property contains boxes for setting the label and the X-axis data.

    """

    # Class attributes
    NAME = "Data1D"
    DISPLAY_NAME = "Data"
    REQUIREMENTS = [*BasePlotProp.REQUIREMENTS, 'data_table_plugin']
    WIDGET_NAMES = [*BasePlotProp.WIDGET_NAMES, 'data_label_box', 'x_data_box']

    # This function creates and returns the data label box
    def data_label_box(self):
        """
        Creates a widget box for setting the label of the plot data and returns
        it.

        """

        # Make a lineedit for setting the label of the plot
        data_label_box = GW.QLineEdit()
        data_label_box.setToolTip("Label of this plot")

        # Return name and box
        return('Label', data_label_box)

    # This function creates and returns the x-axis data box
    def x_data_box(self):
        """
        Creates a widget box for setting the data for the X-axis and returns
        it.

        """

        # Make a combobox for setting the x-axis data
        x_data_box = DataColumnBox(self.data_table_plugin)
        x_data_box.setToolTip("Data table and column to use for the X-axis "
                              "data")

        # Return name and box
        return('X-axis', x_data_box)


# Define 'Data2D' plot property
class Data2DProp(Data1DProp):
    """
    Provides the definition of the :class:`~Data2DProp` plot property.

    This property contains boxes for setting the label and the X-axis; and
    Y-axis data.

    """

    # Class attributes
    NAME = "Data2D"
    WIDGET_NAMES = [*Data1DProp.WIDGET_NAMES, 'y_data_box']

    # This function creates and returns the y-axis data box
    def y_data_box(self):
        """
        Creates a widget box for setting the data for the Y-axis and returns
        it.

        """

        # Make a combobox for setting the y-axis data
        y_data_box = DataColumnBox(self.data_table_plugin)
        y_data_box.setToolTip("Data table and column to use for the Y-axis "
                              "data")

        # Return name and box
        return('Y-axis', y_data_box)


# Define 'Data1or2D' plot property
class Data1or2DProp(Data2DProp):
    """
    Provides the definition of the :class:`~Data1or2DProp` plot property.

    This property contains boxes for setting the label and the X-axis; and
    Y-axis data. The X-axis data is optional.

    """

    # Class attributes
    NAME = "Data1or2D"

    # This function creates and returns the optional x-axis data box
    def x_data_box(self):
        """
        Creates a widget box for optionally setting the data for the X-axis and
        returns it.

        """

        # Make a combobox for setting the x-axis data
        x_data_box = GW.ToggleBox(
            DataColumnBox(self.data_table_plugin),
            tooltip="Disable to automatically set the X-axis data.")
        x_data_box.setToolTip("Data table and column to use for the X-axis "
                              "data")
        set_box_value(x_data_box, (False, (None, None)))

        # Return name and box
        return('X-axis', x_data_box)


# Define 'Data3D' plot property
class Data3DProp(Data2DProp):
    """
    Provides the definition of the :class:`~Data3DProp` plot property.

    This property contains boxes for setting the label and the X-axis; Y-axis;
    and Z-axis data.

    """

    # Class attributes
    NAME = "Data3D"
    WIDGET_NAMES = [*Data2DProp.WIDGET_NAMES, 'z_data_box']

    # This function creates and returns the z-axis data box
    def z_data_box(self):
        """
        Creates a widget box for setting the data for the Z-axis and returns
        it.

        """

        # Make a combobox for setting the z-axis data
        z_data_box = DataColumnBox(self.data_table_plugin)
        z_data_box.setToolTip("Data table and column to use for the Z-axis "
                              "data")

        # Return name and box
        return('Z-axis', z_data_box)


# Define 'MultiDataND' plot property, which holds several 'DataND' props
class MultiDataNDProp(BasePlotProp):
    """
    Provides the definition of the :class:`~MultiDataNDProp` plot property.

    This property contains a tab widget with multiple `DataNDProp` properties.

    """

    # Class attributes
    DISPLAY_NAME = "Data"
    WIDGET_NAMES = [*BasePlotProp.WIDGET_NAMES, 'multi_data_box']
    TRACK_VALUES = False

    # Initialize multi data property
    def __init__(self, data_prop, *args, **kwargs):
        # Save the provided data_prop
        self.data_prop = data_prop

        # Call super constructor
        super().__init__(*args, **kwargs)

    # This function creates and returns the multi data box
    def multi_data_box(self):
        """
        Creates a widget box for setting the data for multiple 'DataND' props
        and returns it.

        """

        # Make a tab widget for holding data tabs
        tab_widget = MultiDataTabWidget()
        self.tab_widget = tab_widget

        # Create add button for tabs
        add_but = GW.QToolButton()
        add_but.setToolTip("Add additional data set")
        tab_widget.setCornerWidget(add_but, QC.Qt.TopRightCorner)

        # If this theme has an 'add' icon, use it
        if QG.QIcon.hasThemeIcon('add'):
            add_but.setIcon(QG.QIcon.fromTheme('add'))
        # Else, use a simple plus
        else:
            add_but.setText('+')

        # Connect tab widget signals
        get_modified_signal(add_but).connect(self.add_data_box)
        tab_widget.tabCloseRequested.connect(self.remove_data_box)

        # Add initial data box
        self.add_data_box()

        # Return box
        return(tab_widget,)

    # This function adds a data box to the tab widget
    @QC.Slot()
    def add_data_box(self):
        """
        Adds a new data tab to this plot property.

        """

        # Create a default widget for the new DataND prop
        data_prop = GW.BaseBox()
        get_modified_signal(data_prop).connect(self.tab_widget.modified)

        # Create a dictionary with all requirements of this property
        prop_kwargs = {req: getattr(self, req)
                       for req in self.data_prop.REQUIREMENTS}

        # Create the DataND prop
        prop_layout = self.data_prop(**prop_kwargs)

        # Set prop_layout as the layout for data_prop
        data_prop.setLayout(prop_layout)

        # Obtain the name of this data_prop
        name = "data_%i" % (self.tab_widget.count())

        # Add data_prop to the tab widget
        index = self.tab_widget.addTab(data_prop, name)

        # Switch focus to the new tab
        set_box_value(self.tab_widget, index)

        # Check if there is now more than a single tab
        self.tab_widget.setTabsClosable(self.tab_widget.count() > 1)

    # This function removes a data box from the tab widget
    @QC.Slot(int)
    def remove_data_box(self, index):
        """
        Removes the data tab associated with the provided `index` from this
        plot property.

        """

        # Obtain the DataND prop associated with this index
        data_prop = self.tab_widget.widget(index)

        # Close this data_prop
        data_prop.close()

        # Remove this data_prop from the tab widget
        self.tab_widget.removeTab(index)

        # Check if there is still more than a single tab
        self.tab_widget.setTabsClosable(self.tab_widget.count() > 1)


# Define custom QTabWidget for holding the multi data
class MultiDataTabWidget(GW.QTabWidget):
    # Define signals
    modified = QC.Signal()

    # Override constructor to connect some signals
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(*args, **kwargs)

        # Connect signals
        self.tabWasInserted.connect(self.modified)
        self.tabWasRemoved.connect(self.modified)

    # Define special get_box_value method
    def get_box_value(self, *value_sig):
        """
        Returns the values stored in the tabs of this multi data tab widget, as
        requested by the provided `value_sig`.

        Parameters
        ----------
        value_sig : positional arguments of object
            The signature of the value(s) that must be returned.
            If a signature is invalid, only the valid part will be used.
            See ``Notes`` for all valid signatures.

        Returns
        -------
        value : obj
            The requested value(s).

        Notes
        -----
        The following signatures are valid (`values` is equal to
        ``[widgets.items() for widgets in tabWidgets]``):

            =================== ===========================================
            value signature     requested value
            =================== ===========================================
            `()`                ``values``
            `(int,)`            ``values[int]``
            `(str,)`            ``[value[str] for value in values]``
            `(int, str)`        ``values[int][str]``
            `(str, *args)`      ``[value[str][*args] for value in values]``
            `(int, str, *args)` ``values[int][str][*args]``
            =================== ===========================================

        """

        # Convert value_sig to a list
        value_sig = list(value_sig)

        # Create empty list of values
        value = []

        # Check if the first argument of value_sig is an integer
        if value_sig and isinstance(value_sig[0], int):
            # If so, use the tab indicated by this index
            index = value_sig.pop(0)
            tabWidgets = [self.widget(index)]
            indexed = True
        else:
            # If not, use all tabs
            tabWidgets = self.tabWidgets()
            indexed = False

        # Loop over all tab widgets
        for widget in tabWidgets:
            # Obtain the dict of widgets in this tab
            widgets = widget.layout().widgets

            # Create dict with all box values of these widgets
            values = {key: get_box_value(box) for key, box in widgets.items()}

            # Add this dict to value
            value.append(values)

        # Check if the first argument of value_sig is a string
        if value_sig and isinstance(value_sig[0], str):
            # If so, it indicates a box that must be returned
            key = value_sig.pop(0)
            value = [val[key] for val in value]

            # If value_sig still has elements, it indexes this box
            for sig in value_sig:
                value = [val[sig] for val in value]

        # If indexed is True, return solely the first argument
        if indexed:
            value = value[0]

        # Return value
        return(value)

    # Define special set_box_value method
    def set_box_value(self, value, *value_sig):
        """
        Sets the provided `value` in the tabs of this multi data tab widget, as
        requested by the provided `value_sig`.

        Parameters
        ----------
        value : obj
            The value that must be set.
        value_sig : positional arguments of object
            The signature of the value(s) that must be set.
            If a signature is invalid, only the valid part will be used.
            See ``Notes`` for all valid signatures.

        Notes
        -----
        The following signatures are valid:

            =============== ========== ===============================
            value signature value type operation
            =============== ========== ===============================
            `()`            -          <default>
            `(int,)`        dict       ``tabWidgets[int][key]``
            `(str,)`        array_like ``tabWidgets[:][str]``
            `(int, str)`    obj        ``tabWidgets[int][str]``
            =============== ========== ===============================

        """

        # If value_sig is empty, use the default operation by raising an error
        if not value_sig:
            raise NotImplementedError

        # If value cannot be iterated over, make it into a list
        if isinstance(value, str) or not hasattr(value, '__iter__'):
            value = [value]

        # Convert value_sig to a list
        value_sig = list(value_sig)

        # Check if the first argument of value_sig is an integer
        if isinstance(value_sig[0], int):
            # If so, use tha tab indicated by this index
            index = value_sig.pop(0)
            tabWidgets = [self.widget(index)]
            indexed = True
        else:
            # If not, use all tabs
            tabWidgets = self.tabWidgets()
            indexed = False

        # Obtain the list of all required boxes
        tabBoxes = [widget.layout().widgets for widget in tabWidgets]

        # Check if the first argument of value_sig is a string
        if value_sig and isinstance(value_sig[0], str):
            # If so, it indicates the key of a specific box
            key = value_sig.pop(0)
            boxes = [tab[key] for tab in tabBoxes]

            # Loop over all boxes and assign the values
            for box, val in zip(boxes, value):
                set_box_value(box, val)

        # If not, it must have been indexed
        elif indexed:
            # If it was indexed, obtain the sole tab that was obtained
            boxes = tabBoxes[0]

            # Loop over all values in value and assign them
            for key, val in value.items():
                set_box_value(boxes[key], val)

        # Else, the signature is invalid, so raise an error
        else:
            raise NotImplementedError


# Define 'MultiData1D' plot property, holding multiple 'Data1D' props
class MultiData1DProp(MultiDataNDProp):
    """
    Provides the definition of the :class:`~MultiData1DProp` plot property.

    This property contains a tab widget with multiple `Data1DProp` properties.

    """

    # Class attributes
    NAME = "MultiData1D"
    REQUIREMENTS = [*MultiDataNDProp.REQUIREMENTS, *Data1DProp.REQUIREMENTS]

    # Initialize multi 1D data property
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(Data1DProp, *args, **kwargs)


# Define 'MultiData2D' plot property, holding multiple 'Data2D' props
class MultiData2DProp(MultiDataNDProp):
    """
    Provides the definition of the :class:`~MultiData2DProp` plot property.

    This property contains a tab widget with multiple `Data2DProp` properties.

    """

    # Class attributes
    NAME = "MultiData2D"
    REQUIREMENTS = [*MultiDataNDProp.REQUIREMENTS, *Data2DProp.REQUIREMENTS]

    # Initialize multi 2D data property
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(Data2DProp, *args, **kwargs)


# Define 'MultiData3D' plot property, holding multiple 'Data3D' props
class MultiData3DProp(MultiDataNDProp):
    """
    Provides the definition of the :class:`~MultiData3DProp` plot property.

    This property contains a tab widget with multiple `Data3DProp` properties.

    """

    # Class attributes
    NAME = "MultiData3D"
    REQUIREMENTS = [*MultiDataNDProp.REQUIREMENTS, *Data3DProp.REQUIREMENTS]

    # Initialize multi 3D data property
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(Data3DProp, *args, **kwargs)


# Create custom class for setting the data column used in plots
class DataColumnBox(GW.DualComboBox):
    # Initialize DataColumnBox class
    def __init__(self, data_table_plugin_obj, parent=None, *args, **kwargs):
        # Save provided data_table_obj
        self.data_table_plugin = data_table_plugin_obj
        self.tab_widget = data_table_plugin_obj.tab_widget

        # Call super constructor
        super().__init__((False, False), r"<html>&rarr;</html>", parent, *args,
                         **kwargs)

    # This function sets up the data column box
    # TODO: Figure out how to stop this from resizing when contents change
    def init(self, *args, **kwargs):
        # Call super setup
        super().init(*args, **kwargs)

        # Extract the two created comboboxes
        tables_box, columns_box = self[:]
        self.tables_box = tables_box
        self.columns_box = columns_box

        # Add items to data tables combobox
        for i, name in enumerate(self.tab_widget.tabNames()):
            tables_box.addItem(name)
            self.set_tables_box_item_tooltip(i, name)

        # Connect signals for tables_box
        self.tab_widget.tabTextChanged.connect(tables_box.setItemText)
        self.tab_widget.tabTextChanged.connect(
            self.set_tables_box_item_tooltip)
        self.tab_widget.tabWasInserted[int, str].connect(tables_box.insertItem)
        self.tab_widget.tabWasInserted[int, str].connect(
            self.set_tables_box_item_tooltip)
        self.tab_widget.tabWasRemoved.connect(tables_box.removeItem)
        get_modified_signal(tables_box, int).connect(
            self.set_columns_box_table)

        # Set initial contents of columns_box
        self.data_table = None
        self.model = None
        self.set_box_value((None, None))

    # This function sets the tooltip of an item in the tables box
    @QC.Slot(int, str)
    def set_tables_box_item_tooltip(self, index, text):
        """
        Sets the tooltip of a specified table with `index` to the given `text`.

        Parameters
        ----------
        index : int
            The logical index of the data table that needs to change its
            tooltip.
        text : str
            The string that needs to be used for this new tooltip.

        """

        self.tables_box.setItemData(index, text, QC.Qt.ToolTipRole)

    # This function sets the data table in the columns box
    @QC.Slot(int)
    def set_columns_box_table(self, index):
        """
        Sets the columns combobox to contain all columns that are contained in
        the data table with `index`.

        Parameters
        ----------
        index : int
            The logical index of the data table whose columns need to be put
            into columns box.

        """

        # Clear the columns_box of all its items
        self.columns_box.clear()

        # If the currently saved data table still exists, disconnect signals
        if(self.data_table_plugin.tab_widget.indexOf(self.data_table) != -1):
            self.model.columnsInserted.disconnect(self.insert_columns)
            self.model.columnsRemoved.disconnect(self.remove_columns)
            self.model.columnNameChanged.disconnect(
                self.columns_box.setItemText)
            self.model.columnNameChanged.disconnect(
                self.set_columns_box_item_tooltip)

        # If currently a data table is selected, obtain its columns
        if(index != -1):
            # Obtain the data table associated with the provided index
            self.data_table = self.data_table_plugin.dataTable(index)
            self.model = self.data_table.model

            # Add all columns in this data table to the columns box
            for i, name in enumerate(self.model.columnNames()):
                self.columns_box.addItem(name)
                self.set_columns_box_item_tooltip(i, name)

            # Connect signals for columns_box
            self.model.columnsInserted.connect(self.insert_columns)
            self.model.columnsRemoved.connect(self.remove_columns)
            self.model.columnNameChanged.connect(self.columns_box.setItemText)
            self.model.columnNameChanged.connect(
                self.set_columns_box_item_tooltip)

        # Else, set data_table and model to None
        else:
            self.data_table = None
            self.model = None

    # This function sets the tooltip of an item in the columns box
    @QC.Slot(int, str)
    def set_columns_box_item_tooltip(self, index, text):
        """
        Sets the tooltip of a specified column with `index` to the given
        `text`.

        Parameters
        ----------
        index : int
            The logical index of the data column that needs to change its
            tooltip.
        text : str
            The string that needs to be used for this new tooltip.

        """

        self.columns_box.setItemData(index, text, QC.Qt.ToolTipRole)

    # This function inserts column display names into the columns box
    @QC.Slot(QC.QModelIndex, int, int)
    def insert_columns(self, parent, first, last):
        """
        Inserts new columns into the columns box between given `first` and
        `last`.

        Parameters
        ----------
        parent : :obj:`~PyQt5.QtCore.QModelIndex` object
            The parent that was used in the data table model.
            This function does not need it.
        first : int
            The logical index of the first column that was inserted.
        last : int
            The logical index of the last column that was inserted.

        """

        # Insert all columns between first and last+1 to the columns box
        for i in range(first, last+1):
            name = self.model.dataColumn(i).name
            self.columns_box.insertItem(i, name)
            self.set_columns_box_item_tooltip(i, name)

    # This function removes column display names from the columns box
    @QC.Slot(QC.QModelIndex, int, int)
    def remove_columns(self, parent, first, last):
        """
        Removes the columns from the columns box between given `first` and
        `last`.

        Parameters
        ----------
        parent : :obj:`~PyQt5.QtCore.QModelIndex` object
            The parent that was used in the data table model.
            This function does not need it.
        first : int
            The logical index of the first column that was removed.
        last : int
            The logical index of the last column that was removed.

        """

        # If the currently set column has been removed, set it to -1
        if get_box_value(self.columns_box, int) in range(first, last+1):
            set_box_value(self.columns_box, -1)

        # Remove all columns between first and last+1 from the columns box
        for i in reversed(range(first, last+1)):
            self.columns_box.removeItem(i)

    # This function retrieves the data table and column currently selected
    def get_box_value(self, *args, **kwargs):
        """
        Returns the currently selected data table and its associated column.

        Returns
        -------
        data_table : :obj:`~guipy.plugins.data_table.widgets.DataTableWidget` \
            object
            The data table that is currently set in this data column box.
        data_column : :obj:`~guipy.plugins.data_table.widgets.DataTableColumn`\
            object
            The data table column in `data_table` that is currently set.

        """

        # Obtain the currently selected column
        column_index = get_box_value(self.columns_box, int)

        # If currently a valid column is selected, return table and column
        if(column_index != -1):
            return(self.data_table, self.model.dataColumn(column_index))
        # Else, return (None, None)
        else:
            return(None, None)

    # This function sets the data table and column
    def set_box_value(self, value):
        """
        Sets the current value of the data table and its associated column to
        `value`.

        Parameters
        ----------
        value : tuple
            A tuple containing the data table and its associated column,
            formatted as `(data_table, data_column)`.

        """

        # If value[0] is None, value is equal to (-1, -1)
        if value[0] is None:
            set_box_value(self.tables_box, -1)
            set_box_value(self.columns_box, -1)
        else:
            table_name = self.tab_widget.tabText(
                self.tab_widget.indexOf(value[0]))
            set_box_value(self.tables_box, table_name)
            set_box_value(self.columns_box, value[1].name)
