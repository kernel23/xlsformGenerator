import os
from qgis.PyQt.QtCore import pyqtSlot, QUrl
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QPushButton
from qgis.PyQt.QtWebEngineWidgets import QWebEngineView
from qgis.PyQt.QtWebChannel import QWebChannel
from qgis.core import QgsProject, QgsVectorLayer, QgsField, QgsFeature, QgsGeometry
from PyQt5.QtCore import QVariant

class XLSFormLayerGeneratorDialog(QDialog):
    """The main dialog for the XLSForm Layer Generator plugin."""

    def __init__(self, parent=None):
        """Constructor."""
        super(XLSFormLayerGeneratorDialog, self).__init__(parent)
        self.setWindowTitle("XLSForm Layer Generator")
        self.resize(1000, 800)

        # --- Layout and Widgets ---
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.webview = QWebEngineView()
        layout.addWidget(self.webview)

        self.create_layer_button = QPushButton("Create Layer")
        layout.addWidget(self.create_layer_button)

        # --- Web Channel Setup ---
        self.channel = QWebChannel()
        self.channel.registerObject('backend', self) # Expose this object to JS
        self.webview.page().setWebChannel(self.channel)

        # --- Load the Web App ---
        plugin_dir = os.path.dirname(__file__)
        html_path = os.path.join(plugin_dir, 'webapp', 'index.html')
        self.webview.setUrl(QUrl.fromLocalFile(html_path))

        # --- Connections ---
        self.create_layer_button.clicked.connect(self.trigger_js_data_request)

    def trigger_js_data_request(self):
        """Executes JS function to get form data and send it back."""
        self.webview.page().runJavaScript("sendDataToPython();")

    @pyqtSlot(dict)
    def generate_layer(self, data):
        """
        Receives form data from JS and generates the QGIS Layer.
        This is the core Python logic.
        """
        # For now, just print the data to show the bridge is working
        print("Data received from JavaScript:", data)

        # In a future step, this will be replaced with the full layer generation logic.
        # e.g., self.create_geopackage_layer(data)

        # Placeholder for layer creation logic
        layer_name = data.get('settings', {}).get('form_id', 'new_layer')

        # Create a memory layer to demonstrate
        vl = QgsVectorLayer("Point?crs=EPSG:4326", layer_name, "memory")
        pr = vl.dataProvider()

        # Add fields
        fields = []
        for q in data.get('questions', []):
            field_name = q.get('name')
            field_type = self.get_qgis_field_type(q.get('type'))
            if field_name:
                fields.append(QgsField(field_name, field_type))

        pr.addAttributes(fields)
        vl.updateFields()

        # Add layer to project
        QgsProject.instance().addMapLayer(vl)
        print(f"Layer '{layer_name}' created and added to the project.")

    def get_qgis_field_type(self, xlsform_type):
        """Maps XLSForm types to QGIS field types."""
        if xlsform_type in ['integer']:
            return QVariant.Int
        if xlsform_type in ['decimal']:
            return QVariant.Double
        if xlsform_type in ['date']:
            return QVariant.Date
        # Default to String for text, select_one, select_multiple, etc.
        return QVariant.String
