# -*- coding: utf-8 -*-

"""
Colors
======
Provides a collection of :class:`~PyQt5.QtWidgets.QWidget` subclasses for
handling colors in :mod:`~matplotlib`.

"""


# %% IMPORTS
# Built-in imports
from importlib import import_module
from itertools import chain
import re

# Package imports
from cmasher.utils import get_cmap_type
from matplotlib import cm, rcParams
from matplotlib.colors import BASE_COLORS, CSS4_COLORS, Colormap, to_rgba
import matplotlib.pyplot as plt
import numpy as np
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW
from sortedcontainers import SortedDict as sdict, SortedSet as sset

# GuiPy imports
from guipy import layouts as GL, widgets as GW
from guipy.widgets import get_box_value, get_modified_signal, set_box_value

# All declaration
__all__ = ['ColorBox', 'ColorMapBox']


# %% CLASS DEFINITIONS
# Make class with a special box for setting the color of a plotted line
class ColorBox(GW.BaseBox):
    """
    Defines the :class:`~ColorBox` class.

    This widget allows for colors in *matplotlib* to be easily picked by the
    user.
    All cyclic; basic; and CSS4 colors in *matplotlib* are available from the
    combobox.
    Additionally, the HEX code of a color can be typed in as well.
    Finally, the user has access to a colorwheel by clicking on the color
    label, which allows for any color to be picked manually, including any
    colors currently on screen using a screenpicker.

    The default color, which is used when an invalid color is currently typed
    in, can be set using :meth:`~set_default_color`.

    """

    # Signals
    modified = QC.Signal([], [str])

    # Set the size for the color labels
    clabel_size = (70, 18)

    def __init__(self, parent=None):
        """
        Initialize an instance of the :class:`~ColorBox` class.

        """

        # Call super constructor
        super().__init__(parent)

        # Create the color box
        self.init()

    # This property returns the default 'modified' signal
    @property
    def default_modified_signal(self):
        return(self.modified[str])

    # This function creates the color box
    def init(self):
        """
        Sets up the color box entry after it has been initialized.

        This function is mainly responsible for creating the color wheel and
        color label, that allow the user to quickly cycle through different
        color options.

        """

        # Create the box layout
        box_layout = GL.QHBoxLayout(self)
        box_layout.setContentsMargins(0, 0, 0, 0)

        # Create a color label
        color_label = self.create_color_label()
        self.color_label = color_label
        box_layout.addWidget(color_label)

        # Create a color combobox
        color_combobox = self.create_color_combobox()
        box_layout.addWidget(color_combobox)
        self.color_combobox = color_combobox

        # Set the default starting color of the color box
        self.set_box_value(rcParams['lines.color'])

    # This function is automatically called whenever 'modified' is emitted
    @QC.Slot()
    def modified_signal_slot(self):
        self.modified[str].emit(get_box_value(self.color_combobox))

    # This function creates the color label
    def create_color_label(self):
        """
        Creates a special label that shows the currently selected or hovered
        color, and returns it.

        """

        # Create the color label
        color_label = GW.QLabel()

        # Set some properties
        color_label.setFrameShape(QW.QFrame.StyledPanel)
        color_label.setScaledContents(True)
        color_label.setToolTip("Click to open the custom color picker")
        color_label.setSizePolicy(QW.QSizePolicy.Fixed, QW.QSizePolicy.Fixed)
        color_label.mousePressed.connect(self.show_colorpicker)

        # Return it
        return(color_label)

    # This function creates the color combobox
    def create_color_combobox(self):
        """
        Creates a combobox that holds all default colors accepted by matplotlib
        and returns it.

        """

        # Obtain the CN colors
        n_cyclic = len(rcParams['axes.prop_cycle'])
        CN_COLORS = [("C%i" % (i), "This is MPL cyclic color #%i" % (i))
                     for i in range(n_cyclic)]

        # Make tuple of all colors
        colors = (CN_COLORS, BASE_COLORS, CSS4_COLORS)

        # Determine the cumulative lengths of all four sets
        cum_len = np.cumsum(list(map(len, colors)))

        # Make combobox for colors
        color_box = GW.EditableComboBox()

        # Add a special validator to this combobox
        validator = GW.ComboBoxValidator(color_box, r"#?[\da-fA-F]{6}")
        color_box.setValidator(validator)

        # Fill combobox with all colors
        for i, color in enumerate(chain(*colors)):
            # If color is a tuple, it consists of (color, tooltip)
            if isinstance(color, tuple):
                color_box.addItem(color[0])
                color_box.setItemData(i, color[1], QC.Qt.ToolTipRole)
            else:
                color_box.addItem(color)

        # Add some separators
        for i in reversed(cum_len[:-1]):
            color_box.insertSeparator(i)

        # Set remaining properties
        color_box.setToolTip("Select or type (in HEX) the color")
        color_box.highlighted[str].connect(self.set_color_label)
        color_box.popup_hidden[str].connect(self.set_color)
        color_box.editTextChanged.connect(self.set_color)
        color_box.focusLost.connect(
            lambda: self.set_color(self.get_box_value()))
        return(color_box)

    # This function converts an MPL color to a QColor
    @staticmethod
    def convert_to_qcolor(color):
        """
        Converts a provided matplotlib color `color` to a
        :obj:`~PyQt5.QtGui.QColor` object.

        Parameters
        ----------
        color : str or tuple of length {3, 4}
            The matplotlib color that must be converted.

        Returns
        -------
        qcolor : :obj:`~PyQt5.QtGui.QColor` object
            The instance of the :class:`~PyQt5.QtGui.QColor` class that
            corresponds to the provided `color`.

        """

        # Obtain the RGBA values of an MPL color
        r, g, b, a = to_rgba(color)

        # Convert to Qt RGBA values
        color = QG.QColor(
            round(r*255),
            round(g*255),
            round(b*255),
            round(a*255))

        # Return color
        return(color)

    # This function converts a QColor to an MPL color
    @staticmethod
    def convert_to_mpl_color(qcolor):
        """
        Converts a provided :obj:`~PyQt5.QtGui.QColor` object `color` to a
        matplotlib color.

        Parameters
        ----------
        qcolor : :obj:`~PyQt5.QtGui.QColor` object
            The instance of the :class:`~PyQt5.QtGui.QColor` class must be
            converted to a matplotlib color.

        Returns
        -------
        color : str
            The corresponding matplotlib color.
            The returned `color` is always written in HEX.

        """

        hexid = qcolor.name()
        return(str(hexid))

    # This function creates a pixmap of an MPL color
    @staticmethod
    def create_color_pixmap(color, size):
        """
        Creates a :obj:`~PyQt5.QtGui.QPixmap` object consisting of the given
        `color` with the provided `size`.

        Parameters
        ----------
        color : str
            The matplotlib color that must be used for the pixmap.
        size : tuple
            The width and height dimension values of the pixmap to be created.

        Returns
        -------
        pixmap : :obj:`~PyQt5.QtGui.QPixmap` object
            The instance of the :class:`~PyQt5.QtGui.QPixmap` class that was
            created from the provided `color` and `size`.

        """

        # Obtain the RGBA values of an MPL color
        color = ColorBox.convert_to_qcolor(color)

        # Create an image object
        image = QG.QImage(*size, QG.QImage.Format_RGB32)

        # Fill the entire image with the same color
        image.fill(color)

        # Convert the image to a pixmap
        pixmap = QG.QPixmap.fromImage(image)

        # Return the pixmap
        return(pixmap)

    # This function shows the custom color picker dialog
    @QC.Slot()
    def show_colorpicker(self):
        """
        Shows the colorwheel picker dialog to the user, allowing for any color
        option to be selected.

        """

        # Obtain current qcolor
        qcolor = self.convert_to_qcolor(self.get_box_value())

        # Show color dialog
        color = QW.QColorDialog.getColor(
            qcolor, parent=self,
            options=QW.QColorDialog.DontUseNativeDialog)

        # If the returned color is valid, save it
        if color.isValid():
            self._set_color(self.convert_to_mpl_color(color))

    # This function is called whenever the user changes the lineedit
    @QC.Slot(str)
    def set_color(self, color):
        """
        Sets the current color to the provided `color`, and updates the entry
        in the combobox and the label accordingly.

        Parameters
        ----------
        color : str
            The color that needs to be used as the current color. The provided
            `color` can be any string that is accepted as a color by
            matplotlib.
            If `color` is invalid, the default color is used instead.

        """

        # Check if the combobox currently holds an acceptable input
        status = self.color_combobox.lineEdit().hasAcceptableInput()

        # Check status
        if status:
            # If valid, add a hash if color is a 6-digit hex string
            color = re.sub(r"^[\da-fA-F]{6}$", lambda x: '#'+x[0], color)
            set_box_value(self.color_combobox, color)
        else:
            # Else, use the default color
            color = self.default_color

            # If combobox currently has no focus, set combobox value as well
            if not self.color_combobox.hasFocus():
                set_box_value(self.color_combobox, color)

        # Set the color label of the colorbox
        self.set_color_label(color)

    # This function sets a given color as the current color
    @QC.Slot(str)
    def _set_color(self, color):
        # Set the color label
        self.set_color_label(color)

        # Set the combobox to the proper value as well
        set_box_value(self.color_combobox, color)

    # This function sets the color of the colorlabel
    @QC.Slot(str)
    def set_color_label(self, color):
        """
        Sets the current color label to the provided `color`.

        Parameters
        ----------
        color : str
            The color that needs to be used as the current color label. The
            provided `color` can be any string that is accepted as a color by
            matplotlib.

        """

        # Create pixmap of given color
        pixmap = self.create_color_pixmap(color, self.clabel_size)

        # Set the colorlabel
        set_box_value(self.color_label, pixmap)

    # This function sets the default color of the color box
    @QC.Slot()
    @QC.Slot(str)
    def set_default_color(self, color=None):
        """
        Sets the default color value to `color`.

        Optional
        --------
        color : str or None. Default: None
            The matplotlib color value that must be set as the default value
            for this colorbox.
            If *None*, use the current color value of this colorbox instead.

        """

        # If color is None, obtain current value
        if color is None:
            color = self.get_box_value()

        # Set new default color
        self.default_color = color
        self.color_combobox.lineEdit().setPlaceholderText(color)

    # This function retrieves a value of this special box
    def get_box_value(self, *value_sig):
        """
        Returns the current color value of the color combobox.

        Returns
        -------
        color : str
            The current matplotlib color value.

        """

        # Return the value currently set
        return(get_box_value(self.color_combobox, *value_sig))

    # This function sets the value of this special box
    def set_box_value(self, value, *value_sig):
        """
        Sets the current color value to `value`.
        This also sets the default color to `value`.

        Parameters
        ----------
        value : str
            The matplotlib color value that must be set for this colorbox.

        """

        # Set the current default color
        self.set_default_color(value)
        self._set_color(value)


