#!/usr/bin/env python
# encoding: utf-8

import wx
import wx.grid

class ConceptSystemTable(wx.grid.PyGridTableBase):
    
    def __init__(self, concept_system):
        wx.grid.PyGridTableBase.__init__(self)
        self.concept_system = concept_system
        
    def GetNumberRows(self):
        return len(self.concept_system)
        
    def GetNumberCols(self):
        return 2
        
    def GetColLabelValue(self, col):
        return ["Extent", "Intent"][col]
        
    def GetRowLabelValue(self, row):
        return row + 1
        
    def IsEmptyCell(self, row, col):
        return False
        
    def GetValue(self, row, col):
        if col == 0:
            return str(self.concept_system[row].extent)
        else:
            return str(self.concept_system[row].intent)
        
    def SetValue(self, row, col, value):
        pass


class ConceptSystemGrid(wx.grid.Grid):

    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1)
        
    def SetTable(self, table):
        self.element = table.concept_system
        super(ConceptSystemGrid, self).SetTable(table)


if __name__ == '__main__':
    pass

