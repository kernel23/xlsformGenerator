import os
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProject

# Import the dialog
from .xlsform_layer_generator_dialog import XLSFormLayerGeneratorDialog

class XLSFormLayerGenerator:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor."""
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = u'&XLSForm Layer Generator'
        self.toolbar = self.iface.addToolBar(u'XLSFormLayerGenerator')
        self.toolbar.setObjectName(u'XLSFormLayerGenerator')
        self.dlg = None

    def initGui(self):
        """Create the menu entries and toolbar icons for the plugin."""
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        icon = QIcon(icon_path)
        self.action = QAction(icon, u'Generate Layer from XLSForm', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.toolbar.addAction(self.action)
        self.actions.append(self.action)
        # Also add to a menu
        self.iface.addPluginToMenu(self.menu, self.action)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(u'&XLSForm Layer Generator', action)
        self.iface.removeToolBarIcon(self.action)
        del self.toolbar

    def run(self):
        """Run method that performs all the work."""
        # Create the dialog only if it doesn't exist
        if self.dlg is None:
            self.dlg = XLSFormLayerGeneratorDialog(self.iface.mainWindow())

        # Show the dialog
        self.dlg.show()
        # The dialog is non-modal, so we don't call exec_()
        # The user can interact with QGIS while the dialog is open.