# Make class with a special box for setting the colormap of a plotted 2D hist
class ColorMapBox(GW.BaseBox):
    """
    Defines the :class:`~ColorMapBox` class.

    This widget allows for colormaps in *matplotlib* to be easily picked by the
    user.
    All colormaps that are registered in :mod:`matplotlib.cm` before the first
    time that this widget is initialized, are available in the combobox.
    Colormaps can be added to *matplotlib* using the
    :func:`~matplotlib.cm.register_cmap` function.

    The first time this widget is initialized, all icons for all colormaps are
    drawn and stored in memory, which can take a few seconds. Every

    """

    # Signals
    modified = QC.Signal([], [str])

    # Set the size for the colormap previews
    cmap_size = (70, 16)

    # Set flag for first_init
    init_flag = False

    # Set property for bad_cmaps
    bad_cmaps = {'gist_ncar', 'gist_rainbow', 'gist_stern', 'hsv', 'jet',
                 'nipy_spectral'}

    # Initialize ColorMapBox
    def __init__(self, parent=None):
        """
        Initialize an instance of the :class:`~ColorMapBox` class.

        """

        # Call super constructor
        super().__init__(parent)

        # Create the colormap box
        self.init()

    # This property returns the default 'modified' signal
    @property
    def default_modified_signal(self):
        return(self.modified[str])

    # This function creates a combobox with colormaps
    def init(self):
        # Check if this class has been initialized before, and do so if not
        if not self.init_flag:
            self.first_init()

        # Create a layout for this widget
        box_layout = GL.QHBoxLayout(self)
        box_layout.setContentsMargins(0, 0, 0, 0)

        # Create a combobox for cmaps
        cmaps_box = GW.EditableComboBox()
        validator = GW.ComboBoxValidator(cmaps_box)
        cmaps_box.setValidator(validator)

        # Add all colormaps to cmaps_box
        for cmap in self.cmaps_cl:
            cmap_icon = self.cmap_icons[cmap]
            cmaps_box.addItem(cmap_icon, cmap)

        # Add some separators
        for i in reversed(self.cum_len[:-2]):
            cmaps_box.insertSeparator(i)

        # Set remaining properties
        set_box_value(cmaps_box, rcParams['image.cmap'])
        cmaps_box.setIconSize(QC.QSize(*self.cmap_size))
        cmaps_box.completer().popup().setIconSize(QC.QSize(*self.cmap_size))
        get_modified_signal(cmaps_box, str).connect(self.cmap_selected)
        cmaps_box.focusLost.connect(
            lambda: set_box_value(cmaps_box, get_box_value(cmaps_box, int)))

        # Add cmaps_box to layout
        box_layout.addWidget(cmaps_box)
        self.cmaps_box = cmaps_box

    # This function prepares the class for being initialized for the first time
    def first_init(self):
        # Obtain all colormaps that are registered in MPL
        cmaps = plt.colormaps()

        # Split cmaps up into their cmap types
        cm_types = ['sequential', 'diverging', 'cyclic', 'qualitative', 'misc']
        cmaps_cd = {cm_type: sset() for cm_type in cm_types}
        for cmap in cmaps:
            cmaps_cd[get_cmap_type(cmap)].add(cmap)

        # Create empty list of cmaps sorted on type
        cmaps_cl = []
        cum_len = []

        # Loop over every type
        for cmaps_cs in cmaps_cd.values():
            # Take all base versions of the colormaps
            cmaps_cl.extend([cmap for cmap in cmaps_cs
                             if not cmap.endswith('_r')])
            cum_len.extend([len(cmaps_cl)])

            # Also add all the reversed versions
            cmaps_cl.extend([cmap for cmap in cmaps_cs if cmap.endswith('_r')])
            cum_len.extend([len(cmaps_cl)]*2)

        # Store list of colormaps and the category lengths
        ColorMapBox.cmaps_cl = cmaps_cl
        ColorMapBox.cum_len = cum_len

        # Create the colormap icons
        cmap_icons = sdict()
        for cmap in cmaps:
            cmap_icons[cmap] = self.create_cmap_icon(cmap, self.cmap_size)
        ColorMapBox.cmap_icons = cmap_icons

        # Save that class has been initialized for the first time
        ColorMapBox.init_flag = True

    # This function is automatically called whenever 'modified' is emitted
    @QC.Slot()
    def modified_signal_slot(self):
        self.modified[str].emit(get_box_value(self.cmaps_box))

    # This function creates an icon of a colormap
    @staticmethod
    def create_cmap_icon(cmap, size):
        """
        Creates a :obj:`~PyQt5.QtGui.QIcon` object of the given `cmap` with the
        provided `size`.

        Parameters
        ----------
        cmap : :obj:`~matplotlib.colors.Colormap` object or str
            The colormap for which an icon needs to be created.
        size : tuple
            A tuple containing the width and height dimension values of the
            icon to be created.

        Returns
        -------
        icon : :obj:`~PyQt5.QtGui.QIcon` object
            The instance of the :class:`~PyQt5.QtGui.QIcon` class that was
            created from the provided `cmap` and `size`.

        """

        # Obtain the cmap
        cmap = cm.get_cmap(cmap)

        # Obtain the RGBA values of the colormap
        mplRGBA = cmap(np.arange(cmap.N))

        # Convert to Qt RGBA values
        qtRGBA = [ColorBox.convert_to_qcolor(RGBA).rgba() for RGBA in mplRGBA]

        # Create an image object
        image = QG.QImage(cmap.N, 1, QG.QImage.Format_RGB32)

        # Set the value of every pixel in this image
        for i, RGBA in enumerate(qtRGBA):
            image.setPixel(i, 0, RGBA)

        # Scale the image to its proper size
        image = image.scaled(*size)

        # Convert the image to a pixmap
        pixmap = QG.QPixmap.fromImage(image)

        # Convert the pixmap to an icon
        icon = QG.QIcon(pixmap)

        # Return the icon
        return(icon)

    # This function allows cmaps to be added to the 'bad_cmaps' set
    def addBadCmaps(self, cmaps):
        """
        Adds the provided list of `cmaps` to the set of colormaps that should
        not be used by the user under any circumstances.

        If a user selects a colormap that is considered 'bad', a warning
        message will be shown to the user.

        Parameters
        ----------
        cmaps : list of str
            List of names of colormaps that are registered in
            :mod:`matplotlib.cm` that should be added to the list of 'bad'
            colormaps.

        """

        # Obtain the names of all colormaps
        cmap_names = plt.colormaps()

        # Make sure every colormap provided is a valid colormap
        for cmap in cmaps:
            if cmap in cmap_names and not cmap.endswith('_r'):
                # If so, add it to the set
                self.bad_cmaps.add(cmap)

    # This function checks a selected cmap
    @QC.Slot(str)
    def cmap_selected(self, cmap):
        """
        Qt slot that checks a provided `cmap` and shows an error message if
        `cmap` is a terrible colormap.

        """

        # If a terrible colormap is selected, show error message
        if cmap.startswith(tuple(self.bad_cmaps)):
            # Create error message
            err_msg = ("The selected <b><i>%s</i></b> cmap is a bad choice for"
                       " plotting data. To avoid introducing fake perceptual "
                       "features, it is recommended to pick a <i>perceptually "
                       "uniform sequential</i> colormap, like the ones with "
                       "the <i>cmr.</i> prefix.<br><br>"
                       "See <a href=\"%s\">here</a> for more information on "
                       "this subject." %
                       (cmap,
                        "https://cmasher.readthedocs.io/user/background.html"))

            # Show error window
            QW.QMessageBox.warning(
                self, "%s WARNING" % (cmap.upper()), err_msg)

    # This function retrieves a value of this special box
    def get_box_value(self, *value_sig):
        """
        Returns the current colormap of the colormap box.

        Returns
        -------
        cmap : str or :obj:`~matplotlib.colors.Colormap` object
            The currently selected colormap.

        """

        # Obtain the value
        cmap = get_box_value(self.cmaps_box)

        # Obtain the Colormap object if requested
        if Colormap in value_sig:
            cmap = plt.get_cmap(cmap)

        # Return it
        return(cmap)

    # This function sets the value of this special box
    def set_box_value(self, value, *value_sig):
        """
        Sets the current colormap to `value`.

        Parameters
        ----------
        value : str or :obj:`~matplotlib.colors.Colormap` object
            The colormap that must be used for this colormap box.

        """

        # Obtain the name of the provided colormap if needed
        if isinstance(value, Colormap):
            value = value.name

        # Set this as the current colormap
        set_box_value(self.cmaps_box, value)
