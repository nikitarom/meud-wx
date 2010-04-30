#!/usr/bin/env python
# encoding: utf-8

import wx

import fca

class ScalingDialog(wx.Dialog):
    
    def __init__(self, mvcontext, scales):
        wx.Dialog.__init__(self, None, -1, "Scaling")
        self.CenterOnScreen()
        
        panel = wx.Panel(self, -1)
        self._context = mvcontext
        self._scales = scales
        
        self.scales_names = [scale.name for scale in scales]
        self.assigned_attributes = dict([(name, []) for name in self.scales_names])
        self.remain_attributes = mvcontext.attributes[:] #!!!

        firstColLabel = wx.StaticText(panel, -1, "Scales")
        secondColLabel = wx.StaticText(panel, -1, "Assigned Attributes")
        thirdColLabel = wx.StaticText(panel, -1, "Remaining Attributes")
        
        self.ScalesLb = wx.ListBox(panel, -1, size=(-1, 200), style=wx.LB_SINGLE | wx.MAXIMIZE_BOX,
                                choices=self.scales_names)
        self.Bind(wx.EVT_LISTBOX, self.OnScaleSelected, self.ScalesLb)
        self.ScalesLb.SetSelection(0)
        self.selected_scale = self.ScalesLb.GetStringSelection()
        self.ScaledAttrLb = wx.ListBox(panel, -1, size=(-1, 200), style=wx.LB_MULTIPLE | wx.LB_EXTENDED | wx.MAXIMIZE_BOX)
        self.RemainAttrsLb = wx.ListBox(panel, -1, size=(-1, 200), style=wx.LB_MULTIPLE | wx.LB_EXTENDED | wx.MAXIMIZE_BOX,
                                    choices=self.remain_attributes)
        
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
        self.ScaledAttrLb.Set(self.assigned_attributes[self.selected_scale])
    
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

if __name__ == '__main__':
    app = wx.PySimpleApp()
    t = [[2, 1, 2, 3],\
        [1, 2, 3, 1],\
        [2, 1, 3, 1],\
        [2, 3, 3, 2]]
    objs = [1, 2, 3, 4]
    attrs = ['a', 'b', 'c', 'd']
    c = fca.ManyValuedContext(t, objs, attrs)
    ct = [[True, False],\
         [False, True]]
    objs = ['value>7', 'value<2']
    attrs = ['>7', '<2']
    c1 = fca.Context(ct, objs, attrs)
    s = fca.Scale(c1)
    s.name = "scale1"
    ct = [[False, False],\
         [False, True]]
    objs = ['value>7', 'value<2']
    attrs = ['>7', '<2']
    c2 = fca.Context(ct, objs, attrs)
    s2 = fca.Scale(c2)
    s2.name = "scale2"
    dialog = ScalingDialog(c, [s, s2]) 
    result = dialog.ShowModal()
    dialog.Destroy() 

