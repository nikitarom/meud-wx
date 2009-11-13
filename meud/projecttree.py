#!/usr/bin/env python
# encoding: utf-8

import wx

tree_settings = {
"size" : (200, -1),
"style" : wx.TR_DEFAULT_STYLE | wx.TR_EDIT_LABELS
}

files_categories = {
"mvcontexts" : "Many-valued contexts",
"scales" : "Scales",
"contexts" : "Contexts",
"concept_systems" : "Concept Systems"
}

class ProjectTree(wx.TreeCtrl):
    """Custom wx.TreeCtrl using as project inspector"""
    
    def __init__(self, parent=None):
        super(ProjectTree, self).__init__(parent, **tree_settings)
        
    def set_project(self, project):
        self._project = project
        
        self.DeleteAllItems()
        self.root = self.AddRoot(self._project.name)
        for category in files_categories.keys():
            list_ = self._project.__getattribute__(category)
            if len(list_) != 0:
                item = self.AppendItem(self.root, files_categories[category])
                for element in list_:
                    self.AppendItem(item, element.name, data=wx.TreeItemData(element))
        self.Expand(self.root)
        
if __name__ == "__main__":
    app = wx.PySimpleApp()
    f = wx.Frame(None)
    t = ProjectTree(f)
    f.Show(True)
    app.MainLoop()

        

