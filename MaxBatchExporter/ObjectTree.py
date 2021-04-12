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
        self.setEditTriggers(QTreeWidget.NoEditTriggers)
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
                columnWidth=18,
                resizeMode=QHeaderView.ResizeToContents,
                hidden=True,
            ),
        }
        self._handleColumnIndex = len(headers) - 1

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

        # Find the root parent
        root = object
        while root is not None:
            if root.Parent is None:
                break
            root = root.Parent

        # Recursively add children
        def _createItemsForObject(object, parent=None):
            self._addItem(object, parent)
            for child in object.Children:
                _createItemsForObject(child, object)

        _createItemsForObject(root)


    """ Add item to tree view based on pymxs object """
    def _addItem(self, object: pymxs.MXSWrapperBase, parent: pymxs.MXSWrapperBase=None):
        # Check if the object exists already
        if self.findObject(object):
            return

        # Find the right parent in the hierarchy
        parentItem = None
        if parent is not None:
            assert isinstance(object, pymxs.MXSWrapperBase), "Tried to read parent which is not of type pymxs.MXSWrapperBase"
            parentItem = self.findItemByPxmsObject(parent)

        # Create item widget
        item = QTreeWidgetItem(parentItem or self, [
            object.name,
            None,
            None,
            str(object.inode.handle),
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


    """ Find whether the object exists """
    def findObject(self, object: pymxs.MXSWrapperBase):
        items = self.findItems(str(object.inode.handle), Qt.MatchContains | Qt.MatchRecursive, self._handleColumnIndex)
        return len(items) > 0


    """ Find item by its pymxs object handle """
    def findItemByPxmsObject(self, object: pymxs.MXSWrapperBase):
        item = self.invisibleRootItem()

        # Recursively find item
        def _findItem(item, object):
            result = None

            for childIndex in range(0, item.childCount()):
                childItem = item.child(childIndex)
                data = childItem.data(self._handleColumnIndex, 0)
                handle = int(data)

                # If we found the matching handle
                if handle == object.inode.handle:
                    result = childItem
                    break
                else:
                    result = _findItem(childItem, object)
                    if result is not None:
                        break

            return result

        return _findItem(item, object)


    """ Get a list of objects to export """
    def getObjectsForExport(self):
        """ Get child objects from item as flattened list """
        def _getChildObjects(item, outChildren: []):
            for childIndex in range(0, item.childCount()):
                childItem = item.child(childIndex)

                # Get the pymxs object
                data = childItem.data(self._handleColumnIndex, 0)
                handle = int(data)
                object = rt.maxOps.getNodeByHandle(handle)
                outChildren += [object]

                _getChildObjects(childItem, outChildren)

        objects = []

        @dataclass
        class ObjectForExport:
            object: pymxs.MXSWrapperBase
            children = []

        rootItem = self.invisibleRootItem()
        for childIndex in range(0, rootItem.childCount()):
            topLevelItem = rootItem.child(childIndex)

            # Get pymxs object
            data = topLevelItem.data(self._handleColumnIndex, 0)
            handle = int(data)
            object = rt.maxOps.getNodeByHandle(handle)

            # Add top level object
            obj = ObjectForExport(object=object)
            _getChildObjects(topLevelItem, obj.children) # Find children
            objects += [obj]

        return objects