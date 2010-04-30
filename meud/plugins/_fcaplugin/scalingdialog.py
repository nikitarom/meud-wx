#!/usr/bin/env python
# encoding: utf-8
import os

import wx

import fca

from _loadscaledialog import LoadScaleDialog

class ScalingDialog(wx.Dialog):
    
    def __init__(self, item, workspace):
        self._workspace = workspace
        mvcontext = fca.read_mv_txt(item.path)
        
        wx.Dialog.__init__(self, None, -1, "Scaling")
        self.CenterOnScreen()
        
        panel = wx.Panel(self, -1)
        self._context = mvcontext
        self._scales = []
        
        self.scales_names = [scale.name for scale in self._scales]
        self.assigned_attributes = dict([(name, []) for name in self.scales_names])
        self.remain_attributes = mvcontext.attributes[:] #!!!

        firstColLabel = wx.StaticText(panel, -1, "Scales")
        secondColLabel = wx.StaticText(panel, -1, "Assigned Attributes")
        thirdColLabel = wx.StaticText(panel, -1, "Remaining Attributes")
        
        self.ScalesLb = wx.ListBox(panel, -1, size=(-1, 200), style=wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.OnScaleSelected, self.ScalesLb)
        
        loadScaleBtn = wx.Button(panel, wx.NewId(), "Load Scale...", (10,20))
        self.Bind(wx.EVT_BUTTON, self.OnLoadScaleButton, loadScaleBtn)
        
        self.ScaledAttrLb = wx.ListBox(panel, -1, size=(-1, 200), style=wx.LB_EXTENDED)
        self.RemainAttrsLb = wx.ListBox(panel, -1, size=(-1, 200), style=wx.LB_EXTENDED)
        
        rightArrowBtn = wx.Button(panel, wx.NewId(), "=>", size=(40, 20))
        self.Bind(wx.EVT_BUTTON, self.OnRightButton, rightArrowBtn)
        leftArrowBtn = wx.Button(panel, wx.NewId(), "<=", size=(40, 20))
        self.Bind(wx.EVT_BUTTON, self.OnLeftButton, leftArrowBtn)
        
        self.okButton = wx.Button(panel, wx.ID_OK, "OK")
        self.okButton.Disable()
        cancelButton = wx.Button(panel, wx.ID_CANCEL, "Cancel")
        cancelButton.SetDefault()
        
        # mainSizer is the top-level sizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        colsSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        colsSizer.Add((20,20), 1)
        
        box1 = wx.BoxSizer(wx.VERTICAL)
        box1.Add(firstColLabel)
        box1.Add(self.ScalesLb)
        box1.Add(loadScaleBtn)
        colsSizer.Add(box1)
        
        colsSizer.Add((20,20), 1)
        
        box2 = wx.BoxSizer(wx.VERTICAL)
        box2.Add(secondColLabel)
        box2.Add(self.ScaledAttrLb)
        colsSizer.Add(box2)
        
        box_ = wx.BoxSizer(wx.VERTICAL)
        box_.Add(rightArrowBtn, 1)
        box_.Add(leftArrowBtn, 1)
        colsSizer.Add(box_, 0, wx.ALIGN_CENTER_VERTICAL)
        
        box3 = wx.BoxSizer(wx.VERTICAL)
        box3.Add(thirdColLabel)
        box3.Add(self.RemainAttrsLb)
        colsSizer.Add(box3)
        
        colsSizer.Add((20,20), 1)
        
        mainSizer.Add(colsSizer, 0, wx.EXPAND, 20)
        
        mainSizer.Add(wx.StaticLine(panel), 0,
                        wx.EXPAND | wx.TOP | wx.BOTTOM, 5)      
        
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
        
        self.RemainAttrsLb.Set(self.remain_attributes)
        self.ScalesLb.Set(self.scales_names)
        if len(self._scales) != 0:
            self.ScalesLb.SetSelection(0)
            self.selected_scale = self.ScalesLb.GetStringSelection()
    
    def OnRightButton(self, event):
        """docstring for OnRightButton"""
        selection = self.ScaledAttrLb.GetSelections()
        selected_strings = [self.assigned_attributes[self.selected_scale][i] for i in selection]
        self.remain_attributes.extend(selected_strings)
        [self.RemainAttrsLb.Append(self.assigned_attributes[self.selected_scale][i])
                                                                for i in selection]
        for s in selected_strings:
            self.assigned_attributes[self.selected_scale].remove(s)
        self.ScaledAttrLb.Set(self.assigned_attributes[self.selected_scale])
        if self.okButton.Enabled:
            self.okButton.Disable()
        
    def OnLeftButton(self, event):
        """docstring for OnLeftButton"""
        selection = self.RemainAttrsLb.GetSelections()
        selected_strings = [self.remain_attributes[i] for i in selection]
        if not self.selected_scale in self.assigned_attributes.keys():
            self.assigned_attributes[self.selected_scale] = []
        self.assigned_attributes[self.selected_scale].extend(selected_strings)
        [self.ScaledAttrLb.Append(self.remain_attributes[i]) for i in selection]
        for s in selected_strings:
            self.remain_attributes.remove(s)
        self.RemainAttrsLb.Set(self.remain_attributes)
        if len(self.remain_attributes) == 0:
            self.okButton.Enable()
            
    def OnScaleSelected(self, event):
        """docstring for OnScaleSelected"""
        self.selected_scale = event.GetString()
        if not self.selected_scale in self.assigned_attributes.keys():
            self.assigned_attributes[self.selected_scale] = []
        self.ScaledAttrLb.Set(self.assigned_attributes[self.selected_scale])
        
    def OnLoadScaleButton(self, event):
        dlg = LoadScaleDialog(self._workspace, self.GetParent())
        dlg.CenterOnScreen()

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
    
        if val == wx.ID_OK:
            item = dlg.GetScale()
            if item and not item.dir:
                context = fca.read_cxt(item.path)
                scale = fca.Scale(context)
                scale.name = item.name
                self._scales.append(scale)
                self.scales_names.append(item.name)
                self.ScalesLb.Set(self.scales_names)
                self.ScalesLb.Select(0)
                self.selected_scale = self.ScalesLb.GetString(0)

        dlg.Destroy()
    
    def GetListOfScales(self):
        """Invoked outside of the dialog. Returns list of scales for each attribute.
        
        Usually after invoking this method, dialog should be destroyed
        """
        ret = []
        for i in range(len(self._context.attributes)):
            for scale in self._scales:
                if self._context.attributes[i] in self.assigned_attributes[scale.name]:
                    ret.append(scale)
                    break
        return ret 

