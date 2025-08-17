import os
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProject

# Import the dialog
from .xlsform_generator_dialog import XLSFormGeneratorDialog

class XLSFormGeneratorPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides access to the QGIS API.
        :type iface: QgsInterface
        """
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = u'&XLSForm Generator'
        self.toolbar = self.iface.addToolBar(u'XLSFormGenerator')
        self.toolbar.setObjectName(u'XLSFormGenerator')
        self.dlg = None

    def initGui(self):
        """Create the menu entries and toolbar icons for the plugin."""
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        icon = QIcon(icon_path)
        self.action = QAction(icon, u'Generate XLSForm', self.iface.mainWindow(
))
        self.action.triggered.connect(self.run)
        self.toolbar.addAction(self.action)
        self.actions.append(self.action)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(u'&XLSForm Generator', action)
        self.iface.removeToolBarIcon(self.action)
        del self.toolbar

    def run(self):
        """Run method that performs all the work."""
        # Create the dialog with elements (after translation) and keep reference
        # Only create one dialog
        if self.dlg is None:
            self.dlg = XLSFormGeneratorDialog()

        # show the dialog
        self.dlg.show()
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
