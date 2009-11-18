#!/usr/bin/env python
# encoding: utf-8

import wx
import wx.grid

import fca

class ContextTable(wx.grid.PyGridTableBase):
    
    def __init__(self, context):
        wx.grid.PyGridTableBase.__init__(self)
        self.context = context
        
    def GetNumberRows(self):
        return len(self.context)
        
    def GetNumberCols(self):
        return len(self.context[0])
        
    def GetColLabelValue(self, col):
        return self.context.attributes[col]
        
    def GetRowLabelValue(self, row):
        return self.context.objects[row]
        
    def IsEmptyCell(self, row, col):
        return False
        
    def GetValue(self, row, col):
        if self.context[row][col]:
            return 1
        else:
            return 0
        
    def SetValue(self, row, col, value):
        self.context[row][col] = (int(value) == 1)
        
        
class MVContextTable(wx.grid.PyGridTableBase):

    def __init__(self, context):
        wx.grid.PyGridTableBase.__init__(self)
        self.context = context

    def GetNumberRows(self):
        return len(self.context)

    def GetNumberCols(self):
        return len(self.context[0])

    def GetColLabelValue(self, col):
        return self.context.attributes[col]

    def GetRowLabelValue(self, row):
        return self.context.objects[row]

    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        return self.context[row][col]

    def SetValue(self, row, col, value):
        self.context[row][col] = int(value)

class ContextGrid(wx.grid.Grid):
    
    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1)
        
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnGridCellDataChange, self)
        
    def SetTable(self, table):
        self.element = table.context
        super(ContextGrid, self).SetTable(table)
        
    def OnGridCellDataChange(self, event):
        pass
    
    
class MVContextGrid(wx.grid.Grid):

    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1)
        
    def SetTable(self, table):
        self.element = table.context
        super(MVContextGrid, self).SetTable(table)


if __name__ == '__main__':
    pass

