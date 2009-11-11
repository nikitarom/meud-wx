# -*- coding: utf-8 -*-
"""Main starting point for meud"""

import wx
import wx.aui

class MainFrame(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent=parent, id=-1, title=title)
        self.sp = wx.SplitterWindow(self)
        
        self.toolBar = self.CreateToolBar()
        self.openButton = wx.Button(self.toolBar, wx.NewId(), "Open")
        self.toolBar.AddControl(self.openButton)
        self.toolBar.Realize()
        
        self.tree = wx.TreeCtrl(self.sp, size=(200,300))
        root = self.tree.AddRoot("workspace")
        self.tree.AppendItem(root, "Test1")
        self.tree.Expand(root)
        
        self.nb = wx.aui.AuiNotebook(self.sp)

        page = wx.TextCtrl(self.nb, -1, "111", style=wx.TE_MULTILINE)
        self.nb.AddPage(page, "Welcome1")
        page = wx.TextCtrl(self.nb, -1, "222", style=wx.TE_MULTILINE)
        self.nb.AddPage(page, "Welcome2")
        
        self.sp.SetMinimumPaneSize(10)
        self.sp.SplitVertically(self.tree, self.nb, -100)
        

class App(wx.App):
    
    def OnInit(self):
        self.frame = MainFrame(parent=None, title="meud")
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True
        
def main():
    app = App(redirect=False)
    app.MainLoop()

if __name__ == '__main__':
    main()