#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main starting point for meud"""

import os
import os.path

import wx
import wx.aui

import fca

import workspaceview
import workspacemodel
import tabsmodel
from scalingdialog import ScalingDialog
from tabsview import TabsView

from globals_ import files_categories, DEBUG, workspace_path

def MsgDlg(window, string, caption='meud', style=wx.YES_NO|wx.CANCEL):
    """Common MessageDialog."""
    dlg = wx.MessageDialog(window, string, caption, style)
    result = dlg.ShowModal()
    dlg.Destroy()
    return result

class MainFrame(wx.Frame):
    
    def __init__(self, parent, title):   
        wx.Frame.__init__(self, parent=parent, id=-1, title=title, size=(800, 600))
        self.CenterOnScreen()
        
        self.sp = wx.SplitterWindow(self)
        
        self.tree = workspaceview.WorkspaceView(self.sp)
        if DEBUG:
            w_path = os.path.abspath(workspace_path)
            self.tree.SetModel(workspacemodel.WorkspaceModel(w_path))
        self.nb = TabsView(self.sp)
        tmodel = tabsmodel.TabsModel()
        tmodel._path = w_path # !!!
        self.nb.SetModel(tmodel)
        self.tree.SetTabsModel(tmodel)
        
        self.sp.SetMinimumPaneSize(10)
        self.sp.SplitVertically(self.tree, self.nb, 200)
        
        #self.SetupMenubar()
        
    def SetupMenubar(self):
        """docstring for SetupMenubar"""
        self.mainmenu = wx.MenuBar()
        
        # File menu #
        menu = wx.Menu()
        self.mainmenu.Append(menu, "&Workspace")
        item = menu.Append(wx.NewId(), "&Refresh...\tF5", "Refresh workspace")
        # self.Bind(wx.EVT_MENU, self.tree.OnRefresh, item)
        
        # File menu #
        menu = wx.Menu()
        self.mainmenu.Append(menu, "&File")
        
        # Scaling menu #
        menu = wx.Menu()
        self.mainmenu.Append(menu, "&Scaling")
        
        item = menu.Append(wx.NewId(), "Sca&le\tCtrl+l", "Scale current many-valued context")
        self.Bind(wx.EVT_MENU, self.OnScaling, item)
        
        self.SetMenuBar(self.mainmenu)
                
    def OnScaling(self, event):
        item = self.tree.GetSelection()
        data = self.tree.GetItemData(item).GetData()
        if isinstance(data, fca.ManyValuedContext):
            dlg = ScalingDialog(data, self.current_project.get_scales())
            if dlg.ShowModal() == wx.ID_OK:
                resulted_context = fca.scale_mvcontext(data, dlg.GetListOfScales())
                dlg.Destroy()
                self.current_project.add_element(resulted_context)
                self.tree.add_new_element("contexts", resulted_context)
                self.current_project.projectdirty = True
                
                
class App(wx.App):
    
    def OnInit(self):
        self.frame = MainFrame(parent=None, title="meud")
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

        
def main():
    app = App(redirect=False)
    app.MainLoop()

if __name__ == "__main__":
    main()