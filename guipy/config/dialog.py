# -*- coding: utf-8 -*-

"""
Config Dialog
=============

"""


# %% IMPORTS
# Built-in imports
import re

# Package importsd
from qtpy import QtCore as QC, QtWidgets as QW
from sortedcontainers import SortedDict as sdict

# GuiPy imports
from guipy import layouts as GL, widgets as GW
from guipy.widgets import get_modified_signal

# All declaration
__all__ = ['ConfigDialog']


# %% CLASS DEFINITIONS
# Define config dialog
class ConfigDialog(GW.QDialog):
    """
    Defines the :class:`~ConfigDialog` class for *GuiPy*.

    This dialog serves as a general configuration skeleton, to which other
    configuration pages can be added through *GuiPy*'s configuration manager.

    """

    # Define class attributes
    NAME = "&Configuration"

    # Create applying, discarding and resetting signals
    applying = QC.Signal()
    discarding = QC.Signal()
    resetting = QC.Signal()

    # Initialize ConfigDialog class
    def __init__(self, config_manager_obj, *args, **kwargs):
        """
        Initialize an instance of the :class:`~ConfigDialog` class.

        Parameters
        ----------
        config_manager_obj : :obj:`~guipy.config.ConfigManager` object
            The config manager object that this config dialog will be connected
            to.

        """

        # Save provided config_manager_obj
        self.config_manager = config_manager_obj

        # Call super constructor
        super().__init__(*args, **kwargs)

        # Set up the config dialog
        self.init()

    # This function shows the config dialog
    @QC.Slot()
    def __call__(self):
        """
        Qt slot that shows the config dialog in the center of the main window.

        """

        # Show it
        self.show()

        # Move the options window to the center of the main window
        self.move(self.parent().geometry().center()-self.rect().center())

    # This function sets up the configuration dialog
    def init(self):
        """
        Sets up the dialog used for setting the configuration in *GuiPy*.

        """

        # Set properties of configuration dialog
        # self.setAttribute(QC.Qt.WA_DeleteOnClose)
        self.setWindowTitle(self.NAME.replace('&', ''))
        self.setWindowFlags(
            QC.Qt.MSWindowsOwnDC |
            QC.Qt.Dialog |
            QC.Qt.WindowTitleHint |
            QC.Qt.WindowSystemMenuHint |
            QC.Qt.WindowCloseButtonHint)

        # Create a window layout
        layout = GL.QVBoxLayout(self)

        # Create a splitter widget for this window
        splitter = GW.QSplitter()
        splitter.setChildrenCollapsible(False)
        layout.addWidget(splitter)

        # Create a contents widget
        contents = GW.QListWidget()
        contents.setMovement(GW.QListView.Static)
        contents.setSpacing(1)
        splitter.addWidget(contents)
        splitter.setStretchFactor(0, 1)
        self.contents = contents

        # Create a sections widget
        sections = GW.QStackedWidget()
        splitter.addWidget(sections)
        splitter.setStretchFactor(1, 5)
        self.sections = sections

        # Connect signals
        contents.currentRowChanged.connect(sections.setCurrentIndex)

        # Create empty dict of config pages
        self.config_pages = sdict()

        # Add a buttonbox
        button_box = QW.QDialogButtonBox()
        button_box.clicked.connect(self.buttonWasPressed)
        layout.addWidget(button_box)
        self.button_box = button_box

        # Add an 'Ok' button
        ok_but = button_box.addButton(button_box.Ok)
        ok_but.setToolTip("Apply current changes and close the configuration "
                          "window")

        # Add a 'Cancel' button
        cancel_but = button_box.addButton(button_box.Cancel)
        cancel_but.setToolTip("Discard current changes and close the "
                              "configuration window")
        self.cancel_but = cancel_but

        # Add an 'Apply' button
        apply_but = button_box.addButton(button_box.Apply)
        apply_but.setToolTip("Apply current configuration changes")
        self.apply_but = apply_but
        self.disable_apply_button()

        # Add a 'Reset' button
        reset_but = button_box.addButton(button_box.Reset)
        reset_but.setToolTip("Reset configuration values to defaults")

        # Create a slot dict for all buttons
        self.slot_dict = {
            button_box.AcceptRole: [
                self.apply_options,
                self.close],
            button_box.RejectRole: [
                self.discard_options,
                self.close],
            button_box.ApplyRole: [
                self.apply_options],
            button_box.ResetRole: [
                self.reset_options]}

    # This function adds a new BasicConfigPage to the dialog
    @QC.Slot(QW.QWidget)
    def add_config_page(self, config_page):
        """
        Adds a provided `config_page` to this dialog, allowing it to be
        modified.
        The name of the config page determines where it will appear in the
        dialog.

        Parameters
        ----------
        config_page : :obj:`~guipy.config.BaseConfigPage` object
            The config page object that must be added to this dialog.

        """

        # Obtain the page sections of this config page
        main, sub, tab = self.get_page_sections(config_page.section_name)

        # Obtain the full page section for this config page
        page_section = self.config_pages.setdefault(
            main, sdict()).setdefault(sub, sdict())

        # Check if this section existed before
        if(len(page_section) == 0):
            # Add the config page as a widget to the page_section and sections
            self.sections.addWidget(config_page)
            self.contents.addItem(main)

            # If this is the first section in contents, select it
            if(self.contents.count() == 1):
                self.contents.setCurrentRow(0)

        elif(len(page_section) == 1):
            # If so, a tab widget will be required
            tab_widget = GW.QTabWidget()
            page_section[''] = tab_widget

            # Obtain the index of the current widget at this section
            prev_page = page_section.values()[1]
            index = self.sections.indexOf(prev_page)

            # Remove this widget
            self.sections.removeWidget(prev_page)

            # Add the tab_widget
            self.sections.insertWidget(index, tab_widget)

            # Add the previous widget and the new config page to the tab_widget
            tab_widget.addTab(prev_page, page_section.keys()[1])
            tab_widget.addTab(config_page, tab)

        else:
            # Obtain the current tab widget
            tab_widget = page_section['']
            tab_widget.addTab(config_page, tab)

        # Connect signals
        get_modified_signal(config_page).connect(self.enable_apply_button)

        # Add this config page to the proper page section
        page_section[tab] = config_page

    # This function determines the config dialog sections a name belongs to
    def get_page_sections(self, section_name):
        """
        Determines which page (sub)sections the given `section_name` would
        belong to and returns it.

        Parameters
        ----------
        section_name : str
            The name of a specific config section.

        Returns
        -------
        main_section : str
            The name of the main section for `section_name`.
        sub_section : str
            The name of the sub section for `section_name`.
        tab_name : str
            The name of the tab on the main section for `section_name`.

        """

        # Create a regex pattern for finding the names
        pattern = r"([^/:]+)(/)?(?(2)([^:]+))(:)?(?(4)(.+))"

        # Match the given section_name
        match = re.match(pattern, section_name)

        # Obtain the different names
        main, sub, tab = match.group(1, 3, 5)

        # Add the sub to main if it is not None
        # TODO: Add the subsection system
        if sub is not None:
            main = f"{main}/{sub}"
            sub = None

        # If tab is None, set it to 'General'
        if tab is None:
            tab = 'General'

        # Return names
        return(main, sub, tab)

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

    # This function applies the new figure options values
    @QC.Slot()
    def apply_options(self):
        """
        Applies all current changes to all configuration values.

        """

        # Emit the applying signal
        self.applying.emit()

        # Disable the apply button
        self.disable_apply_button()

    # This function discards all changes to the figure options
    @QC.Slot()
    def discard_options(self):
        """
        Discards the current changes to all configuration values and sets them
        back to their saved values.

        """

        # Emit the discarding signal
        self.discarding.emit()

        # Disable the apply button
        self.disable_apply_button()

    # This function discards all changes to the figure options
    @QC.Slot()
    def reset_options(self):
        """
        Resets all configuration values back to their defaults.

        """

        # Emit the resetting signal
        self.resetting.emit()

        # Disable the apply button
        self.disable_apply_button()
