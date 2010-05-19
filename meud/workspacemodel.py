"""
Workspace model
"""
import os
import os.path
import shutil
import cPickle

import wx

import fca

from typesmanager import TypesManager

class WorkspaceItem(object):
    
    def __init__(self, name, path, dir=True, parent=None, type="Unknown"):
        self.name = name
        self.path = path
        self.dir = dir
        self.children = []
        self.parent = parent
        self.precessor = None
        if type == "Unknown":
            type = TypesManager.GetDefaultType(path)
        self.type = type
        if parent:
            if not self in parent.children:
                parent.AddChild(self)
            
    def __repr__(self):
        return self.name
        
    def AddChild(self, item):
        if self.dir:
            self.children.append(item)
            
    def SetType(self, type):
        self.type = type

class WorkspaceModel(object):
    _view = None
    
    def __init__(self, path):
        """path is directory containing workspace"""
        self._path = os.path.abspath(path)
        self._metadatapath = os.path.join(self._path, ".metadata")
        self._root = WorkspaceItem("Workspace", self._path)
        
        if not os.path.exists(path):
            os.mkdir(self._path)
            self._SetupNewEnvironment()
        if not os.path.exists(self._metadatapath):
            self._SetupNewEnvironment()
            
        self.LoadWorkspace()
    
    def ImportFile(self, path, parent):
        (head, tail) = os.path.split(path)
        dst = os.path.join(self._path, parent.path)
        if path == os.path.join(dst, tail):
            newitem = self.AddFile(path)
            self.SaveWorkspace()
        else:
            shutil.copy(path, dst)
            # TODO
            newpath = os.path.join(dst, tail)
            newitem = WorkspaceItem(tail, newpath, False, parent)
            self.SaveWorkspace()
        return newitem
    
    def AddFile(self, path, precessor_item=None):
        (head, tail) = os.path.split(path)
        is_dir = not os.path.isfile(path)
        newitem = WorkspaceItem(tail, path, is_dir, self._GetParentItemByPath(head))
        newitem.precessor = precessor_item
        self._view.AddNewItem(newitem)
        return newitem
    
    def AddFileFromPage(self, path, precessor):
        (head, tail) = os.path.split(path)
        newitem = WorkspaceItem(tail, path, precessor.dir, self._GetParentItemByPath(head),
                                 type = precessor.type)
        self._view.AddNewItem(newitem)
        self.SaveWorkspace()
        return newitem
        
    def AddFiles(self, paths, precessor_item):
        if not paths:
            return
        for path in paths:
            self.AddFile(path, precessor_item)
        self.SaveWorkspace()
            
    def _GetParentItemByPath(self, path):
        
        def Walk(item, path):
            if item.path == path:
                return item
            else:
                for c in item.children:
                    item = Walk(c, path)
                    if item:
                        return item
            return None
        
        return Walk(self._root, path)
            
            
    def SetItemType(self, item, type):
        item.type = type
        
    def DeleteItem(self, item):
        if item.dir:
            shutil.rmtree(item.path)
        else:
            try:
                os.remove(item.path)
            except:
                pass
            
        item.parent.children.remove(item)
        del item
        self.SaveWorkspace()
        
    def RenameItem(self, item, new_name):
        if not new_name == item.name:
            (head, tail) = os.path.split(item.path)
            new_path = os.path.join(head, new_name)
            
            try:
                os.rename(item.path, new_path)
            except:
                #TODO: Error handler
                dlg = wx.MessageDialog(self._view.GetParent(), "Can't rename, invalid new name",
                               "Error!",
                               wx.OK | wx.ICON_INFORMATION
                               )
                dlg.ShowModal()
                dlg.Destroy()
                return False
            
            item.name = new_name
            item.path = new_path
            self.SaveWorkspace()
            return True
        
    def NewDir(self, parent, new_dir):
            if not parent.dir:
                parent = parent.parent
            new_path = os.path.join(parent.path, new_dir)
            try:
                os.mkdir(new_path)
            except:
                #TODO: Error handler
                dlg = wx.MessageDialog(self._view.GetParent(), "Can't create new folder, invalid name",
                               "Error!",
                               wx.OK | wx.ICON_INFORMATION
                               )
                dlg.ShowModal()
                dlg.Destroy()
                return None
            
            new_item = WorkspaceItem(new_dir, new_path, True, parent)
            self.SaveWorkspace()
            return new_item
        
    def NewContext(self, parent, name):
        
        def _Error(message):
            dlg = wx.MessageDialog(self._view.GetParent(), message,
                            "Error!",
                            wx.OK | wx.ICON_INFORMATION
                            )
            dlg.ShowModal()
            dlg.Destroy()
            return None
        
        if name in [child.name for child in parent.children]:
            return _Error("Can't create new context, file '{0}' already exists".format(name))
        new_path = os.path.join(parent.path, name)
        try:
            fca.write_cxt(fca.Context(), new_path)
        except:
            #TODO: Error handler
            return _Error("Can't create new context, something wrong")
            
        new_item = WorkspaceItem(name, new_path, False, parent)
        self.SaveWorkspace()
        return new_item
    
    def NewMVContext(self, parent, name):
        
        def _Error(message):
            dlg = wx.MessageDialog(self._view.GetParent(), message,
                            "Error!",
                            wx.OK | wx.ICON_INFORMATION
                            )
            dlg.ShowModal()
            dlg.Destroy()
            return None
        
        if name in [child.name for child in parent.children]:
            return _Error("Can't create new many-valued context, file '{0}' already exists".format(name))
        new_path = os.path.join(parent.path, name)
        try:
            fca.write_mv_txt(fca.ManyValuedContext(), new_path)
        except:
            #TODO: Error handler
            return _Error("Can't create new many-valued context, something wrong")
            
        new_item = WorkspaceItem(name, new_path, False, parent, type="Many-valued context")
        self.SaveWorkspace()
        return new_item
            
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
    
    def FilterType(self, type):
        
        def _Walk(item, fitem, type):
            for child in item.children:
                if child.type == type:
                    WorkspaceItem(child.name, child.path, False, 
                                                 parent=fitem, type=type)
                elif child.dir:
                    _Walk(child, WorkspaceItem(child.name, child.path, True, 
                                                 parent=fitem), type)
                    
        
        newroot = WorkspaceItem("Workspace", self._path)
        _Walk(self._root, newroot, type)
        return newroot
        
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