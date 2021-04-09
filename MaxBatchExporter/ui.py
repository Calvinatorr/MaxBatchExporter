# Import PySide2
from PySide2.QtWidgets import QWidget, QDialog, QLabel, QVBoxLayout, QPushButton
from pymxs import runtime as rt
from .graphics import makePyramidMesh

class PyMaxDialog(QDialog):
    def __init__(self, parent=QWidget.find(rt.windows.getMAXHWND())):
        super(PyMaxDialog, self).__init__(parent)
        self.setWindowTitle("Make Pyramid Window")
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()
        
        label = QLabel("Click button to create a pyramind in the scene")
        mainLayout.addWidget(label)

        button = QPushButton("Pyramid")
        button.clicked.connect(lambda: makePyramidMesh())
        mainLayout.addWidget(button)

        self.setLayout(mainLayout)
        self.resize(250, 100)