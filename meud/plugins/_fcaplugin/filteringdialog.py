import os

import wx

import fca
import fca.algorithms.filtering as filtering
from fca.readwrite import uread_xml

def GetFilteredConcepts(item):
    dialog = FilteringDialog() 
    result = dialog.ShowModal()
    if result == wx.ID_OK:
        options = dialog.GetOptions()
        cs = uread_xml(item.path)
        
        precessor = item.precessor
        while not precessor.type == "Context":
            precessor = precessor.precessor
        (root, ext) = os.path.splitext(precessor.name)
        if ext == ".cxt":
            cxt = fca.read_cxt(precessor.path)
        elif ext == ".txt":
            cxt = fca.read_txt(precessor.path)
        cs.context = cxt
        new_cs = fca.filter_concepts(cs, options["function"], options["mode"], options["opt"])
        
        default_path = item.path[:-4] + "-filtered.xml"
        newpath = default_path
        i = 1
        while (os.path.exists(newpath)):
            newpath = default_path[:-4] + "-{0}".format(i) + newpath[-4:]
            i += 1
        fca.write_xml(newpath, new_cs)
        newpath = [newpath]
    else:
        newpath = []
        
    dialog.Destroy()
    
    return newpath

class FilteringDialog(wx.Dialog):
    
    def __init__(self):
        self.functions = filtering.get_compute_functions()
        modes = filtering.get_modes()
        
        wx.Dialog.__init__(self, None, -1, "Filtering", size=(300,200))
        self.CenterOnScreen()
        
        panel = wx.Panel(self, -1)
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        hSizer.Add(wx.StaticText(panel, -1, "Index: "), 1)
        
        samples = self.functions.keys()
        self.indexChoice = wx.Choice(panel, -1, (200, 100), choices = samples)
        self.indexChoice.Select(0)
        hSizer.Add(self.indexChoice, 3, wx.EXPAND | wx.RIGHT)
        
        mainSizer.Add(hSizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
        mainSizer.Add((10, 10), 1)
        
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        hSizer.Add(wx.StaticText(panel, -1, "Mode: "), 1)
        self.modeChoice = wx.Choice(panel, -1, (100, 50), choices = modes)
        self.modeChoice.Select(0)
        hSizer.Add(self.modeChoice, 3)
        
        mainSizer.Add(hSizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
        mainSizer.Add((10, 10), 1)
        
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        hSizer.Add(wx.StaticText(panel, -1, "Option: "), 1)
        self.optionText = wx.TextCtrl(panel, -1, "1", size=(125, -1))
        hSizer.Add(self.optionText, 3)
        
        mainSizer.Add(hSizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
        mainSizer.Add((10, 10), 1)
        
        mainSizer.Add(wx.StaticLine(panel), 0,
                        wx.EXPAND | wx.TOP | wx.BOTTOM, 5)      
        
        self.okButton = wx.Button(panel, wx.ID_OK, "OK")
        cancelButton = wx.Button(panel, wx.ID_CANCEL, "Cancel")
        cancelButton.SetDefault()
        
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(self.okButton)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(cancelButton)
        btnSizer.Add((20, 20), 1)
        
        mainSizer.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        
        panel.SetSizer(mainSizer)
        
        mainSizer.Fit(self)
        mainSizer.SetSizeHints(self)
        
    def GetOptions(self):
        return {"function" : self.functions[self.indexChoice.GetStringSelection()],
                "mode" : self.modeChoice.GetStringSelection(),
                "opt" : float(self.optionText.GetValue())}
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    dialog = FilteringDialog() 
    result = dialog.ShowModal()
    dialog.Destroy() 