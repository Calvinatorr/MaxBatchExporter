# Import PySide2
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

# Import 3ds Max APIs
from pymxs import runtime as rt

# Import settings
import Settings
import importlib
importlib.reload(Settings)
from Settings import *


class ExportPathWidget(QWidget):
    def __init__(self):
        super(ExportPathWidget, self).__init__()
        self.initUI()
        self.initPath()

        # Path changed hook
        def exportPathChanged():
            Settings.instance().setExportPath(self._path.toPlainText())
            Settings.instance().saveSettings()
        self._path.textChanged.connect(exportPathChanged)


    def initUI(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        # Browse directory button
        browseButton = QPushButton(
            text="Browse",
            toolTip="Browse for an export directory",
            icon=QIcon(":/CivilView/Open_48")
        )
        browseButton.setFixedWidth(24)
        browseButton.clicked.connect(self._browseDirectory)
        layout.addWidget(browseButton)

        # Path widget
        self._path = QTextEdit()
        self._path.setFixedHeight(24)
        layout.addWidget(self._path)


    def initPath(self):
        self._path.setText(Settings.instance().getExportPath())


    def getPath(self):
        return self._path.toPlainText()


    def _browseDirectory(self):
        # Close dialog if it exists
        try:
            self._fileDialog.close()
        except:
            pass

        # Open new file dialog
        self._fileDialog = QFileDialog()
        self._fileDialog.setDirectory(self.getPath())
        newDirectory = str(self._fileDialog.getExistingDirectory(None, "Export directory"))

        # Validate new directory
        if len(newDirectory) > 0:
            self._path.setText(newDirectory)