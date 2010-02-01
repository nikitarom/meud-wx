"""
Created on 01.02.2010

@author: jupp
"""

import os
import os.path

from globals_ import workspace_path

class WorkspaceItem(object):
    
    def __init__(self, name, path, type="dir"):
        self._name = name
        self._path = path
        self._type = type
        self._children = []
        
    def AddChild(self, item):
        if self._type == "dir":
            self._children.append(item)

class WorkspaceModel(object):
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """
        self._path = os.path.abspath(workspace_path)
        self._root = WorkspaceItem("Workspace", "")
        
        self.Walk(self._root)
        print self._root
            
    def Walk(self, root):  
        path = os.path.join(self._path, root._path)
        
        items = os.listdir(path)
        
        for item in items:
            abspath = os.path.join(path, item)
            if os.path.isfile(abspath):
                root.AddChild(WorkspaceItem(item, os.path.relpath(abspath, self._path),
                                             type="file"))
            else:
                newdir = WorkspaceItem(item, os.path.relpath(abspath, self._path),
                                        type="dir")
                root.AddChild(newdir)
                self.Walk(newdir)
        
                
    def AddDir(self, path):
        """Assuming that path is already in workspace directory 
        and path is in relative form"""
        pass
    
    def AddFile(self, path):
        pass
        
if __name__ == "__main__":
    wm = WorkspaceModel()