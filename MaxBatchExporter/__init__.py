name = "Max Batch Exporter"

from pymxs import runtime as rt

import os, sys
# Append the path so we can import relative files, hack please remove
dir = os.path.dirname(os.path.realpath(__file__))
sys.path += [dir]

import UI

# Link our delegate
rt.MaxBatchExporter = UI.show

# Create macroscript
macroscript = {
    "name": "MaxBatchExporter",
    "category": "Custom",
    "tooltip": "Max Batch Exporter",
    "text": "Max Batch Exporter",
    "content": "MaxBatchExporter()"
}
macroscriptID = rt.macros.new(macroscript["category"],
                              macroscript["name"],
                              macroscript["tooltip"],
                              macroscript["button"], # Where is this?
                              macroscript["content"]
                )


# Create menu item
helpMenu = rt.menuMan.findMenu("&Help")
menuItem = rt.menuMan.createActionItem(macroscript["name"], macroscript["category"])
helpMenu.addItem(menuItem, -1)
rt.menuMan.updateMenuBar()