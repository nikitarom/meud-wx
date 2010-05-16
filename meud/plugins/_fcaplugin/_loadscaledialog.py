import wx

tree_settings = {
"size" : (200, 300),
"style" : wx.TR_DEFAULT_STYLE | wx.TR_FULL_ROW_HIGHLIGHT
}

class ScaleTree(wx.TreeCtrl):
    """
    classdocs
    """

    def __init__(self, workspace, parent=None):
        """
        Constructor
        """
        super(ScaleTree, self).__init__(parent, **tree_settings)

        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
        il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        self.SetImageList(il)
        self._imagelist = il
        
        self._wroot = workspace.FilterType("Scale")
        new_tree_item = self.AddRoot(self._wroot.name)
        self.SetPyData(new_tree_item, workspace._root)
        
        self.SetItemImage(new_tree_item, 0, wx.TreeItemIcon_Normal)
        self.SetItemImage(new_tree_item, 1, wx.TreeItemIcon_Expanded)
        self.Walk(self._wroot, self.GetRootItem())
        
        self.Expand(new_tree_item)

    def Walk(self, parent, treeparent):
        for item in parent.children:
            treeitem = self.AddItem(treeparent, item)
            self.Walk(item, treeitem)
            
    def AddItem(self, parent, item):
        new_tree_item = self.AppendItem(parent, item.name)
        self.SetPyData(new_tree_item, item)
        if item.dir:
            self.SetItemImage(new_tree_item, 0, wx.TreeItemIcon_Normal)
            self.SetItemImage(new_tree_item, 1, wx.TreeItemIcon_Expanded)
        else:
            self.SetItemImage(new_tree_item, 2, wx.TreeItemIcon_Normal)
        return new_tree_item
        
class LoadScaleDialog(wx.Dialog):
    
    def __init__(self, workspace, parent=None):

        wx.Dialog.__init__(self, parent, wx.NewId(), "Load scale from workspace", size=(550, 400),
                         style=wx.DEFAULT_DIALOG_STYLE)
        
        self.CenterOnScreen()
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.tree = ScaleTree(workspace, self)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        
        sizer.Add(self.tree, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
        
        self._scale = None
        
    def GetScale(self):
        return self._scale 
    
    def OnSelChanged(self, event):
        item = event.GetItem()
        self._scale = self.tree.GetPyData(item)
        event.Skip()