def GetScaledContext(item, workspace):
    dialog = ScalingDialog(item, workspace) 
    result = dialog.ShowModal()
    if result == wx.ID_OK:
        scales = dialog.GetListOfScales()
        mvcontext = fca.read_mv_txt(item.path)
        context = fca.scale_mvcontext(mvcontext, scales)
        
        default_path = item.path[:-4] + "-scaled.cxt"
        newpath = default_path
        i = 1
        while (os.path.exists(newpath)):
            newpath = default_path[:-4] + "-{0}".format(i) + newpath[-4:]
            i += 1
        fca.write_cxt(context, newpath)
        newpath = [newpath]
    else:
        newpath = []
        
    dialog.Destroy()
    return newpath

#if __name__ == '__main__':
#    app = wx.PySimpleApp()
#    t = [[2, 1, 2, 3],\
#        [1, 2, 3, 1],\
#        [2, 1, 3, 1],\
#        [2, 3, 3, 2]]
#    objs = [1, 2, 3, 4]
#    attrs = ['a', 'b', 'c', 'd']
#    c = fca.ManyValuedContext(t, objs, attrs)
#    ct = [[True, False],\
#         [False, True]]
#    objs = ['value>7', 'value<2']
#    attrs = ['>7', '<2']
#    c1 = fca.Context(ct, objs, attrs)
#    s = fca.Scale(c1)
#    s.name = "scale1"
#    ct = [[False, False],\
#         [False, True]]
#    objs = ['value>7', 'value<2']
#    attrs = ['>7', '<2']
#    c2 = fca.Context(ct, objs, attrs)
#    s2 = fca.Scale(c2)
#    s2.name = "scale2"
#    dialog = ScalingDialog(c) 
#    result = dialog.ShowModal()
#    dialog.Destroy() 

