"""
Workspace view
"""
import os

import wx

from workspacemodel import WorkspaceModel
from pluginsmanager import PluginsManager
from typesmanager import TypesManager

import images

tree_settings = {
"size" : (200, -1),
"style" : wx.TR_DEFAULT_STYLE | wx.TR_FULL_ROW_HIGHLIGHT
}

class WorkspaceView(wx.TreeCtrl):
    """
    classdocs
    """
    
    _ids = {}

    def __init__(self, parent=None):
        """
        Constructor
        """
        super(WorkspaceView, self).__init__(parent, **tree_settings)

        self.init_images()
        
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnTreeItemActivated)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        # Works well on Windows, but fail on linux
        # self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        self.Bind(wx.EVT_RIGHT_UP, self.OnContextMenu)
        
    def init_images(self):
        self.type_image_index = {}
        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        for type in TypesManager.GetKnownTypes():
            if type == "Folder":
                tuple = TypesManager.GetIcon(type)
                self.type_image_index[type] = (il.Add(tuple[0]), il.Add(tuple[1]))
            else:
                self.type_image_index[type] = il.Add(TypesManager.GetIcon(type))
        self.SetImageList(il)
        self._imagelist = il
        
    def SetModel(self, model):
        self._model = model
        model._view = self
        
        new_tree_item = self.AddRoot(model._root.name)
        self.SetPyData(new_tree_item, model._root)
        
        self.SetItemImage(new_tree_item, self.type_image_index["Folder"][0], wx.TreeItemIcon_Normal)
        self.SetItemImage(new_tree_item, self.type_image_index["Folder"][1], wx.TreeItemIcon_Expanded)
        self.Walk(model._root, self.GetRootItem())
        
        self.Expand(new_tree_item)
        
        self._pm = PluginsManager(self._model)
        
    def ResetModel(self):
        self.DeleteAllItems()
        model = self._model
        
        new_tree_item = self.AddRoot(model._root.name)
        self.SetItemImage(new_tree_item, self.type_image_index["Folder"][0], wx.TreeItemIcon_Normal)
        self.SetItemImage(new_tree_item, self.type_image_index["Folder"][1], wx.TreeItemIcon_Expanded)
        self.Walk(model._root, self.GetRootItem())
        self.Expand(new_tree_item)
         
        
    def SetTabsModel(self, tmodel):
        self._tabsmodel = tmodel
        
    def AddNewItem(self, item):
        parent_tree_item = self._ids[item.parent]
        self.AddItem(parent_tree_item, item)
    
    def Walk(self, parent, treeparent):
        for item in parent.children:
            treeitem = self.AddItem(treeparent, item)
            self.Walk(item, treeitem)
            
    def AddItem(self, parent, item):
        new_tree_item = self.AppendItem(parent, item.name)
        self._ids[item] = new_tree_item
        
        self.SetPyData(new_tree_item, item)
        if item.dir:
            self.SetItemImage(new_tree_item, self.type_image_index["Folder"][0], wx.TreeItemIcon_Normal)
            self.SetItemImage(new_tree_item, self.type_image_index["Folder"][1], wx.TreeItemIcon_Expanded)
        else:
            self.SetItemImage(new_tree_item, self.type_image_index[item.type], wx.TreeItemIcon_Normal)
        return new_tree_item
            
    def OnRightDown(self, event):
        pt = event.GetPosition();
        item, flags = self.HitTest(pt)
        if item:
            self.SelectItem(item)
    
    def OnContextMenu(self, event):
        active_treeitem_id = self.GetSelection()
        active_item = self.GetPyData(active_treeitem_id)
            
        menu = wx.Menu()
        
        New_submenu = wx.Menu()
        menu_item = New_submenu.Append(wx.NewId(), "Folder")
        self.Bind(wx.EVT_MENU, self.OnNewFolderClick, menu_item)
        
        menu_item = New_submenu.Append(wx.NewId(), "Context")
        self.Bind(wx.EVT_MENU, self.OnNewContextClick, menu_item)
        
        menu_item = New_submenu.Append(wx.NewId(), "Many-valued context")
        self.Bind(wx.EVT_MENU, self.OnNewManyValuedContextClick, menu_item)
        
        menu.AppendMenu(wx.NewId(), "New", New_submenu)
            
        import_submenu = wx.Menu()
        menu_item = import_submenu.Append(wx.NewId(), "File...")
        self.Bind(wx.EVT_MENU, self.OnImportFileClick, menu_item)
            
        menu_item = import_submenu.Append(wx.NewId(), "Dir...")
        self.Bind(wx.EVT_MENU, self.OnImportDirClick, menu_item)
            
        menu.AppendMenu(wx.NewId(), "Import", import_submenu)
        
        if active_treeitem_id != self.RootItem:
            menu_item = menu.Append(wx.NewId(), "Delete")
            self.Bind(wx.EVT_MENU, self.OnDeleteClick, menu_item)
            
            menu_item = menu.Append(wx.NewId(), "Rename...")
            self.Bind(wx.EVT_MENU, self.OnRenameClick, menu_item)
            
            plugins_submenu = self._pm.GetItemMenu(active_item, self)
            menu.AppendMenu(wx.NewId(), "Plugins", plugins_submenu)
            
            types_submenu = wx.Menu()
            
            types = TypesManager.GetPossibleTypes(active_item)
            for type in types:
                menu_item = types_submenu.AppendRadioItem(wx.NewId(), type)
                
                f = lambda event, tree_item=active_treeitem_id, type=type:\
                    self.SetItemType(tree_item, type)
                    
                self.Bind(wx.EVT_MENU, f, menu_item)
                if active_item.type == type:
                    menu_item.Check()
                
            menu.AppendMenu(wx.NewId(), "Type", types_submenu)
            
        self.PopupMenu(menu)
        menu.Destroy()
        
    def SetItemType(self, tree_item, type):
        item = self.GetPyData(tree_item)
        if item.dir:
            self.SetItemImage(tree_item, self.type_image_index["Folder"][0], wx.TreeItemIcon_Normal)
            self.SetItemImage(tree_item, self.type_image_index["Folder"][1], wx.TreeItemIcon_Expanded)
        else:
            self.SetItemImage(tree_item, self.type_image_index[type], wx.TreeItemIcon_Normal)
        self._model.SetItemType(item, type)
        
    def OnNewContextClick(self, event):
        active_treeitem_id = self.GetSelection()
        active_item = self.GetPyData(active_treeitem_id)
        if not active_item.dir:
            active_item = active_item.parent
            active_treeitem_id = self.GetItemParent(active_treeitem_id)
        
        dlg = wx.TextEntryDialog(
                self.GetParent(), "Enter name:",
                "New context")

        dlg.SetValue("context.cxt")
        
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            new_item = self._model.NewContext(active_item, name)
            
            if new_item:
                self.AddItem(active_treeitem_id, new_item)
    
    def OnNewManyValuedContextClick(self, event):
        active_treeitem_id = self.GetSelection()
        active_item = self.GetPyData(active_treeitem_id)
        if not active_item.dir:
            active_item = active_item.parent
            active_treeitem_id = self.GetItemParent(active_treeitem_id)
        
        dlg = wx.TextEntryDialog(
                self.GetParent(), "Enter name:",
                "New many-valued context")

        dlg.SetValue("mvcontext.txt")
        
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            new_item = self._model.NewMVContext(active_item, name)
            
            if new_item:
                self.AddItem(active_treeitem_id, new_item)
            
    def OnImportFileClick(self, event): 
        item = self.GetSelection()
        parent = self.GetPyData(item)
        if not parent.dir:
            parent = parent.parent # omg
            item = self.GetItemParent(item)
        
        dlg = wx.FileDialog(
            self, message="Choose a file to import",
            defaultDir=os.getcwd(), 
            defaultFile="",
            style=wx.OPEN | wx.CHANGE_DIR
            )
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if self._model.CheckPath(path, parent):
                newitem = self._model.ImportFile(path, parent)
                self.AddItem(item, newitem)
            
        dlg.Destroy()
        
    def OnImportDirClick(self, event):
        item = self.GetSelection()
        parent = self.GetPyData(item)
        if not parent.dir:
            parent = parent.parent # omg
            item = self.GetItemParent(item)
        
        dlg = wx.DirDialog(self, "Choose a directory to import:",
                          style=wx.DD_DEFAULT_STYLE
                                | wx.DD_DIR_MUST_EXIST,
                          defaultPath=os.getcwd()
                           )
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if self._model.CheckPath(path, parent):
                newitem = self._model.ImportDir(path, parent)
                new_tree_item = self.AddItem(item, newitem)
                self.Walk(newitem, new_tree_item)
            
        dlg.Destroy()
        
    def OnDeleteClick(self, event):
        active_treeitem_id = self.GetSelection()
        active_item = self.GetPyData(active_treeitem_id)
        
        msg = "Are you sure to delete '{0}' from the file system".format(active_item.name)
        dlg = wx.MessageDialog(self, msg,
                               "Delete resources",
                               wx.YES_NO | wx.ICON_INFORMATION
                               )
        if dlg.ShowModal() == wx.ID_YES:
            self._model.DeleteItem(active_item)
            self.Delete(active_treeitem_id)
        
        dlg.Destroy()
        
    def OnRenameClick(self, event):
        active_treeitem_id = self.GetSelection()
        active_item = self.GetPyData(active_treeitem_id)
        
        dlg = wx.TextEntryDialog(
                self.GetParent(), "New name:",
                "Rename resource")

        dlg.SetValue(active_item.name)

        if dlg.ShowModal() == wx.ID_OK:
            new_name = dlg.GetValue()
            if self._model.RenameItem(active_item, new_name):
                self.SetItemText(active_treeitem_id, new_name)
        
        dlg.Destroy()
        
    def OnNewFolderClick(self, event):
        active_treeitem_id = self.GetSelection()
        active_item = self.GetPyData(active_treeitem_id)
        if not active_item.dir:
            active_item = active_item.parent
            active_treeitem_id = self.GetItemParent(active_treeitem_id)
        
        dlg = wx.TextEntryDialog(
                self.GetParent(), "Enter name:",
                "New folder")

        dlg.SetValue("New folder")
        
        if dlg.ShowModal() == wx.ID_OK:
            new_folder = dlg.GetValue()
            new_item = self._model.NewDir(active_item, new_folder)
            if new_item:
                new_tree_item = self.AppendItem(active_treeitem_id, new_item.name)
                self._ids[new_item] = new_tree_item
                self.SetPyData(new_tree_item, new_item)
                self.SetItemImage(new_tree_item, self.type_image_index["Folder"][0], wx.TreeItemIcon_Normal)
                self.SetItemImage(new_tree_item, self.type_image_index["Folder"][1], wx.TreeItemIcon_Expanded)

        
    def GetModel(self):
        return self._model
    
    def OnTreeItemActivated(self, event):
        if event:
            item = event.GetItem()
            self._tabsmodel.OpenFile(self.GetPyData(item))