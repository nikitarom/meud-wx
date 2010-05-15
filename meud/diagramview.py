import wx

class ConceptNode(object):
    
    def get_position(self):
        return self._pos
    
    def set_position(self, value):
        self._pos = value
    
    pos = property(get_position, set_position)
    
    def get_X(self):
        return self._pos[0]
    
    def set_X(self, value):
        self._pos[0] = value
    
    def get_Y(self):
        return self._pos[1]
    
    def set_Y(self, value):
        self._pos[1] = value
        
    X = property(get_X, set_X)
    Y = property(get_Y, set_Y)
    
    def __init__(self, concept=None, pos=(100, 100)):
        self._pos = pos
        
    def draw(self, dc):
        dc.SetBrush(wx.Brush("BLUE"))
        dc.DrawCircle(self.X, self.Y, 10)
        
    def hit_test(self, x, y):
        if ((x-self.X) ** 2 + (y - self.Y) ** 2) <= 10 * 10:
            return True
        else:
            return False
        

class MyCanvas(wx.ScrolledWindow):
    
    def __init__(self, parent, id, size = wx.DefaultSize):
        wx.ScrolledWindow.__init__(self, parent, id, (0, 0),
                                    size=size, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour("WHITE")
        
        self.nodes = [ConceptNode(None), ConceptNode(None, pos=(150, 150))]
        self.lines = [(self.nodes[0], self.nodes[1])]
        self._dragged = None
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)
        
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        
        dc.BeginDrawing()

        bg = wx.Brush(self.GetBackgroundColour())
        dc.SetBackground(bg)
        dc.Clear()
        
        for line in self.lines:
            dc.DrawLine(line[0].X, line[0].Y, line[1].X, line[1].Y)
            
        for node in self.nodes:
            node.draw(dc)
            
        dc.EndDrawing()
        
    def OnMouse(self, event):
        if event.LeftDown():
            (x, y) = (event.GetX(), event.GetY())
            for node in self.nodes:
                if node.hit_test(x, y):
                    self._dragged = node
                    self._last_pos = (x, y)
                    break
        elif event.Dragging() or event.LeftUp():
            if self._dragged:
                (x, y) = self._last_pos
                dx = event.GetX() - x
                dy = event.GetY() - y
                self._dragged.pos = (self._dragged.X + dx, self._dragged.Y + dy)
                self._last_pos = (event.GetX(),event.GetY())
                self.Refresh()
            if event.LeftUp():     
                self._dragged = None
                    
        
        
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = wx.Frame(parent=None, title="Test Window")
    win = MyCanvas(frame, wx.ID_ANY)
    frame.Show()
    app.MainLoop()