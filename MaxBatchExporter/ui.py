# Import PySide2
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

# Import 3ds Max APIs
import qtmax
from pymxs import runtime as rt

import os, sys

# Append the path so we can import relative files, hack please remove
dir = os.path.dirname(os.path.realpath(__file__))
sys.path += [dir]

import Export
import ObjectTree
import importlib
importlib.reload(Export)
importlib.reload(ObjectTree)


#MAIN_WINDOW = QWidget.find(rt.windows.getMAXHWND())
MAIN_WINDOW = qtmax.GetQMaxMainWindow()


class PyMaxDialog(QDialog):
    def __init__(self, parent=QWidget.find(rt.windows.getMAXHWND())):
        super(PyMaxDialog, self).__init__(parent)
        self.setWindowTitle("Max Batch Exporter")
        self.setWindowIcon(QIcon(":/GameExporter/SavePreset_32"))
        self.initUI()
        self.setAttribute(Qt.WA_DeleteOnClose)

    def initUI(self):
        layout = QVBoxLayout()

        """ Object tree view """
        objectTree = ObjectTree.ObjectTree()
        objectTree.addObjects(rt.selection) # Default to the current selection
        layout.addWidget(objectTree)

        hbox = QHBoxLayout()
        layout.addLayout(hbox)

        """ Settings button """
        settingsButton = QPushButton(
            text="Settings",
            toolTip="Open FBX settings",
            icon=QIcon(":/Common/Settings_32")
        )
        settingsButton.clicked.connect(Export.openSettings)
        settingsButton.setFixedWidth(32)
        hbox.addWidget(settingsButton)

        """ Export button """
        exportButton = QPushButton(
            text="Export",
            toolTip="Batch process & export to individual files",
            icon=QIcon(":/CommandPanel/Motion/BipedRollout/MotionMixer/BatchSave_32")
        )
        exportButton.clicked.connect(lambda: Export.batchExport([]))
        hbox.addWidget(exportButton)

        self.setLayout(layout)
        self.resize(350, 200)


def show():
    dialog = MAIN_WINDOW.findChild(QDockWidget, __file__)
    if dialog is None:
        dialog = PyMaxDialog(MAIN_WINDOW)
    dialog.show()

if __name__ == '__main__':
    show()