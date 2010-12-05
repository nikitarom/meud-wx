#!/usr/bin/env python
# encoding: utf-8

import wx.grid

import fca

class ConceptSystemTable(wx.grid.PyGridTableBase):
    
    def __init__(self, concept_system):
        wx.grid.PyGridTableBase.__init__(self)
        self.concept_system = concept_system
        self.number_of_meta_cols = len(concept_system[0].meta.keys())
        self._sorted_columns = ["no"] * self.number_of_meta_cols
        
    def GetNumberRows(self):
        return len(self.concept_system)
        
    def GetNumberCols(self):
        return 2 + self.number_of_meta_cols
        
    def GetColLabelValue(self, col):
        return (["Extent", "Intent"] + self.concept_system[0].meta.keys())[col]
        
    def GetRowLabelValue(self, row):
        return row + 1
        
    def IsEmptyCell(self, row, col):
        return False
        
    def GetValue(self, row, col):
        if col == 0:
            extent_string = ", ".join(self.concept_system[row].extent)
            return extent_string
        elif col == 1:
            intent_string = ", ".join(self.concept_system[row].intent)
            return intent_string
        else:
            meta_col = col - 2
            meta_key = self.concept_system[0].meta.keys()[meta_col]
            return self.concept_system[row].meta[meta_key]
        
    def SetValue(self, row, col, value):
        pass
        
    def SortColumn(self, col):
        if col > 1:
            meta_col = col - 2
            meta_key = self.concept_system[0].meta.keys()[meta_col]
            data = self.concept_system[:]
            if self._sorted_columns[meta_col] == "no" or \
               self._sorted_columns[meta_col] == "ascent":
                descent = lambda x, y: cmp(y.meta[meta_key], x.meta[meta_key])
                data.sort(descent)
                self._sorted_columns[meta_col] = "descent"
            elif self._sorted_columns[meta_col] == "descent":
                ascent = lambda x, y: cmp(x.meta[meta_key], y.meta[meta_key])
                data.sort(ascent)
                self._sorted_columns[meta_col] = "ascent"
            self.concept_system = fca.ConceptSystem(data)


class ConceptSystemGrid(wx.grid.Grid):

    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, 
                self.OnLabelRightClicked)
        
    def SetTable(self, table):
        self._table = table
        super(ConceptSystemGrid, self).SetTable(table)
        
    def OnLabelRightClicked(self, evt):
        # Did we click on a row or a column?
        row, col = evt.GetRow(), evt.GetCol()
        if row == -1: 
            self.colPopup(col, evt)
        elif col == -1: 
            pass
            
    def colPopup(self, col, evt):
        """(col, evt) -> display a popup menu when a column label is
        right clicked"""
        x = self.GetColSize(col) / 2
        menu = wx.Menu()
        id1 = wx.NewId()
        sortID = wx.NewId()

        xo, yo = evt.GetPosition()
        self.SelectCol(col)
        cols = self.GetSelectedCols()
        self.Refresh()
        menu.Append(sortID, "Sort Column")

        def sort(event, self=self, col=col):
            self._table.SortColumn(col)

        if len(cols) == 1:
            self.Bind(wx.EVT_MENU, sort, id=sortID)

        self.PopupMenu(menu)
        menu.Destroy()
        return


if __name__ == '__main__':
    pass

