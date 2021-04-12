# Import PySide2
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class ExportOptionsWidget(QWidget):
    def __init__(self):
        super(ExportOptionsWidget, self).__init__()
        self.initUI()


    def initUI(self):
        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setLayout(hbox)

        # World origin
        self._worldOrigin = QCheckBox(
            text="World Origin",
            toolTip="Export from world origin (0,0,0)",
            checked=True
        )
        hbox.addWidget(self._worldOrigin)

        # Colliders
        self._exportColliders = QCheckBox(
            text="Export Colliders",
            toolTip="Include colliders in export?",
            checked=True
        )
        hbox.addWidget(self._exportColliders)

        # Sockets
        self._exportSockets = QCheckBox(
            text="Export Sockets",
            toolTip="Include sockets in export?",
            checked=True
        )
        hbox.addWidget(self._exportSockets)


    """ Export from the world origin? """
    def getWorldOrigin(self):
        return self._worldOrigin.isChecked()


    """ Include colliders in the export? """
    def getExportColliders(self):
        return self._exportColliders.isChecked()


    """ Include sockets in the export? """
    def getExportSockets(self):
        return self._exportSockets.isChecked()