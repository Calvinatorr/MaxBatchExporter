# Import PySide2
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

# Import 3ds Max libraries
import pymxs
from pymxs import runtime as rt

from dataclasses import dataclass
import os, sys


class ObjectTreeWidget(QTreeWidget):
    def __init__(self):
        super(ObjectTreeWidget, self).__init__()
        self.initUI()


    """ Initialize the UI """
    def initUI(self):
        # Styling
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMinimumHeight(250)


        # Headers
        @dataclass
        class Header:
            columnWidth: float = 0.0
            resizeMode: QHeaderView = QHeaderView.Fixed
            hidden: bool = False

        headers = {
            "Mesh": Header(
                columnWidth=48,
                resizeMode=QHeaderView.Stretch,
            ),
            "Colliders": Header(
                columnWidth=48,
            ),
            "Sockets": Header(
                columnWidth=48,
            ),
            "Handle": Header(
                columnWidth=48,
                hidden=True,
            ),
        }

        # Assign header labels
        headerLabels = []
        for key, item in headers.items():
            headerLabels += [key]
        self.setHeaderLabels(headerLabels)

        self.header().setStretchLastSection(False)

        # Assign header (column) attributes
        for index in range(0, len(headers)):
            header = headers[list(headers)[index]]

            self.header().setSectionResizeMode(index, header.resizeMode)

            if header.hidden:
                self.hideColumn(index)


    """ Add pymxs object """
    def addObject(self, object: pymxs.MXSWrapperBase):
        assert isinstance(object, pymxs.MXSWrapperBase), "Tried to add object which is not of type pymxs.MXSWrapperBase"

        # Create item widget
        item = QTreeWidgetItem(self, [
            object.name,
            None,
            None,
            object,
        ])

        # Assign icons
        @dataclass
        class IconAssociation:
            icon: QIcon
            classTypes: []

        iconAssociations = [
            IconAssociation(
                icon=QIcon(":/CommandPanel/CreateTypes/Helpers_32"),
                classTypes=[
                    "dummy",
                ]
            ),
            IconAssociation(
                icon=QIcon(":/CommandPanel/CreateTypes/Shapes_32"),
                classTypes=[
                    "line",
                    "rectangle",
                    "circle",
                    "ellipse",
                    "arc",
                    "donut",
                    "ngon",
                    "star",
                    "text",
                    "helix",
                    "egg",
                    "sectioner",
                    "freehand",
                ]
            ),
            IconAssociation(
                icon=QIcon(":/CommandPanel/CreateTypes/Lights_32"),
                classTypes=[
                    "light",
                    "skylight",
                    "photometric light",
                    "free light",
                    "sun positioner",
                ]
            ),
            IconAssociation(
                icon=QIcon(":/CommandPanel/Motion/BipedRollout/Bones_32"),
                classTypes=[
                    "bone",
                    "ring_array",
                    "biped_object",
                ]
            ),
        ]

        # Assign icon associations
        className = str(rt.classOf(object)).lower()
        iconAssociationFound = False
        for ic in iconAssociations:
            if className in ic.classTypes:
                item.setIcon(0, ic.icon)
                iconAssociationFound = True
                break
        if not iconAssociationFound:
            item.setIcon(0, QIcon(":/CommandPanel/CreateTypes/Geometry_32"))


    """ Add list of pymxs objects """
    def addObjects(self, objects: []):
        for obj in objects:
            self.addObject(obj)