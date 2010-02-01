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
        
    def SetModel(self, model):
        self._model = model
        model._root.ref = self.AddRoot(model._root._name)
        self.Walk(model._root)
        
    def Walk(self, root):
        for item in root._children:
            item.ref = self.AppendItem(root.ref, item._name)
            self.Walk(item)
        
if __name__ == "__main__":
    app = wx.PySimpleApp()
    f = wx.Frame(None)
    t = WorkspaceView(f)
    t.SetModel(WorkspaceModel())
    f.Show(True)
    app.MainLoop()