import os
from pymxs import runtime as rt

def batchExport(objects=[], path=""):
    #for obj in objects:

    path = rt.maxFilePath
    pathname = os.path.join(path, "export.fbx")
    print(rt.exportFile)
    rt.exportFile(pathname, rt.Name("noPrompt"), selectedOnly=True, using="FBXEXP")

def openSettings():
    rt.OpenFbxSetting()