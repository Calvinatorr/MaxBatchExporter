# Import PySide2
from PySide2.QtWidgets import QWidget, QDialog, QLabel, QVBoxLayout, QPushButton, QDockWidget
from PySide2 import QtCore
import qtmax
from pymxs import runtime as rt

import os, sys

# Append the path so we can import relative files, hack please remove
dir = os.path.dirname(os.path.realpath(__file__))
sys.path += [dir]

#from .Graphics import makePyramidMesh # Relative to package
from Graphics import makePyramidMesh

#MAIN_WINDOW = QWidget.find(rt.windows.getMAXHWND())
MAIN_WINDOW = qtmax.GetQMaxMainWindow()

class PyMaxDialog(QDialog):
    def __init__(self, parent=QWidget.find(rt.windows.getMAXHWND())):
        super(PyMaxDialog, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle("Max Batch Exporter")
        self.initUI()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def initUI(self):
        mainLayout = QVBoxLayout()
        
        label = QLabel("Click button to create a pyramind in the scene")
        mainLayout.addWidget(label)

        button = QPushButton("Pyramid")
        button.clicked.connect(lambda: makePyramidMesh())
        mainLayout.addWidget(button)

        self.setLayout(mainLayout)
        self.resize(250, 100)


def show():
    dialog = MAIN_WINDOW.findChild(QDockWidget, __file__)
    if dialog is None:
        dialog = PyMaxDialog(MAIN_WINDOW)
    dialog.show()

if __name__ == '__main__':
    show()