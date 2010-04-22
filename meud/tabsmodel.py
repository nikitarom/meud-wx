"""
Tabs Model
"""
import os.path

import wx

class TabsModel(object):
    
    def __init__(self):
        self._opened_files = []
        self._path = ""
        
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
                
                newtab.LoadFile(os.path.join(self._path, item.path))
                self._tabs_view.AddPage(newtab, item.name, True)
                
    def CloseFile(self, item):
        self._opened_files.remove(item)
