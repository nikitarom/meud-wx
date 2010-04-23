"""
Workspace model
"""
import os.path
import shutil
import cPickle

from typesmanager import TypesManager

class WorkspaceItem(object):
    
    def __init__(self, name, path, dir=True, parent=None, type="Unknown"):
        self.name = name
        self.path = path
        self.dir = dir
        self.children = []
        self.parent = parent
        if type == "Unknown":
            type = TypesManager.GetDefaultType(path)
        self.type = type
        if parent:
            parent.AddChild(self)
            
    def __repr__(self):
        return self.name
        
    def AddChild(self, item):
        if self.dir:
            self.children.append(item)
            
    def SetType(self, type):
        self.type = type

class WorkspaceModel(object):
    
    def __init__(self, path):
        """path is directory containing workspace"""
        self._path = os.path.abspath(path)
        self._metadatapath = os.path.join(self._path, ".metadata")
        self._root = WorkspaceItem("Workspace", "")
        
        if not os.path.exists(path):
            os.mkdir(self._path)
            self._SetupNewEnvironment()
        if not os.path.exists(self._metadatapath):
            self._SetupNewEnvironment()
            
        self.LoadWorkspace()
    
    def ImportFile(self, path, parent):
        dst = os.path.join(self._path, parent.path)
        shutil.copy(path, dst)
        (head, tail) = os.path.split(path)
        # TODO
        newpath = os.path.join(dst, tail)
        newitem = WorkspaceItem(tail, newpath, False, parent)
        self.SaveWorkspace()
        return newitem
    
    def SetItemType(self, item, type):
        item.type = type
        
    def DeleteItem(self, item):
        item.parent.children.remove(item)
        del item
        self.SaveWorkspace()
    
    def ImportDir(self, path, parent):
        dst = os.path.join(self._path, parent.path)
        (head, tail) = os.path.split(path)
        newpath = os.path.join(dst, tail)
        os.mkdir(newpath)
        newitem = WorkspaceItem(tail, os.path.join(parent.path, tail), True, parent)
        self._Walk(path, newitem)
        self.SaveWorkspace()
        return newitem
        
    def _Walk(self, srcpath, parentitem):
        dst = os.path.join(self._path, parentitem.path)
        
        names = os.listdir(srcpath)
        
        for name in names:
            abspath = os.path.join(srcpath, name)
            if os.path.isfile(abspath):
                shutil.copy(abspath, dst)
                newfile = WorkspaceItem(name, os.path.join(parentitem.path, name),
                                             False, parentitem)
            else:
                os.mkdir(os.path.join(dst, name))
                newdir = WorkspaceItem(name, os.path.join(parentitem.path, name),
                                        True, parentitem)
                self._Walk(abspath, newdir)
                
    def CheckPath(self, path, parent):
        (head, tail) = os.path.split(path)
        for child in parent.children:
            if child.name == tail:
                return False
        return True
        
    def GetRoot(self):
        pass
    
    def GetParent(self, item):
        pass
    
    def GetChildren(self, item):
        pass
    
    def _SetupNewEnvironment(self):
        os.mkdir(self._metadatapath)
        self.SaveWorkspace()
        
    def __del__(self):
        self.SaveWorkspace()
        
    def SaveWorkspace(self):
        output = open(os.path.join(self._metadatapath, "meud.data"), "wb")
        cPickle.dump(self._root, output)
        output.close()
        
    def LoadWorkspace(self):
        input = open(os.path.join(self._metadatapath, "meud.data"), "rb")
        self._root = cPickle.load(input)
        input.close()