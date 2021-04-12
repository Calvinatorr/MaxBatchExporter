# Import PySide2
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

# Import 3ds Max libraries
import qtmax
from pymxs import runtime as rt

import os, sys

# Append the path so we can import relative files, hack please remove
dir = os.path.dirname(os.path.realpath(__file__))
sys.path += [dir]

import Export
import ExportOptions
import ExportPath
import ObjectTree
import importlib
importlib.reload(Export)
importlib.reload(ExportOptions)
importlib.reload(ExportPath)
importlib.reload(ObjectTree)
import Settings
importlib.reload(Settings)


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
        layout.setAlignment(Qt.AlignTop)

        # File path widget
        self.exportPath = ExportPath.ExportPathWidget()
        layout.addWidget(self.exportPath)

        # Options
        self.exportOptions = ExportOptions.ExportOptionsWidget()
        layout.addWidget(self.exportOptions)

        # Object tree view
        self.objectTree = ObjectTree.ObjectTreeWidget()
        self.objectTree.addObjects(rt.selection) # Default to the current selection
        layout.addWidget(self.objectTree)

        hbox = QHBoxLayout()
        layout.addLayout(hbox)

        # Settings button
        settingsButton = QToolButton(
            text="Settings",
            toolTip="Open FBX settings",
            icon=QIcon(":/Common/Settings_32")
        )
        settingsButton.clicked.connect(Export.openSettings)
        hbox.addWidget(settingsButton)

        # Export button
        exportButton = QPushButton(
            text="Export",
            toolTip="Batch process & export to individual files",
            icon=QIcon(":/CommandPanel/Motion/BipedRollout/MotionMixer/BatchSave_32")
        )
        exportButton.clicked.connect(self._export)
        hbox.addWidget(exportButton)

        # Progress bar
        self._progressBar = QProgressBar(
            textVisible=False
        )
        self._progressBar.setFixedHeight(12)
        layout.addWidget(self._progressBar)

        # Layout
        self.setLayout(layout)
        self.resize(400, 200)


    def event(self, event):
        if event.type() == QEvent.EnterWhatsThisMode:
            QDesktopServices.openUrl(r"https://github.com/Calvinatorr/MaxBatchExporter/blob/main/README.md")
            return True

        return super(PyMaxDialog, self).event(event)


    """ Export files """
    def _export(self):
        objects = self.objectTree.getObjectsForExport()

        # Nothing to export so pass
        if len(objects) <= 0:
            return

        # Disable for performance
        rt.disableSceneRedraw()
        rt.suspendEditing()

        # Cache selection
        selectionCache = list(rt.selection) or []
        rt.clearSelection()

        path = self.exportPath.getPath()

        # Export each root object
        try:
            for index in range(0, len(objects)):
                o = objects[index]
                time = float(index) / float(max(len(objects) - 1, 1))

                # Generate pathname
                filename = o.object.name
                pathname = os.path.join(path, filename)

                # Show progress
                print("Exporting file '" + pathname + "'..")
                self._progressBar.setValue(index * 100)

                cachedPosition = o.object.pos
                if self.exportOptions.getWorldOrigin():
                    o.object.pos = rt.point3(0, 0, 0)

                rt.select(o.object) # Select root object & clear others
                for child in o.children:
                    rt.selectMore(child)

                rt.exportFile(pathname, rt.Name("noPrompt"), selectedOnly=True, using="FBXEXP")

                # Reset position
                if self.exportOptions.getWorldOrigin():
                    o.object.pos = cachedPosition
        except error as e:
            print(e)

        # Restore scene selection
        rt.clearSelection()
        rt.select(selectionCache)

        # Re-enable
        rt.resumeEditing()
        rt.enableSceneRedraw()
        rt.redrawViews()



def show():
    dialog = MAIN_WINDOW.findChild(QDockWidget, __file__)
    if dialog is None:
        dialog = PyMaxDialog(MAIN_WINDOW)
    dialog.show()

if __name__ == '__main__':
    show()