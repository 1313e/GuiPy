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
from guipy import layouts as GL, widgets as GW
from guipy.plugins.figure.widgets.plot_entry import FigurePlotEntry
from guipy.widgets import get_box_value, get_modified_signal, set_box_value

# All declaration
__all__ = ['FigureOptionsDialog']


# %% CLASS DEFINITIONS
# Define class for the Figure options dialog
class FigureOptionsDialog(GW.QDialog):
    # Create applying and discarding signals
    applying = QC.Signal()
    discarding = QC.Signal()

    # Create refreshing_plots and refreshing_figure signals
    refreshing_plots = QC.Signal()
    refreshing_figure = QC.Signal()

    # Initialize FigureOptionsDialog
    def __init__(self, canvas, figure_widget_obj):
        # Save provided FigureWidget object
        self.figure_widget = figure_widget_obj
        self.canvas = canvas
        self.figure = self.canvas.figure
        self.axis = self.figure.gca()

        # Call super constructor
        super().__init__(figure_widget_obj)

        # Set up the figure options dialog
        self.init()

    # This function shows the dialog
    @QC.Slot()
    def __call__(self):
        # Show it
        self.show()

        # Determine the position of the top left corner of the figure dock
        dock_pos = self.figure_widget.rect().topLeft()

        # Determine the size of this dialog
        size = self.size()
        size = QC.QPoint(size.width(), 0)

        # Determine position of top left corner
        dialog_pos = self.figure_widget.mapToGlobal(dock_pos-size)

        # Move it slightly to give some spacing
        dialog_pos.setX(dialog_pos.x()-12)

        # Move the dialog there
        self.move(dialog_pos)

    # This function sets up the figure options dialog
    def init(self):
        # Initialize empty dict of options
        self.options_dict = {}

        # Install event filter
        self.installEventFilter(self)

        # Set dialog properties
        # TODO: Figure out how to make the menu modal without it moving
        # automatically to the center on Linux
        self.setWindowTitle("Figure options")
        self.setWindowModality(QC.Qt.ApplicationModal)
        self.setWindowFlags(
            QC.Qt.MSWindowsOwnDC |
            QC.Qt.Dialog |
            QC.Qt.WindowTitleHint |
            QC.Qt.WindowSystemMenuHint |
            QC.Qt.WindowCloseButtonHint)

        # Create a layout
        layout = GL.QVBoxLayout(self)

        # Add the options tabs to it
        self.options_tabs = self.create_options_tabs()
        layout.addWidget(self.options_tabs)

        # Add stretch
        layout.addStretch()

        # Add a buttonbox
        button_box = QW.QDialogButtonBox()
        button_box.clicked.connect(self.buttonWasPressed)
        layout.addWidget(button_box)
        self.button_box = button_box

        # Add an 'Ok' button
        ok_but = button_box.addButton(button_box.Ok)
        ok_but.setToolTip("Apply current changes and close the figure options "
                          "menu")

        # Add a 'Cancel' button
        cancel_but = button_box.addButton(button_box.Cancel)
        cancel_but.setToolTip("Discard current changes and close the figure "
                              "options menu")
        self.cancel_but = cancel_but

        # Add an 'Apply' button
        apply_but = button_box.addButton(button_box.Apply)
        apply_but.setToolTip("Apply current figure options")
        self.apply_but = apply_but
        self.disable_apply_button()

        # Add a 'Refresh' button
        refresh_but = button_box.addButton('Refresh', button_box.ActionRole)
        refresh_but.setToolTip("Refresh figure using current figure options "
                               "without applying them")

        # Create a slot dict for all buttons
        self.slot_dict = {
            button_box.AcceptRole: [
                self.refresh_figure,
                self.apply_options,
                self.close],
            button_box.RejectRole: [
                self.discard_options,
                self.refresh_figure,
                self.close],
            button_box.ApplyRole: [
                self.apply_options],
            button_box.ActionRole: [
                self.refresh_figure]}

    # This function is called whenever a button is pressed
    @QC.Slot(QW.QAbstractButton)
    def buttonWasPressed(self, button):
        """
        Handles the actions that should be carried out when the provided
        `button` is pressed.

        """

        # Obtain the role of the provided button
        but_role = self.button_box.buttonRole(button)

        # Obtain the button's slots that must be called
        slots = self.slot_dict[but_role]

        # Call all slots defined in slots
        for slot in slots:
            slot()

    # This function adds the provided widget as an options entry
    def add_options_entry(self, widget):
        """
        Adds the provided `widget` as an options entry to this options dialog.
        This allows for the values of `widget` to be tracked and potentially
        discarded/reverted.

        """

        # Add widget as an entry to options_dict
        self.options_dict[widget] = get_box_value(widget)
        get_modified_signal(widget).connect(self.enable_apply_button)

    # This function removes the provided widget as an options entry
    def remove_options_entry(self, widget):
        """
        Removes the options entry associated with the provided `widget`, no
        longer tracking its values.

        """

        # Remove widget as an entry to options_dict
        self.options_dict.pop(widget)

    # This function creates the options tabwidget
    def create_options_tabs(self):
        # Create a tab widget
        tab_widget = GW.QTabWidget()

        # Add figure tab
        tab_widget.addTab(*self.create_figure_tab())

        # Add plots tab
        tab_widget.addTab(*self.create_plots_tab())

        # Return layout
        return(tab_widget)

    # This function creates the 'Figure' tab
    def create_figure_tab(self):
        # Create a tab
        tab = GW.BaseBox()
        get_modified_signal(tab).connect(self.enable_apply_button)

        # Create layout
        layout = GL.QFormLayout(tab)

        # Make line edit for title
        title_box = GW.FigureLabelBox()
        title_box[0].setToolTip("Figure title")
        title_box[1].setToolTip("Title size")
        set_box_value(
            title_box, ('', {'fontsize': rcParams['figure.titlesize']}))
        self.add_options_entry(title_box)
        self.refreshing_figure.connect(lambda: self.axis.set_title(
            *get_box_value(title_box, str, dict)))
        layout.addRow("Title", title_box)
        self.title_box = title_box

        # X-AXIS
        # Create a group box for the X-axis
        x_axis_group = GW.QGroupBox("X-axis")
        layout.addRow(x_axis_group)
        x_axis_layout = GL.QFormLayout(x_axis_group)

        # Make a box for setting the label on the x-axis
        x_label_box = GW.FigureLabelBox()
        x_label_box[0].setToolTip("Label of the X-axis")
        x_label_box[1].setToolTip("Label size")
        set_box_value(
            x_label_box, ('', {'fontsize': rcParams['axes.labelsize']}))
        self.add_options_entry(x_label_box)
        self.refreshing_figure.connect(lambda: self.axis.set_xlabel(
            *get_box_value(x_label_box, str, dict)))
        x_axis_layout.addRow("Label", x_label_box)
        self.x_label_box = x_label_box

        # Make a box for setting the range on the x-axis
        # TODO: Allow for a small formula or cell range to be given instead?
        x_range_box = GW.DualLineEdit((float, float),
                                      r"<html>&le; X &le;</html>")
        x_min_box, x_max_box = x_range_box[:]
        x_min_box.setToolTip("Minimum value of the X-axis")
        x_max_box.setToolTip("Maximum value of the X-axis")
        set_box_value(x_range_box, self.axis.get_xlim())

        # Connect signals for x_range_box
        self.refreshing_figure.connect(lambda: self.axis.set_xlim(
            *get_box_value(x_range_box), auto=None))
        self.axis.callbacks.connect(
            'xlim_changed', lambda x: set_box_value(x_range_box, x.get_xlim()))

        # Make togglebox for enabling/disabling the use of this range
        x_range_togglebox = GW.ToggleBox(
            x_range_box, tooltip="Check to manually set the X-axis range")
        self.add_options_entry(x_range_togglebox)
        x_axis_layout.addRow("Range", x_range_togglebox)

        # Connect signals for x_range_togglebox
        self.refreshing_figure.connect(lambda: self.axis.set_autoscalex_on(
            not get_box_value(x_range_togglebox, bool)))

        # Make a box for setting the scale on the x-axis
        x_scale_box = GW.QComboBox()
        x_scale_box.addItems(['linear', 'log', 'symlog', 'logit'])
        x_scale_box.setToolTip("Value scale of the X-axis")
        self.add_options_entry(x_scale_box)
        self.refreshing_figure.connect(lambda: self.axis.set_xscale(
            get_box_value(x_scale_box)))
        x_axis_layout.addRow("Scale", x_scale_box)

        # Y-AXIS
        # Create a group box for the Y-axis
        y_axis_group = GW.QGroupBox("Y-axis")
        layout.addRow(y_axis_group)
        y_axis_layout = GL.QFormLayout(y_axis_group)

        # Make a box for setting the label on the y-axis
        y_label_box = GW.FigureLabelBox()
        y_label_box[0].setToolTip("Label of the Y-axis")
        y_label_box[1].setToolTip("Label size")
        set_box_value(
            y_label_box, ('', {'fontsize': rcParams['axes.labelsize']}))
        self.add_options_entry(y_label_box)
        self.refreshing_figure.connect(lambda: self.axis.set_ylabel(
            *get_box_value(y_label_box, str, dict)))
        y_axis_layout.addRow("Label", y_label_box)
        self.y_label_box = y_label_box

        # Make a box for setting the range on the y-axis
        y_range_box = GW.DualLineEdit((float, float),
                                      r"<html>&le; Y &le;</html>")
        y_min_box, y_max_box = y_range_box[:]
        y_min_box.setToolTip("Minimum value of the Y-axis")
        y_max_box.setToolTip("Maximum value of the Y-axis")
        set_box_value(y_range_box, self.axis.get_ylim())

        # Connect signals for y_range_box
        self.refreshing_figure.connect(lambda: self.axis.set_ylim(
            *get_box_value(y_range_box), auto=None))
        self.axis.callbacks.connect(
            'ylim_changed', lambda y: set_box_value(y_range_box, y.get_ylim()))

        # Make togglebox for enabling/disabling the use of this range
        y_range_togglebox = GW.ToggleBox(
            y_range_box, tooltip="Check to manually set the Y-axis range")
        self.add_options_entry(y_range_togglebox)
        y_axis_layout.addRow("Range", y_range_togglebox)

        # Connect signals for y_range_togglebox
        self.refreshing_figure.connect(lambda: self.axis.set_autoscaley_on(
            not get_box_value(y_range_togglebox, bool)))

        # Make a box for setting the scale on the y-axis
        y_scale_box = GW.QComboBox()
        y_scale_box.addItems(['linear', 'log', 'symlog', 'logit'])
        y_scale_box.setToolTip("Value scale of the Y-axis")
        self.add_options_entry(y_scale_box)
        self.refreshing_figure.connect(lambda: self.axis.set_yscale(
            get_box_value(y_scale_box)))
        y_axis_layout.addRow("Scale", y_scale_box)

        # PROPS
        # Create a group box for figure properties
        props_group = GW.QGroupBox("Properties")
        layout.addRow(props_group)
        props_layout = GL.QFormLayout(props_group)

        # Make a combobox for choosing the location of the legend
        legend_loc_box = GW.QComboBox()
        legend_loc_box.addItems(mpl.legend.Legend.codes.keys())
        legend_loc_box.setToolTip("Location of the figure legend")
        set_box_value(legend_loc_box, rcParams['legend.loc'])

        # Make a togglebox for using a legend
        legend_togglebox = GW.ToggleBox(
            legend_loc_box, "Legend",
            tooltip="Toggle the use of a figure legend")
        self.add_options_entry(legend_togglebox)
        props_layout.addRow(legend_togglebox)
        self.legend_togglebox = legend_togglebox

        # Return tab
        return(tab, "Figure")

    # This function creates the 'Plots' tab
    def create_plots_tab(self):
        # Create a tab
        tab = GW.BaseBox()
        get_modified_signal(tab).connect(self.enable_apply_button)

        # Create layout
        layout = GL.QFormLayout(tab)

        # PLOT
        # Create a plot picker layout
        plot_layout = GL.QHBoxLayout()
        layout.addRow(plot_layout)

        # Create a label
        plot_label = GW.QLabel("Plot")
        plot_label.setSizePolicy(QW.QSizePolicy.Fixed, QW.QSizePolicy.Fixed)
        plot_layout.addWidget(plot_label)

        # Create a combobox for choosing an existing plot
        plot_entries = GW.QComboBox()
        plot_entries.setToolTip("Select the plot entry you wish to edit")
        plot_layout.addWidget(plot_entries)
        get_modified_signal(plot_entries).disconnect(tab.modified)
        self.plot_entries = plot_entries

        # Add a toolbutton for adding a new plot entry
        add_but = GW.QToolButton()
        add_but.setToolTip("Add new plot entry")
        get_modified_signal(add_but).connect(self.add_entry)
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
        plot_pages = GW.QStackedWidget()
        get_modified_signal(plot_entries, int).connect(
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
        plot_entry = FigurePlotEntry(index, name, self.figure_widget)

        # Connect signals
        plot_entry.entryNameChanged.connect(
            lambda x: self.plot_entries.setItemText(index, x))
        plot_entry.entryRemoveRequested.connect(self.remove_entry)

        # Add it to the plot_entries and plot_pages
        self.plot_entries.addItem(name)
        self.plot_pages.addWidget(plot_entry)
        get_modified_signal(plot_entry).connect(self.enable_apply_button)

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
        # TODO: Should this be removed once changes can be discarded?
        button_clicked = GW.QMessageBox.warning(
            self, "WARNING: Delete plot",
            ("Are you sure you want to delete the plot with name <b>%s</b>? "
             "(<i>Note: This action is irreversible!</i>)" % (name)),
            GW.QMessageBox.Yes | GW.QMessageBox.No, GW.QMessageBox.No)

        # Remove the entry and page at this index if the user answered 'yes'
        if(button_clicked == GW.QMessageBox.Yes):
            self.plot_entries.removeItem(index)
            self.plot_pages.removeWidget(widget)
            widget.setParent(None)
            widget.close()
            del widget

    # Override eventFilter to filter out ESC presses
    def eventFilter(self, widget, event):
        # Check if the event involves anything for which the popup should close
        if((event.type() == QC.QEvent.KeyPress) and
           event.key() in (QC.Qt.Key_Escape,)):
            # Act as if the 'Cancel' button was clicked
            self.cancel_but.click()
            return(True)

        # Else, process events as normal
        else:
            return(super().eventFilter(widget, event))

    # This function refreshes the figure
    # OPTIMIZE: Drawing canvas can take several seconds for large data plots
    @QC.Slot()
    def refresh_figure(self):
        # Emit the refreshing signals
        self.refreshing_plots.emit()
        self.refreshing_figure.emit()

        # Update the legend
        self.set_legend()

        # Process figure axes limits
        self.axis.relim()
        self.axis.autoscale_view(None, True, True)

        # Draw canvas
        self.canvas.draw()

    # This function sets the legend of the figure
    @QC.Slot()
    def set_legend(self):
        # Obtain the legend_flag
        flag, loc = get_box_value(self.legend_togglebox)

        # If flag is True, create a legend
        if flag:
            self.axis.legend(loc=loc)

        # Else, remove the current one if it exists
        elif self.axis.legend_ is not None:
            self.axis.legend_.remove()

    # This function applies the new figure options values
    @QC.Slot()
    def apply_options(self):
        """
        Applies all current values of all figure options.

        """

        # Emit the applying signal
        self.applying.emit()

        # Apply all new values
        for widget in self.options_dict.keys():
            self.options_dict[widget] = get_box_value(widget)

        # Disable the apply button
        self.disable_apply_button()

    # This function enables the apply button
    @QC.Slot()
    def enable_apply_button(self):
        """
        Qt slot that enables the apply button at the bottom of the figure
        options dialog.
        The apply button is enabled if at least one change has been made to any
        figure option.

        """

        self.apply_but.setEnabled(True)

    # This function disables the apply button
    @QC.Slot()
    def disable_apply_button(self):
        """
        Qt slot that disables the apply button at the bottom of the figure
        options dialog.
        The apply button is disabled whenever no changes have been made to any
        figure option.

        """

        self.apply_but.setEnabled(False)

    # This function discards all changes to the figure options
    @QC.Slot()
    def discard_options(self):
        """
        Discards the current values of all figure options and sets them back to
        their saved values.

        """

        # Emit the discarding signal
        self.discarding.emit()

        # Discard all current changes
        for widget, value in self.options_dict.items():
            set_box_value(widget, value)

        # Disable the apply button
        self.disable_apply_button()

    # Override reject to discard all options if called
    def reject(self):
        self.cancel_but.click()
        super().reject()
