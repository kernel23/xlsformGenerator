def classFactory(iface):
    """Load XLSFormLayerGenerator class from file xlsform_layer_generator.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .xlsform_layer_generator import XLSFormLayerGenerator
    return XLSFormLayerGenerator(iface)
