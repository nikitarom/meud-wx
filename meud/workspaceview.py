"""
Created on 01.02.2010

@author: jupp
"""

import wx

from workspacemodel import WorkspaceModel

tree_settings = {
"size" : (200, -1),
"style" : wx.TR_DEFAULT_STYLE | wx.TR_EDIT_LABELS
}

class WorkspaceView(wx.TreeCtrl):
    """
    classdocs
    """

    def __init__(self, parent=None):
        """
        Constructor
        """
        super(WorkspaceView, self).__init__(parent, **tree_settings)
        
        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
        il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        self.SetImageList(il)
        self._il = il
        
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnTreeItemActivated)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        
    def SetModel(self, model):
        self._model = model
        self._model._view = self
        
        model._root.ref = self.AddRoot(model._root._name)
        self.SetPyData(model._root.ref, model._root)
        
        self.SetItemImage(model._root.ref, 0, wx.TreeItemIcon_Normal)
        self.SetItemImage(model._root.ref, 1, wx.TreeItemIcon_Expanded)
        self.Walk(model._root)
        
        self.Expand(model._root.ref)
        
    def GetModel(self):
        return self._model
        
    def Walk(self, root):
        for item in root._children:
            self.AddItem(root, item)
            self.Walk(item)
            
    def AddItem(self, root, item):
        item.ref = self.AppendItem(root.ref, item._name)
        self.SetPyData(item.ref, item)
        if item.dir:
            self.SetItemImage(item.ref, 0, wx.TreeItemIcon_Normal)
            self.SetItemImage(item.ref, 1, wx.TreeItemIcon_Expanded)
        else:
            self.SetItemImage(item.ref, 2, wx.TreeItemIcon_Normal)
            
    def OnTreeItemActivated(self, event):
        if event:
            item = event.GetItem()
            self._model.OpenFile(self.GetPyData(item))
            
    def OnContextMenu(self, event):
        active_treeitem_id = self.GetSelection()
        active_item = self.GetPyData(active_treeitem_id)
        if active_item.dir:
            menu = wx.Menu()
            menu_item = menu.Append(wx.NewId(), "tfidf")
            self.Bind(wx.EVT_MENU, self.OnTFIDF, menu_item)
            
            self.PopupMenu(menu)
            menu.Destroy()
            
    def OnTFIDF(self, event):
        import nltktest as nl
        active_treeitem_id = self.GetSelection()
        active_item = self.GetPyData(active_treeitem_id)
        path = active_item._path
        nl.main(self._model.GetAbsPath(path))
        self._model.Reload()
            
    def OnRefresh(self, event):
        self._model.Reload()
        
if __name__ == "__main__":
    app = wx.PySimpleApp()
    f = wx.Frame(None)
    t = WorkspaceView(f)
    t.SetModel(WorkspaceModel())
    f.Show(True)
    app.MainLoop()