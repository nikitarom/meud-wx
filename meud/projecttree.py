#!/usr/bin/env python
# encoding: utf-8

import wx

tree_settings = {
"size" : (200, -1),
"style" : wx.TR_DEFAULT_STYLE | wx.TR_EDIT_LABELS
}

class ProjectTree(wx.TreeCtrl):
    """Custom wx.TreeCtrl using as project inspector"""
    
    def __init__(self, parent=None):
        super(ProjectTree, self).__init__(parent, **tree_settings)
        
    def set_project(self, project):
        self._project = project
        
        self.root = self.tree.AddRoot(self.current_project.name)
        if len(self.current_project.mvcontexts) != 0:
            item = self.tree.AppendItem(self.root, "MV contexts")
            for element in self.current_project.mvcontexts:
                self.tree.AppendItem(item, element.name)
        if len(self.current_project.scales) != 0:
            item = self.tree.AppendItem(self.root, "Scales")
            for element in self.current_project.scales:
                self.tree.AppendItem(item, element.name)
        if len(self.current_project.contexts) != 0:
            item = self.tree.AppendItem(self.root, "Contexts")
            for element in self.current_project.contexts:
                self.tree.AppendItem(item, element.name)
        if len(self.current_project.concept_systems) != 0:
            item = self.tree.AppendItem(self.root, "Concept Systems")
            for element in self.current_project.concept_systems:
                self.tree.AppendItem(item, element.name)
        
if __name__ == "__main__":
    app = wx.PySimpleApp()
    f = wx.Frame(None)
    t = ProjectTree(f)
    f.Show(True)
    app.MainLoop()

        

