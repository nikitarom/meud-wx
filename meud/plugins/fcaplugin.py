"""FCA plugin"""
import os.path

import wx

import fca

from _plugin import Plugin
import _fcaplugin

class FCAPlugin(Plugin):
    name = "FCA"
    
    def get_actions(self, item):
        if item.type == "Context":
            return ["Save concepts"]
        if item.type == "Many-valued context":
            return ["Scale"]
        if item.type == "Concepts":
            return ["Filter", "Save diagram as .dot file"]
    
    def do_action(self, item, workspace, action):
        if action == "Save concepts":
            return self.SaveConcepts(item)
        elif action == "Scale":
            return self.ScaleMVContext(item, workspace)
        elif action == "Filter":
            pass
        elif action == "Save diagram as .dot file":
            return self.SaveDiagramAsDotFile(item, workspace)
        
    def SaveDiagramAsDotFile(self, item, workspace):
        default_path = "".join([item.path[:-3], "dot"])
        newpath = default_path
        i = 1
        while (os.path.exists(newpath)):
            newpath = default_path[:-4] + "-{0}".format(i) + newpath[-4:]
            i += 1
        cl = fca.read_xml(item.path)
        fca.write_dot(cl, newpath)
        
        dlg = wx.MessageDialog(None, ".dot file has been saved to " + newpath,
                                "Done",
                                wx.OK | wx.ICON_INFORMATION
                                )
        dlg.ShowModal()
        dlg.Destroy()
        
        return [newpath]
        
    def ScaleMVContext(self, item, workspace):
        return _fcaplugin.GetScaledContext(item, workspace)
        
        
    def SaveConcepts(self, item):
        (root, ext) = os.path.splitext(item.name)
        if ext == ".cxt":
            cxt = fca.read_cxt(item.path)
        elif ext == ".txt":
            cxt = fca.read_txt(item.path)
        cl = fca.ConceptLattice(cxt)
        number_of_concepts = len(cl)
    
        default_path = "".join([item.path[:-3], "xml"])
        newpath = default_path
        i = 1
        while (os.path.exists(newpath)):
            newpath = default_path[:-4] + "-{0}".format(i) + newpath[-4:]
            i += 1
        fca.write_xml(newpath, cl)
            
        dlg = wx.MessageDialog(None, str(number_of_concepts) +\
                                " concepts have been stored in " + newpath,
                                "Done",
                                wx.OK | wx.ICON_INFORMATION
                                )
        dlg.ShowModal()
        dlg.Destroy()
        
        return [newpath]