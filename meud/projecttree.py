#!/usr/bin/env python
# encoding: utf-8

import wx.aui

import fca

import project, contextgrid, conceptsystemgrid
from globals_ import files_categories

tree_settings = {
"size" : (200, -1),
"style" : wx.TR_DEFAULT_STYLE | wx.TR_EDIT_LABELS
}

class ProjectTree(wx.TreeCtrl):
    """Custom wx.TreeCtrl using as project inspector"""
    
    def __init__(self, parent=None):
        super(ProjectTree, self).__init__(parent, **tree_settings)
        self.nb = wx.aui.AuiNotebook(parent) # Notebook control
        
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnTreeItemActivated)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndLabelEdit)
        
    def set_project(self, project, project_dir):
        self._project = project
        self._project_dir = project_dir
        self._cats_ids = {}
        self._open_elements = []
        
        self.DeleteAllItems()
        self.root = self.AddRoot(self._project.name)
        for category in files_categories.keys():
            list_ = self._project.__getattribute__(category)
            if len(list_) != 0:
                self._cats_ids[category] = self.AppendItem(self.root, files_categories[category])
                for element in list_:
                    self.AppendItem(self._cats_ids[category],
                                    element.name, data=wx.TreeItemData(element))
        self.Expand(self.root)
        
    def add_new_element(self, category, element):
        if category not in self._cats_ids.keys():
            self._cats_ids[category] = self.AppendItem(self.root, files_categories[category])
        self.AppendItem(self._cats_ids[category], element.name, data=wx.TreeItemData(element))
        
    def OnTreeItemActivated(self, event, item=None):
        """Tree item was activated: try to open this file."""
        if event:
            item = event.GetItem()
        if item != self.root and self.GetItemText(item) not in files_categories.values():
            # load the current selected file
            # self.SetItemBold(item, 1)
            element = self.GetItemData(item).GetData()
            for i in range(self.nb.GetPageCount()):
                if element == self.nb.GetPage(i).element:
                    self.nb.SetSelection(i)
                    return
            if isinstance(element, fca.Scale):
                new_page = contextgrid.ContextGrid(self.nb)
                new_page.Show(False)
                new_page.SetTable(contextgrid.ContextTable(element))
                self.nb.AddPage(new_page, element.name)
                self.nb.SetSelection(self.nb.GetPageIndex(new_page))
                self._project.projectdirty = True
            elif isinstance(element, fca.Context):
                new_page = contextgrid.ContextGrid(self.nb)
                new_page.Show(False)
                new_page.SetTable(contextgrid.ContextTable(element))
                self.nb.AddPage(new_page, element.name)
                self.nb.SetSelection(self.nb.GetPageIndex(new_page))
                self._project.projectdirty = True
            elif isinstance(element, fca.ManyValuedContext):
                new_page = contextgrid.MVContextGrid(self.nb)
                new_page.Show(False)
                new_page.SetTable(contextgrid.MVContextTable(element))
                self.nb.AddPage(new_page, element.name)
                self.nb.SetSelection(self.nb.GetPageIndex(new_page))
                self._project.projectdirty = True
            elif isinstance(element, fca.ConceptSystem):
                new_page = conceptsystemgrid.ConceptSystemGrid(self.nb)
                new_page.Show(False)
                new_page.SetTable(conceptsystemgrid.ConceptSystemTable(element))
                self.nb.AddPage(new_page, element.name)
                self.nb.SetSelection(self.nb.GetPageIndex(new_page))
                self._project.projectdirty = True
        else:
            pass
            
    def OnFileRemove(self, event):
        """Removes a file from the current project."""
        item = self.GetSelection()
        if item != self.root and self.GetItemText(item) not in files_categories.values():
            self.Delete(item)
            self._project.delete_element(self.GetItemData(item).GetData())
            project.save_project(self._project, self._project_dir)
            
    def OnEndLabelEdit(self, event):
        """docstring for OnEndLabelEdit"""
        item = event.GetItem()
        self.GetItemData(item).GetData().name = event.GetLabel()
        project.save_project(self._project, self._project_dir)
            
        
if __name__ == "__main__":
    app = wx.PySimpleApp()
    f = wx.Frame(None)
    t = ProjectTree(f)
    f.Show(True)
    app.MainLoop()