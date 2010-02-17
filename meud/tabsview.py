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
        
    def SetModel(self, model):
        self._model = model
        model._tabs_view = self