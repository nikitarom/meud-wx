#!/usr/bin/env python
# encoding: utf-8
import os.path

import wx.grid

import fca
from fca.readwrite import (uwrite_cxt, uread_cxt)

import images

class DummyCellEditor(wx.grid.PyGridCellEditor):
    """
    This is a sample GridCellEditor that shows you how to make your own custom
    grid editors.  All the methods that can be overridden are shown here.  The
    ones that must be overridden are marked with "*Must Override*" in the
    docstring.
    """
    def __init__(self):
        wx.grid.PyGridCellEditor.__init__(self)

    def Create(self, parent, id, evtHandler=None):
        """
        Called to create the control, which must derive from wx.Control.
        *Must Override*
        """
        self.SetControl(wx.Control(parent, id))

    def BeginEdit(self, row, col, grid):
        """
        Fetch the value from the table and prepare the edit control
        to begin editing.  Set the focus to the edit control.
        *Must Override*
        """
        self.Show(False)
        self.value = int(grid.GetTable().GetValue(row, col))
        self.EndEdit(row, col, grid)

    def EndEdit(self, row, col, grid):
        """
        Complete the editing of the current cell. Returns True if the value
        has changed.  If necessary, the control may be destroyed.
        *Must Override*
        """
        if self.value == 1:
            grid.GetTable().SetValue(row, col, "0")
        else:
            grid.GetTable().SetValue(row, col, "1")
        if grid.GetParent().saved:
            grid.GetParent().DoUnsaved()
        return True

    def Reset(self):
        """
        Reset the value in the control back to its starting value.
        *Must Override*
        """
        pass

    def Destroy(self):
        """final cleanup"""
        super(DummyCellEditor, self).Destroy()

    def Clone(self):
        """
        Create a new object which is the copy of this one
        *Must Override*
        """
        return DummyCellEditor()

class CrossRenderer(wx.grid.PyGridCellRenderer):
    def __init__(self):
        wx.grid.PyGridCellRenderer.__init__(self)

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        dc.SetBackgroundMode(wx.SOLID)
        dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
        if isSelected:
            dc.SetPen(wx.Pen(colour="BLUE"))
        else:
            dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangleRect(rect)

        dc.SetBackgroundMode(wx.TRANSPARENT)

        value = grid.GetCellValue(row, col)
        
        if int(value) == 1:
            dc.SetPen(wx.Pen(colour="BLACK", width=3))
            dx = (rect.TopLeft[0] - rect.TopRight[0])/3
            dc.DrawLine(rect.TopLeft[0] - dx, rect.TopLeft[1],
                         rect.BottomRight[0] + dx, rect.BottomRight[1])
            dc.DrawLine(rect.TopRight[0] + dx, rect.TopRight[1],
                         rect.BottomLeft[0] - dx, rect.BottomLeft[1])

    def Clone(self):
        return CrossRenderer()


class ContextTable(wx.grid.PyGridTableBase):
    
    init_value = False
    
    def __init__(self, item, model):
        self._item = item
        path = item.path
        self._model = model
        wx.grid.PyGridTableBase.__init__(self)
        (head, ext) = os.path.splitext(path)
        if ext == ".cxt":
            context = uread_cxt(path)
        elif ext == ".txt":
            context = fca.read_txt(path)
        self.path = path
        self.context = context
        
    def DoUnsaved(self):
        self._model.DoUnsaved(self._item)
        
    def Save(self):
        self._model.DoSaved(self._item)
        uwrite_cxt(self.context, self.path)
        
    def GetNumberRows(self):
        return len(self.context) + 1
        
    def GetNumberCols(self):
        return len(self.context.attributes) + 1
        
