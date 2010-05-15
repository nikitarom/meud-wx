"""
Tabs Model
"""
import wx

import contextgrid

class TabsModel(object):
    
    def __init__(self, workspace):
        self._opened_files = []
        self._path = ""
        self._tabs = {}
        self._workspace = workspace
        
    def DoUnsaved(self, item):
        self._tabs_view.SetPageText(self._tabs_view.GetPageIndex(self._tabs[item]),
                                     "*" + item.name)
        
    def DoSaved(self, item):
        self._tabs_view.SetPageText(self._tabs_view.GetPageIndex(self._tabs[item]),
                                     item.name)
        
    def FileSaveAs(self, path, page):
        new_item = self._workspace.AddFileFromPage(path, page.ref)
        
        old_item = page.ref
        self._opened_files.remove(old_item)
        self._opened_files.append(new_item)
        self._tabs.pop(old_item)
        self._tabs[new_item] = page
        
        page.ref = new_item
        self._tabs_view.SetPageText(self._tabs_view.GetPageIndex(page), new_item.name)
        return new_item
        
    def OpenFile(self, item):
        if item in self._opened_files:
            self._tabs_view.SetSelection(self._tabs_view.GetPageIndex(self._tabs[item]))
        elif not item.dir and not item in self._opened_files:
            self._opened_files.append(item)
            # then we create new tab in the tabs view
            if self._tabs_view:
                if item.type == "Context" or item.type == "Scale":
                    newtab = contextgrid.ContextGrid(self._tabs_view)
                    newtab.SetTable(contextgrid.ContextTable(item, self))
                elif item.type == "Many-valued context":
                    newtab = contextgrid.MVContextGrid(self._tabs_view)
                    newtab.SetTable(contextgrid.MVContextTable(item, self))
                else:
                    newtab = wx.TextCtrl(self._tabs_view, -1, "", size=(200, 100), 
                                     style=wx.TE_MULTILINE|wx.TE_READONLY)
                    newtab.SetFont(wx.Font(14, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL,
                                       wx.FONTWEIGHT_NORMAL))
                    newtab.LoadFile(item.path)
                
                # TODO:
                newtab.ref = item
                self._tabs[item] = newtab
                    
                self._tabs_view.AddPage(newtab, item.name, True)
                
    def CloseFile(self, item):
        self._opened_files.remove(item)
        item.tab = None
