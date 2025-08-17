def classFactory(iface):
    """Load XLSFormGeneratorPlugin class from file xlsform_generator_plugin.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .xlsform_generator_plugin import XLSFormGeneratorPlugin
    return XLSFormGeneratorPlugin(iface)
