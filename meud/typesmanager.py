import os.path

_possible_types = {
                   ".cxt" : ["Context", "Scale"],
                   ".txt" : ["Text", "Context"],
                   ".xml" : ["Concepts"]
                   }

class TypesManager(object):
    
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
        return ["Unknown"]