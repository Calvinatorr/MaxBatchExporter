# Import standard libraries
import os, json

# Import 3ds Max libraries
from pymxs import runtime as rt


""" Settings singleton object """
class Settings(object):
    _instance: object = None
    _propertyName = "MaxBatchExporterSettings"
    data = {}

    def __init__(self):
        raise RuntimeError("Call instance() instead")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

            # Initialization here

        return cls._instance

    def getData(self):
        # Empty dictionary
        if not self.data:
            self.loadSettings()

        return self.data


    """ Get expected filename of the settings file, including the path """
    def getExportPathKey(self):
        path = rt.maxFilePath
        if len(path) > 0:
            key = os.path.join(rt.maxFilePath, rt.maxFileName)
        else:
            key = rt.GetDir(rt.Name("scene"))
        return key


    """ Get the settings from the JSON file, will create the JSON file if it does't exist """
    def loadSettings(self):
        custom = rt.Name("custom")

        #rt.fileProperties.deleteProperty(custom, self._propertyName)

        # If property exists
        propertyIndex = rt.fileProperties.findProperty(custom, self._propertyName)
        initProperty = False
        if propertyIndex > 0:
            dataStr = rt.fileProperties.getPropertyValue(custom, propertyIndex)
            try:
                self.data = json.loads(dataStr)
                initProperty = False
            except ValueError:
                initProperty = True
        else:
            initProperty = True

        # Initialize the property
        if initProperty:
            # Default default
            self.data = {
                "exportPath": rt.maxFilePath
            }

            # Now save
            self.saveSettings()

        return self.data


    """ Save the settings into the .max file """
    def saveSettings(self):
        custom = rt.Name("custom")
        try:
            rt.fileProperties.addProperty(custom, self._propertyName, json.dumps(self.data))
        except BaseException:
            pass

        # Debug print
        """for i in range(rt.fileProperties.getNumProperties(custom)):
            print("name:", rt.fileProperties.getPropertyName(custom, i+1))
            print("value:", rt.fileProperties.getPropertyValue(custom, i+1))"""


    """ Get the export path for this file """
    def getExportPath(self):
        return self.getData()["exportPath"] or ""


    def setExportPath(self, path: str):
        self.getData()["exportPath"] = path