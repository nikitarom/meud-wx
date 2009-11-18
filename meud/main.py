#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main starting point for meud"""

import os

import wx

import fca

import project
import projecttree
from scalingdialog import ScalingDialog

from globals_ import files_categories

def MsgDlg(window, string, caption='meud', style=wx.YES_NO|wx.CANCEL):
    """Common MessageDialog."""
    dlg = wx.MessageDialog(window, string, caption, style)
    result = dlg.ShowModal()
    dlg.Destroy()
    return result

class MainFrame(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent=parent, id=-1, title=title, size=(800, -1))
        self.CenterOnScreen()
        
        self.sp = wx.SplitterWindow(self)
        
        self.tree = projecttree.ProjectTree(self.sp)
        
        self.sp.SetMinimumPaneSize(10)
        self.sp.SplitVertically(self.tree, self.tree.nb, 10)
        
        self.current_project = None
        self.project_dir = None
        self.root = None
        
        self.SetupMenubar()
        
    def SetupMenubar(self):
        """docstring for SetupMenubar"""
        self.mainmenu = wx.MenuBar()
        # Project menu #
        menu = wx.Menu()
        self.mainmenu.Append(menu, "&Project")
        
        item = menu.Append(wx.NewId(), "&New Project...\tCtrl+N", "Create new project")
        self.Bind(wx.EVT_MENU, self.OnProjectNew, item)
        
        item = menu.Append(wx.NewId(), "&Open Project...\tCtrl+O")
        self.Bind(wx.EVT_MENU, self.OnProjectOpen, item)
        
        self.itemSaveProject = menu.Append(wx.NewId(), "&Save Project",
                                            "Save changes to project")
        self.itemSaveProject.Enable(False)
        self.Bind(wx.EVT_MENU, self.OnProjectSave, self.itemSaveProject)
        
        # File menu #
        menu = wx.Menu()
        self.mainmenu.Append(menu, "&File")
        
        item = menu.Append(wx.NewId(), "&Import...\tCtrl+I", "Add file to project")
        self.Bind(wx.EVT_MENU, self.OnImport, item)
        
        item = menu.Append(wx.NewId(), "&Remove\tCtrl+R", "Remove selected file from project")
        self.Bind(wx.EVT_MENU, self.tree.OnFileRemove, item)
        
        # Scaling menu #
        menu = wx.Menu()
        self.mainmenu.Append(menu, "&Scaling")
        
        item = menu.Append(wx.NewId(), "Sca&le\tCtrl+l", "Scale current many-valued context")
        self.Bind(wx.EVT_MENU, self.OnScaling, item)
        
        self.SetMenuBar(self.mainmenu)
    
    def CheckProjectDirty(self):
        """Were the current project changed? If so, save it before."""
        open_it = True
        if self.current_project == None:
            return True
        if self.current_project.projectdirty:
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
            
            self.SetTitle(" - ".join(["meud", self.current_project.name]))
            self.tree.set_project(self.current_project, self.project_dir)

            self.current_project.projectdirty = False
            self.itemSaveProject.Enable(True)
        except IOError:
            pass
            
    def project_save(self):
        """Save a meud project"""
        try:
            project.save_project(self.current_project, self.project_dir)
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
        if self.current_project.projectdirty:
            self.project_save()
    
    def OnImport(self, event):
        """Import scale, context or mvcontext to current project"""
        choices = files_categories.values()
        dialog = wx.SingleChoiceDialog(self, "Choose a category of the file you trying to import",
                                        "Choose a category", choices) 
        if dialog.ShowModal() == wx.ID_OK:
            category = dialog.GetStringSelection()
            wildcard = "*.cxt files (*.cxt)|*.cxt|" \
                        "Tab-separated files (*.txt)|*.txt|" \
                        "All files (*.*)|*.*"
            dlg = wx.FileDialog(self, 'Choose a file to import.', '.', '', wildcard,
                                wx.OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                ext = os.path.splitext(path)[1]
                if category == "Scales" and ext==".cxt":
                    new_element = fca.Scale(fca.read_cxt(path))
                    self.current_project.add_element(new_element)
                    self.tree.add_new_element("scales", new_element)
                elif category == "Contexts":
                    if ext==".cxt":
                            new_element = fca.read_cxt(path)
                    elif ext==".txt":
                            new_element = fca.read_txt(path)
                    self.current_project.add_element(new_element)
                    self.tree.add_new_element("contexts", new_element)
                elif category == "Many-valued contexts":
                    new_element = fca.read_mv_txt(path)
                    self.current_project.add_element(new_element)
                    self.tree.add_new_element("mvcontexts", new_element)
                elif category == "Concept Systems":
                    new_element = fca.read_xml(path)
                    self.current_project.add_element(new_element)
                    self.tree.add_new_element("concept_systems", new_element)
                else:
                    MsgDlg(self, 'Not supported yet', 'Error!', wx.OK)
                self.project_save()
                
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