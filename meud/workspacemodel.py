"""
Created on 01.02.2010

@author: jupp
"""

import os
import os.path

import wx

from globals_ import workspace_path

default_types = {".txt" : "Text",
                 ".cxt" : "Context"}

class WorkspaceItem(object):
    
    def __init__(self, name, path, dir=True):
        self._name = name
        self._path = path
        self.dir = dir
        self._children = []
        self.ref = None
        
    def AddChild(self, item):
        if self.dir:
            self._children.append(item)

class WorkspaceModel(object):
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """
        if not os.path.exists(workspace_path):
            os.mkdir(workspace_path)
        self._path = os.path.abspath(workspace_path)
        
        self._root = WorkspaceItem("Workspace", "")
        self._opened_files = []
        self._tabs_view = None
        self._view = None
        
        self.Walk(self._root)
            
    def Walk(self, root):  
        path = os.path.join(self._path, root._path)
        
        items = os.listdir(path)
        
        for item in items:
            abspath = os.path.join(path, item)
            if os.path.isfile(abspath):
                newfile = WorkspaceItem(item, os.path.relpath(abspath, self._path),
                                             dir=False)
                root.AddChild(newfile)
                if self._view:
                    self._view.AddItem(root, newfile)
            else:
                newdir = WorkspaceItem(item, os.path.relpath(abspath, self._path),
                                        dir=True)
                root.AddChild(newdir)
                if self._view:
                    self._view.AddItem(root, newdir)
                self.Walk(newdir)
                
    def _Retouch(self, item):
        """go through the tree and determine deleted and added elements"""
        if not os.path.exists(os.path.join(self._path, item._path)):
            if item.ref:
                self._view.Delete(item.ref)
            del item
        elif item.dir:
            path = os.path.join(self._path, item._path)
            items = os.listdir(path)
            existed_paths = [i._path for i in item._children]
            current_paths = [os.path.join(item._path, path) for path in items]
            
            new_paths = set(current_paths) - set(existed_paths)
            
            for path in new_paths:
                abspath = os.path.join(self._path, path)
                if os.path.isfile(abspath):
                    newfile = WorkspaceItem(path, os.path.relpath(abspath, self._path),
                                             dir=False)
                    item.AddChild(newfile)
                    if self._view:
                        self._view.AddItem(item, newfile)
                else:
                    newdir = WorkspaceItem(path, os.path.relpath(abspath, self._path),
                                        dir=True)
                    item.AddChild(newdir)
                    if self._view:
                        self._view.AddItem(item, newdir)
                    self.Walk(newdir)
            
            for child in item._children:
                self._Retouch(child)
        
    def Reload(self):
        self._Retouch(self._root)
                
    def OpenFile(self, item):
        if not item.dir and not item in self._opened_files:
            self._opened_files.append(item)
            # then we create new tab in the tabs view
            if self._tabs_view:
                newtab = wx.TextCtrl(self._tabs_view, -1,"", size=(200, 100), 
                                     style=wx.TE_MULTILINE|wx.TE_READONLY)
                newtab.SetFont(wx.Font(14, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL,
                                       wx.FONTWEIGHT_NORMAL))
                # TODO:
                newtab.ref = item
                
                newtab.LoadFile(os.path.join(self._path, item._path))
                self._tabs_view.AddPage(newtab, item._name, True)
                
    def CloseFile(self, item):
        self._opened_files.remove(item)
                
    def AddDir(self, path):
        """Assuming that path is already in workspace directory 
        and path is in relative form"""
        pass
    
    def AddFile(self, path):
        pass
        
if __name__ == "__main__":
    wm = WorkspaceModel()