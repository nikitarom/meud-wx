"""FCA plugin"""
import os.path

import wx

import fca

from _plugin import Plugin

class FCAPlugin(Plugin):
    name = "FCA"
    
    def get_actions(self, item):
        if item.type == "Context":
            return ["Save concepts"]
    
    def do_action(self, item, action):
        if action == "Save concepts":
            (root, ext) = os.path.splitext(item.name)
            if ext == ".cxt":
                cxt = fca.read_cxt(item.path)
            elif ext == ".txt":
                cxt = fca.read_txt(item.path)
            cs = fca.norris(cxt)
            
            default_path = "".join([item.path[:-3], "xml"])
            newpath = default_path
            i = 1
            while (os.path.exists(newpath)):
                newpath = default_path[:-4] + "-{0}".format(i) + newpath[-4:]
                i += 1
            fca.write_xml(newpath, cs)
            
            dlg = wx.MessageDialog(None, "Concepts have been stored in " + newpath,
                               "Done",
                               wx.OK | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            dlg.Destroy()
            
            return [newpath]
