"""
Created on 02.02.2010

@author: jupp
"""

import wx.aui

class TabsView(wx.aui.AuiNotebook):
    """
    classdocs
    """

    def __init__(self, parent):
        """
        Constructor
        """
        super(TabsView, self).__init__(parent)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnNotebookPageClose)
        
    def SetModel(self, model):
        self._model = model
        model._tabs_view = self

    def OnNotebookPageClose(self, event):
        ctrl = event.GetEventObject()
        item = ctrl.GetPage(event.GetSelection()).ref
        self._model.CloseFile(item)