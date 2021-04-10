name = "Max Batch Exporter"

import MaxBatchExporter.UI

def startup():
    """Create and show the dialog during 3ds Max startup"""
    dialog = MaxBatchExporter.UI.PyMaxDialog()
    dialog.show()