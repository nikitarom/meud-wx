# -*- coding: utf-8 -*-
"""Main starting point for meud"""

import os

import wx
import wx.aui

import fca

import project

def MsgDlg(window, string, caption='meud', style=wx.YES_NO|wx.CANCEL):
    """Common MessageDialog."""
    dlg = wx.MessageDialog(window, string, caption, style)
    result = dlg.ShowModal()
    dlg.Destroy()
    return result

class MainFrame(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent=parent, id=-1, title=title)
        self.SetupMenubar()
        
        self.sp = wx.SplitterWindow(self)
        
        #self.toolBar = self.CreateToolBar()
        #self.openButton = wx.Button(self.toolBar, wx.NewId(), "Open")
        #self.toolBar.AddControl(self.openButton)
        #self.toolBar.Realize()
        
        self.tree = wx.TreeCtrl(self.sp, size=(200,-1),
                                style=wx.TR_DEFAULT_STYLE | wx.TR_EDIT_LABELS)
        
        self.nb = wx.aui.AuiNotebook(self.sp)
        
        self.sp.SetMinimumPaneSize(10)
        self.sp.SplitVertically(self.tree, self.nb, 10)
        
        self.current_project = None
        self.project_dir = None
        self.projectdirty = False
        self.root = None
        
    def SetupMenubar(self):
        """docstring for SetupMenubar"""
        self.mainmenu = wx.MenuBar()
        menu = wx.Menu()
        self.mainmenu.Append(menu, "&File")
        
        item = menu.Append(wx.NewId(), "&New Project...\tCtrl+N", "Create new project")
        self.Bind(wx.EVT_MENU, self.OnProjectNew, item)
        
        item = menu.Append(wx.NewId(), "&Open Project...\tCtrl+O")
        self.Bind(wx.EVT_MENU, self.OnProjectOpen, item)
        
        self.itemSaveProject = menu.Append(wx.NewId(), "&Save Project",
                                            "Save changes to project")
        self.itemSaveProject.Enable(False)
        self.Bind(wx.EVT_MENU, self.OnProjectSave, self.itemSaveProject)
                
        item = menu.Append(wx.NewId(), "&Import...", "Add file to project")
        self.Bind(wx.EVT_MENU, self.OnImport, item)
        
        self.SetMenuBar(self.mainmenu)
    
    def CheckProjectDirty(self):
        """Were the current project changed? If so, save it before."""
        open_it = True
        if self.projectdirty:
            # save the current project first.
            result = MsgDlg(self, "The project has been changed.  Save?")
            if result == wx.ID_YES:
                self.project_save()
            if result == wx.ID_CANCEL:
                open_it = False
        return open_it

    def project_open(self, project_dir):
        """Open and process a meud project"""
        try:
            self.current_project = project.load_project(project_dir)
            self.project_dir = project_dir
            
            self.tree.DeleteAllItems()
            self.SetTitle(" - ".join(["meud", self.current_project.name]))
            
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
            
            self.projectdirty = False
            self.itemSaveProject.Enable(True)
        except IOError:
            pass
            
    def project_save(self):
        """Save a meud project"""
        try:
            project.save_project(self.current_project, self.project_dir)
            self.projectdirty = False
        except IOError:
            MsgDlg(self, 'There was an error saving the new project file.', 'Error!', wx.OK)
        
    def OnProjectNew(self, event):
        """Create a new meud project."""
        open_it = self.CheckProjectDirty()
        if open_it:
            dlg = wx.TextEntryDialog(self, "Name for new project:", "New project",
                                     "New project", wx.OK|wx.CANCEL)
            if dlg.ShowModal() == wx.ID_OK:
                newproj = project.Project(dlg.GetValue())
                dlg.Destroy()
                dlg = wx.DirDialog(self, message="Choose a folder to contain new project")
                if dlg.ShowModal() == wx.ID_OK:
                    try:
                        # save the project file.
                        project.save_project(newproj, os.path.join(dlg.GetPath(), newproj.name))
                        self.project_open(os.path.join(dlg.GetPath(), newproj.name))
                    except IOError:
                        MsgDlg(self, "There was an error saving the new project file.",
                                "Error!", wx.OK)
            dlg.Destroy()
            
    def OnProjectOpen(self, event):
        """Open a meud file."""
        open_it = self.CheckProjectDirty()
        if open_it:
            dlg = wx.DirDialog(self, message="Choose a folder containing a project to open.")
            if dlg.ShowModal() == wx.ID_OK:
                self.project_open(dlg.GetPath())
            dlg.Destroy()
    
    def OnProjectSave(self, event):
        """Save a current meud project"""
        if self.projectdirty:
            self.project_save()
    
    def OnImport(self, event):
        """Import scale, context or mvcontext to current project"""
        dlg = wx.FileDialog(self, 'Choose a file to import.', '.', '', '*.cxt', wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = os.path.split(dlg.GetPath())
            self.current_project.add_element(fca.Scale(fca.read_cxt(dlg.GetPath())))
            self.project_save()
            

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