# -*- coding: utf-8 -*-

"""
Figure Options
==============

"""


# %% IMPORTS
# Built-in imports

# Package imports
import matplotlib as mpl
from matplotlib import rcParams
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy.layouts import (
    QW_QFormLayout, QW_QHBoxLayout, QW_QVBoxLayout)
from guipy.plugins.figure.widgets.plot_entry import FigurePlotEntry
from guipy.widgets import (
    DualSpinBox, FigureLabelBox, QW_QCheckBox, QW_QComboBox, QW_QDialog,
    QW_QGroupBox, QW_QLabel, QW_QMessageBox, QW_QStackedWidget, QW_QTabWidget,
    QW_QToolButton, QW_QWidget, ToggleBox, get_box_value,
    get_modified_box_signal, set_box_value)

# All declaration
__all__ = ['FigureOptionsDialog']


# %% CLASS DEFINITIONS
# Define class for the Figure options dialog
class FigureOptionsDialog(QW_QDialog):
    # Initialize FigureOptionsDialog
    def __init__(self, toolbar, *args, **kwargs):
        # Save provided FigureToolbar object
        self.toolbar = toolbar
        self.canvas = toolbar.canvas
        self.figure = self.canvas.figure
        self.axis = self.figure.gca()

        # Call super constructor
        super().__init__(toolbar)

        # Set up the figure options dialog
        self.init(*args, **kwargs)

    # This function sets up the figure options dialog
    def init(self):
        # Install event filter
        self.installEventFilter(self)

        # Set dialog properties
        self.setWindowFlags(
            QC.Qt.Dialog |
            QC.Qt.FramelessWindowHint |
            QC.Qt.NoDropShadowWindowHint)

        # Create a layout
        layout = QW_QVBoxLayout(self)

        # Add the options tabs to it
        self.options_tabs = self.create_options_tabs(0)
        layout.addWidget(self.options_tabs)

        # Add stretch
        layout.addStretch()

        # Add a buttonbox
        button_box = QW.QDialogButtonBox()
        layout.addWidget(button_box)
        close_but = button_box.addButton(button_box.Close)
        get_modified_box_signal(close_but).connect(
            self.toolbar.toggle_options_dialog)

    # This function creates the options tabwidget for the selected plot type
    def create_options_tabs(self, index=None):
        # Create a tab widget
        tab_widget = QW_QTabWidget(browse_tabs=False)

        # Add figure tab
        tab_widget.addTab(*self.create_figure_tab())

        # Add plots tab
        tab_widget.addTab(*self.create_plots_tab())

        # Return layout
        return(tab_widget)

    # This function creates the 'Figure' tab
    def create_figure_tab(self):
        # Create a tab
        tab = QW_QWidget()

        # Create layout
        layout = QW_QFormLayout(tab)

        # Make line edit for title
        title_box = FigureLabelBox()
        title_box[0].setToolTip("Figure title")
        title_box[1].setToolTip("Title size")
        set_box_value(title_box,
                      ('', {'fontsize': rcParams['axes.titlesize']}))
        get_modified_box_signal(title_box)[str, dict].connect(
            self.axis.set_title)
        layout.addRow("Title", title_box)
        self.title_box = title_box

        # X-AXIS
        # Create a group box for the X-axis
        x_axis_group = QW_QGroupBox("X-axis")
        layout.addRow(x_axis_group)
        x_axis_layout = QW_QFormLayout(x_axis_group)

        # Make a box for setting the label on the x-axis
        x_label_box = FigureLabelBox()
        x_label_box[0].setToolTip("Label of the X-axis")
        x_label_box[1].setToolTip("Label size")
        set_box_value(x_label_box,
                      ('', {'fontsize': rcParams['axes.labelsize']}))
        get_modified_box_signal(x_label_box)[str, dict].connect(
            self.axis.set_xlabel)
        x_axis_layout.addRow("Label", x_label_box)
        self.x_label_box = x_label_box

        # Make a box for setting the range on the x-axis
        # TODO: Maybe use dual lineedits instead to eliminate range problem?
        # TODO: This would also allow for a cell or small formula to be used
        x_range_box = DualSpinBox((float, float), r"<html>&le; X &le;</html>")
        x_min_box, x_max_box = x_range_box[:]
        x_min_box.setRange(-9999999, 9999999)
        x_min_box.setToolTip("Minimum value of the X-axis")
        x_max_box.setRange(-9999999, 9999999)
        x_max_box.setToolTip("Maximum value of the X-axis")
        set_box_value(x_range_box, self.axis.get_xlim())

        # Connect signals for x_range_box
        get_modified_box_signal(x_range_box)[float, float].connect(
            lambda *args: self.axis.set_xlim(*args, auto=None))
        self.axis.callbacks.connect(
            'xlim_changed', lambda x: set_box_value(x_range_box, x.get_xlim()))

        # Make togglebox for enabling/disaling the use of this range
        x_range_togglebox = ToggleBox(
            x_range_box, tooltip="Toggle the use of a manual X-axis range")
        x_axis_layout.addRow("Range", x_range_togglebox)

        # Connect signals for x_range_togglebox
        get_modified_box_signal(x_range_togglebox)[bool].connect(
            lambda x: self.axis.set_autoscalex_on(not x))

        # Make a box for setting the scale on the x-axis
        x_scale_box = QW_QComboBox()
        x_scale_box.addItems(['linear', 'log', 'symlog', 'logit'])
        x_scale_box.setToolTip("Value scale of the X-axis")
        get_modified_box_signal(x_scale_box).connect(self.axis.set_xscale)
        x_axis_layout.addRow("Scale", x_scale_box)

        # Y-AXIS
        # Create a group box for the Y-axis
        y_axis_group = QW_QGroupBox("Y-axis")
        layout.addRow(y_axis_group)
        y_axis_layout = QW_QFormLayout(y_axis_group)

        # Make a box for setting the label on the y-axis
        y_label_box = FigureLabelBox()
        y_label_box[0].setToolTip("Label of the Y-axis")
        y_label_box[1].setToolTip("Label size")
        set_box_value(y_label_box,
                      ('', {'fontsize': rcParams['axes.labelsize']}))
        get_modified_box_signal(y_label_box)[str, dict].connect(
            self.axis.set_ylabel)
        y_axis_layout.addRow("Label", y_label_box)
        self.y_label_box = y_label_box

        # Make a box for setting the range on the y-axis
        y_range_box = DualSpinBox((float, float), r"<html>&le; Y &le;</html>")
        y_min_box, y_max_box = y_range_box[:]
        y_min_box.setRange(-9999999, 9999999)
        y_min_box.setToolTip("Minimum value of the Y-axis")
        y_max_box.setRange(-9999999, 9999999)
        y_max_box.setToolTip("Maximum value of the Y-axis")
        set_box_value(y_range_box, self.axis.get_ylim())

        # Connect signals for y_range_box
        get_modified_box_signal(y_range_box)[float, float].connect(
            lambda *args: self.axis.set_ylim(*args, auto=None))
        self.axis.callbacks.connect(
            'ylim_changed', lambda y: set_box_value(y_range_box, y.get_ylim()))

        # Make togglebox for enabling/disabling the use of this range
        y_range_togglebox = ToggleBox(
            y_range_box, tooltip="Toggle the use of a manual Y-axis range")
        y_axis_layout.addRow("Range", y_range_togglebox)

        # Connect signals for y_range_togglebox
        get_modified_box_signal(y_range_togglebox)[bool].connect(
            lambda y: self.axis.set_autoscaley_on(not y))

        # Make a box for setting the scale on the y-axis
        y_scale_box = QW_QComboBox()
        y_scale_box.addItems(['linear', 'log', 'symlog', 'logit'])
        y_scale_box.setToolTip("Value scale of the Y-axis")
        get_modified_box_signal(y_scale_box).connect(self.axis.set_yscale)
        y_axis_layout.addRow("Scale", y_scale_box)

        # PROPS
        # Create a group box for figure properties
        props_group = QW_QGroupBox("Properties")
        layout.addRow(props_group)
        props_layout = QW_QFormLayout(props_group)

        # Make a combobox for choosing the location of the legend
        legend_loc_box = QW_QComboBox()
        legend_loc_box.addItems(mpl.legend.Legend.codes.keys())
        legend_loc_box.setToolTip("Location of the figure legend")
        set_box_value(legend_loc_box, rcParams['legend.loc'])

        # Make a togglebox for using a legend
        legend_togglebox = ToggleBox(
            legend_loc_box, "Legend",
            tooltip="Toggle the use of a figure legend")
        props_layout.addRow(legend_togglebox)
        self.legend_togglebox = legend_togglebox

        # Connect signals
        get_modified_box_signal(legend_togglebox).connect(self.set_legend)
        get_modified_box_signal(legend_loc_box).connect(self.set_legend)

        # Return tab
        return(tab, "Figure")

    # This function creates the 'Plots' tab
    def create_plots_tab(self):
        # Create a tab
        tab = QW_QWidget()

        # Create layout
        layout = QW_QFormLayout(tab)

        # PLOT
        # Create a plot picker layout
        plot_layout = QW_QHBoxLayout()
        layout.addRow(plot_layout)

        # Create a label
        plot_label = QW_QLabel("Plot")
        plot_label.setSizePolicy(QW.QSizePolicy.Fixed, QW.QSizePolicy.Fixed)
        plot_layout.addWidget(plot_label)

        # Create a combobox for choosing an existing plot
        plot_entries = QW_QComboBox()
        plot_entries.setToolTip("Select the plot entry you wish to edit")
        plot_layout.addWidget(plot_entries)
        self.plot_entries = plot_entries

        # Add a toolbutton for adding a new plot entry
        add_but = QW_QToolButton()
        add_but.setToolTip("Add new plot entry")
        get_modified_box_signal(add_but).connect(self.add_entry)
        plot_layout.addWidget(add_but)

        # If this theme has an 'add' icon, use it
        if QG.QIcon.hasThemeIcon('add'):
            add_but.setIcon(QG.QIcon.fromTheme('add'))
        # Else, use a simple plus
        else:
            add_but.setText('+')

        # Add a separator
        layout.addSeparator()

        # Add a stacked widget here for dividing the plots
        plot_pages = QW_QStackedWidget()
        get_modified_box_signal(plot_entries, int).connect(
            plot_pages.setCurrentIndex)
        layout.addRow(plot_pages)
        self.plot_pages = plot_pages

        # Return tab
        return(tab, "Plots")

    # This function adds a plot entry
    @QC.Slot()
    def add_entry(self):
        # Obtain index of this plot entry
        index = self.plot_entries.count()

        # Obtain name
        name = "%i_plot" % (index)

        # Create plot entry box
        plot_entry = FigurePlotEntry(index, name, self.toolbar)

        # Connect signals
        plot_entry.entryNameChanged.connect(
            lambda x: self.plot_entries.setItemText(index, x))
        plot_entry.entryRemoveRequested.connect(self.remove_entry)

        # Add it to the plot_entries and plot_pages
        self.plot_entries.addItem(name)
        self.plot_pages.addWidget(plot_entry)

        # Set the shown entry to the new entry
        set_box_value(self.plot_entries, index)

    # This function removes a plot entry
    @QC.Slot()
    def remove_entry(self):
        # Obtain the index and widget of the currently shown plot entry
        index = get_box_value(self.plot_entries, int)
        name = get_box_value(self.plot_entries, str)
        widget = self.plot_pages.currentWidget()

        # If index is -1, return
        if(index == -1):
            return

        # Show a warning message asking if the user really wants to remove it
        button_clicked = QW_QMessageBox.warning(
            self, "WARNING: Delete plot",
            ("Are you sure you want to delete the plot with name <b>%s</b>? "
             "(<i>Note: This action is irreversible!</i>)" % (name)),
            QW_QMessageBox.Yes | QW_QMessageBox.No, QW_QMessageBox.No)

        # Remove the entry and page at this index if the user answered 'yes'
        if(button_clicked == QW_QMessageBox.Yes):
            self.plot_entries.removeItem(index)
            self.plot_pages.removeWidget(widget)
            widget.close()
            del widget

    # Override showEvent to show the dialog in the proper location
    def showEvent(self, event):
        # Call super event
        super().showEvent(event)

        # Determine the position of the top left corner of the figure dock
        dock_pos = self.toolbar.rect().topLeft()

        # Determine the size of this dialog
        size = self.size()
        size = QC.QPoint(size.width(), 0)

        # Determine position of top left corner
        dialog_pos = self.toolbar.mapToGlobal(dock_pos-size)

        # Move it slightly to give some spacing
        dialog_pos.setX(dialog_pos.x()-12)

        # Move the dialog there
        self.move(dialog_pos)

    # Override eventFilter to filter out clicks, ESC and Enter
    def eventFilter(self, widget, event):
        # Check if the event involves anything for which the popup should close
        if((event.type() == QC.QEvent.KeyPress) and
           event.key() in (QC.Qt.Key_Escape,)):
            # Toggle the options dialog
            self.toolbar.toggle_options_dialog()
            return(True)

        # Else, process events as normal
        else:
            return(super().eventFilter(widget, event))

    # This function refreshes the figure
    # TODO: Write system that stores all changes made (figure + plots) and
    # applies them whenever this function is called
    # TODO: Add a 'Refresh' button in the options menu as well
    @QC.Slot()
    def refresh_figure(self):
        # Update the figure
        if self.axis.legend_ is not None:
            self.set_legend()
        self.axis.relim()
        self.axis.autoscale_view(None, True, True)
        self.canvas.draw()

    # This function sets the legend of the figure
    @QC.Slot()
    def set_legend(self):
        # Obtain the legend_flag
        flag, loc = get_box_value(self.legend_togglebox)

        # If flag is True, create a legend
        if flag:
            self.axis.legend(loc=loc)

        # Else, remove the current one
        else:
            self.axis.legend_.remove()