#    def GetColLabelValue(self, col):
#        return self.context.attributes[col]
#        
#    def GetRowLabelValue(self, row):
#        return self.context.objects[row]
        
    def IsEmptyCell(self, row, col):
        if (row==0) and (col==0):
            return True
        return False
        
    def GetValue(self, row, col):
        if (col == 0) and (row == 0):
            return ""
        elif (col == 0) and (row > 0):
            return self.context.objects[row-1]
        elif (row == 0) and (col > 0):
            try:
                value = self.context.attributes[col-1]
            except:
                value = "0"
            return value
        elif (row > 0) and (col > 0):
            if self.context[row-1][col-1]:
                return 1
            else:
                return 0
        
    def SetValue(self, row, col, value):
        if (row > 0) and (col > 0):
            self.context[row-1][col-1] = (int(value) == 1)
        elif (col == 0) and (row > 0):
            self.context.objects[row-1] = str(value)
            self.DoUnsaved()
        elif (row == 0) and (col > 0):
            self.context.attributes[col-1] = str(value)
            self.DoUnsaved()
            
    def SaveAs(self, path):
        uwrite_cxt(self.context, path)
        self._item = self._model.FileSaveAs(path, self._view)
        self.path = self._item.path
            
    def AppendCols(self, numCols=1):
        self.DoUnsaved()
        if len(self.context.objects) == 0:
            self.context.add_attribute([], "New Attribute")
        else:
            self.context.add_attribute([self.init_value]*len(self.context), "New Attribute")
        
        msg = wx.grid.GridTableMessage(self,            # The table
              wx.grid.GRIDTABLE_NOTIFY_COLS_APPENDED,   # what we did to it
              1                                         # how many
              )
        self.GetView().ProcessTableMessage(msg)
        self.GetView().SetGridCursor(0, len(self.context.attributes))
        self.GetView().EnableCellEditControl()
        
    def AppendRows(self, numRows=1):
        self.DoUnsaved()
        if len(self.context.attributes) == 0:
            self.context.add_object([], "New Object")
        else:
            self.context.add_object([self.init_value]*len(self.context.attributes), "New Object")
        
        msg = wx.grid.GridTableMessage(self,            # The table
              wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED,   # what we did to it
              1                                         # how many
              )
        self.GetView().ProcessTableMessage(msg)
        self.GetView().SetGridCursor(len(self.context), 0)
        self.GetView().EnableCellEditControl()
        
    def DeleteCols(self, pos=0, numCols=1):
        self.DoUnsaved()
        cols = self.GetView().GetSelectedCols()
        cols.sort()
        cols.reverse()
        if len(cols) != 0:
            for col in cols:
                if col==0:
                    continue
                self.context.delete_attribute(col-1)
                msg = wx.grid.GridTableMessage(self,            # The table
                      wx.grid.GRIDTABLE_NOTIFY_COLS_INSERTED
                      )
                self.GetView().ProcessTableMessage(msg)
        self.GetView().ClearSelection()
    
    def DeleteRows(self, pos=0, numCols=1):
        self.DoUnsaved()
        rows = self.GetView().GetSelectedRows()
        rows.sort()
        rows.reverse()
        if len(rows) != 0:
            for row in rows:
                if row==0:
                    continue
                self.context.delete_object(row-1)
                msg = wx.grid.GridTableMessage(self,            # The table
                      wx.grid.GRIDTABLE_NOTIFY_ROWS_INSERTED
                      )
                self.GetView().ProcessTableMessage(msg)
        self.GetView().ClearSelection()
        
        
class MVContextTable(ContextTable):

    init_value = 0
    
    def __init__(self, item, model):
        self._item = item
        path = item.path
        self._model = model
        wx.grid.PyGridTableBase.__init__(self)
        self.context = fca.read_mv_txt(path)
        self.path = path
        
    def Save(self):
        self._model.DoSaved(self._item)
        fca.write_mv_txt(self.context, self.path)
        
    def SaveAs(self, path):
        fca.write_mv_txt(self.context, path)
        self._item = self._model.FileSaveAs(path, self._view)

    def GetValue(self, row, col):
        if (col == 0) and (row == 0):
            return ""
        elif (col == 0) and (row > 0):
            return self.context.objects[row-1]
        elif (row == 0) and (col > 0):
            try:
                value = self.context.attributes[col-1]
            except:
                value = ""
            return value
        elif (row > 0) and (col > 0):
            return self.context[row-1][col-1]
        
    def SetValue(self, row, col, value):
        self.DoUnsaved()
        if (row > 0) and (col > 0):
            try:
                self.context[row-1][col-1] = int(value)
            except:
                self.context[row-1][col-1] = str(value)
        elif (col == 0) and (row > 0):
            self.context.objects[row-1] = str(value)
            self.DoUnsaved()
        elif (row == 0) and (col > 0):
            self.context.attributes[col-1] = str(value)
            self.DoUnsaved()

