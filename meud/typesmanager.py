import os.path

import images

_possible_types = {
                   ".cxt" : ["Context", "Scale"],
                   ".txt" : ["Text", "Context", "Many-valued context"],
                   ".xml" : ["Concepts"],
                   ".dot" : ["Graphviz dot"],
                   ".png" : ["Image"],
                   "" : ["Folder"]
                   }

class TypesManager(object):
    
    @staticmethod
    def GetKnownTypes():
        ktypes = set()
        for value in _possible_types.values():
            for type in value:
                ktypes.add(type)
        ktypes.add("Unknown")
        return ktypes
    
    @staticmethod
    def GetPossibleTypes(item):
        (root, ext) = os.path.splitext(item.path)
        if ext in _possible_types.keys():
            return _possible_types[ext] + ["Unknown"]
        return ["Unknown"]
    
    @staticmethod
    def GetDefaultType(path):
        (root, ext) = os.path.splitext(path)
        if ext in _possible_types.keys():
            return _possible_types[ext][0]
        return "Unknown"
    
    @staticmethod
    def GetIcon(type):
        if type == "Context":
            return images.GetBitmap("Context")
        elif type == "Many-valued context":
            return images.GetBitmap("MVContext")
        elif type == "Scale":
            return images.GetBitmap("Scale")
        elif type == "Text":
            return images.GetBitmap("Text")
        elif type == "Concepts":
            return images.GetBitmap("ConceptLattice")
        elif type == "Image":
            return images.GetBitmap("Image")
        elif type == "Folder":
            return (images.GetBitmap("HDir"), images.GetBitmap("OpenHDir"))
        else:
            return images.GetBitmap("Unknown")