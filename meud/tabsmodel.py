"""
Tabs Model
"""
import wx
from wx.lib.scrolledpanel import ScrolledPanel

import fca
from fca.readwrite import uread_xml

import contextgrid
import diagramview
import conceptsystemgrid

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
                elif item.type == "Image":
                    png = wx.Image(item.path, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
                    newtab = ScrolledPanel(self._tabs_view, -1)
                    wx.StaticBitmap(newtab, -1, png, (10, 10), (png.GetWidth(), png.GetHeight()))
                    newtab.SetScrollRate(20,20)
                    newtab.SetVirtualSize((png.GetWidth() + 20, png.GetHeight() + 20))
                elif item.type == "Concepts":
                    dlg = wx.SingleChoiceDialog(
                            None, 'What do you want to do?', 'Choose variant',
                            ["View diagram", "View concepts", "Table"], 
                            wx.CHOICEDLG_STYLE
                            )
                    if dlg.ShowModal() == wx.ID_OK:
                        what = dlg.GetStringSelection()
                    else:
                        what = "Do nothing"
                    dlg.Destroy()
                        
                    if what == "View concepts":
                        newtab = wx.TextCtrl(self._tabs_view, -1, "", size=(200, 100), 
                                         style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP)
                        newtab.SetFont(wx.Font(12, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL,
                                           wx.FONTWEIGHT_NORMAL))
                        cs = uread_xml(item.path)
                        for concept in cs:
                            s = u"[{0} : {1}] @ {2}\n".format(", ".join(concept.extent),
                                                             ", ".join(concept.intent),
                                                             concept.meta)
                            newtab.WriteText(s)
                    elif what == "View diagram":
                        newtab = diagramview.DiagramWindow(self._tabs_view, 
                                                           wx.NewId(),
                                                           filename=item.name,
                                                           path=item.path)
                    elif what == "Table":
                        table = conceptsystemgrid.ConceptSystemTable(uread_xml(item.path))
                        newtab = conceptsystemgrid.ConceptSystemGrid(self._tabs_view)
                        newtab.SetTable(table)
                    elif what == "Do nothing":
                        self._opened_files.pop()
                        return
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