class ContextGrid(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.grid = wx.grid.Grid(self, -1)
        
        self.toolBar = self.CreateToolBar()
        self.toolBar.Realize()
        
        self.saved = True
        
    def DoUnsaved(self):
        self._saved = False
        self.grid.Table.DoUnsaved()
        
    def SetTable(self, table):
        # TODO:
        table._view = self
        self.grid.element = table.context
        self.grid.SetTable(table)
        
        for row in range(len(table.context)):
            for col in range(len(table.context[0])):
                self.grid.SetCellRenderer(row+1, col+1, CrossRenderer())
                self.grid.SetCellEditor(row+1, col+1, DummyCellEditor())
        
    def CreateToolBar(self):
        tb = wx.ToolBar(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tb, 0, wx.EXPAND)
        sizer.Add(self.grid, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        tool = tb.AddLabelTool(wx.NewId(), "Save", images.GetBitmap("Save"),
                shortHelp="Save current file")
        self.Bind(wx.EVT_TOOL, self.OnSave, tool)
        
        tool = tb.AddLabelTool(wx.NewId(), "Save as...", images.GetBitmap("SaveAs"),
                shortHelp="Save current file as...")
        self.Bind(wx.EVT_TOOL, self.OnSaveAs, tool)
        
        tb.AddSeparator()
        
        tool = tb.AddLabelTool(wx.NewId(), "Add Object", images.GetBitmap("AddRow"),
                shortHelp="Add object")
        self.Bind(wx.EVT_TOOL, self.OnAddRow, tool)
        
        tool = tb.AddLabelTool(wx.NewId(), "Add Attribute", images.GetBitmap("AddColumn"),
                shortHelp="Add Attribute")
        self.Bind(wx.EVT_TOOL, self.OnAddColumn, tool)
        
        tool = tb.AddLabelTool(wx.NewId(), "Delete Object",
         images.GetBitmap("DeleteRow"), shortHelp="Delete Object")
        self.Bind(wx.EVT_TOOL, self.OnDeleteRow, tool)
        
        tool = tb.AddLabelTool(wx.NewId(), "Delete Attribute",
         images.GetBitmap("DeleteColumn"), shortHelp="Delete Attribute")
        self.Bind(wx.EVT_TOOL, self.OnDeleteColumn, tool)
        
        return tb
    
    def OnAddRow(self, event):
        self.grid.GetTable().AppendRows()
        context = self.grid.GetTable().context
        row = len(context)
        for col in range(len(context[0])):
            self.grid.SetCellRenderer(row, col+1, CrossRenderer())
            self.grid.SetCellEditor(row, col+1, DummyCellEditor())
    
    def OnAddColumn(self, event):
        self.grid.GetTable().AppendCols()
        context = self.grid.GetTable().context
        col = len(context.attributes)
        for row in range(len(context)):
            self.grid.SetCellRenderer(row+1, col, CrossRenderer())
            self.grid.SetCellEditor(row+1, col, DummyCellEditor())
    
    def OnDeleteRow(self, event):
        self.grid.GetTable().DeleteRows()
    
    def OnDeleteColumn(self, event):
        self.grid.GetTable().DeleteCols()
    
    def OnSave(self, event):
        self.saved = True
        self.grid.GetTable().Save()
        
    def OnSaveAs(self, event):
        self.saved = True
        dlg = wx.FileDialog(
                    self, message="Save file as ...", defaultDir=os.getcwd(), 
                    defaultFile=".cxt", wildcard='*.cxt', style=wx.SAVE
                    )
        if dlg.ShowModal() == wx.ID_OK:
                    path = dlg.GetPath()
                    self.grid.GetTable().SaveAs(path)
        dlg.Destroy()
    
class MVContextGrid(ContextGrid):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.grid = wx.grid.Grid(self, -1)
        
        self.toolBar = self.CreateToolBar()
        self.toolBar.Realize()
        
        self.saved = True
        
    def SetTable(self, table):
        table._view = self
        self.grid.element = table.context
        self.grid.SetTable(table)
        
    def OnAddRow(self, event):
        self.grid.GetTable().AppendRows()

    def OnAddColumn(self, event):
        self.grid.GetTable().AppendCols()

if __name__ == '__main__':
    pass

