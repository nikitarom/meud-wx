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
    
    def get_concept(self):
        return self._concept
        
    concept = property(get_concept)
    
    def __init__(self, concept=None, pos=(100, 100), top_labels=["Top"],
                    bottom_labels=["Bottom"]):
        self._pos = pos
        self._concept = concept
        self._t_labels = top_labels
        self._b_labels = bottom_labels
        
    def draw(self, dc):
        dc.SetBrush(wx.Brush("BLUE"))
        dc.DrawCircle(self.X, self.Y, 10)
        
        h_step = dc.GetCharHeight()
        for i in range(len(self._t_labels)):
            dc.DrawText(self._t_labels[i], self.X - 10, self.Y - 25 - h_step*i)
        for i in range(len(self._b_labels)):
            dc.DrawText(self._b_labels[i], self.X - 10, self.Y + 10 + h_step*i)
        
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
        self._dragged = None
        self.cs = None
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
    def SetConceptSystem(self, cl):
        self.cs = cl
        self._positions = get_coordinates(cl)
        own_objects = find_own_objects(cl)
        own_attributes = find_own_attributes(cl)
        
        self.nodes = []
        
        size = self.GetClientSize()
        for concept in cl:
            new_coords = (10 + self._positions[concept][0] * (size[0] - 20),
            size[1] - 10 - self._positions[concept][1] * (size[1] - 20))
            self.nodes.append(ConceptNode(concept, new_coords, own_attributes[concept],
                                own_objects[concept]))
        
        self.lines = []
        for i in range(len(cl)):
            for concept in cl.children(cl[i]):
                j = cl.index(concept)
                self.lines.append((self.nodes[i], self.nodes[j]))
            
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
        
    def OnSize(self, event):
        if self.cs:
            size = self.GetClientSize()
            for i in range(len(self.cs)):
                new_coords = (10 + self._positions[self.cs[i]][0] * (size[0] - 20),
                size[1] - 10 - self._positions[self.cs[i]][1] * (size[1] - 20))
                self.nodes[i].pos = new_coords
        
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
                new_xy = (self._dragged.X + dx, self._dragged.Y + dy)
                if self.TryDrag(new_xy):
                    self._dragged.pos = new_xy
                    self._last_pos = (event.GetX(),event.GetY())
                self.Refresh()
            if event.LeftUp():     
                self._dragged = None
                
    def TryDrag(self, pos):
        concept = self._dragged.concept
        for child in self.cs.children(concept):
            i = self.cs.index(child)
            if pos[1] > self.nodes[i].Y:
                return False
        for parent in self.cs.parents(concept):
            i = self.cs.index(parent)
            if pos[1] < self.nodes[i].Y:
                return False
        return True
        
        
def find_own_objects(cs):
    """Return set of own objects for current concept"""
    own_objects = {}
    for con in cs:
        own_objects[con] = []
        for obj in con.extent:
            own_objects[con].append(obj)
            for sub_con in cs:
                if sub_con.extent < con.extent and\
                        obj in sub_con.extent:
                    own_objects[con].pop()
                    break
    return own_objects

def find_own_attributes(cs):
    """Return set of own attributes for current concept"""
    own_attributes = {}
    for con in cs:
        own_attributes[con] = []
        for attr in con.intent:
            own_attributes[con].append(attr)
            for sub_con in cs:
                if sub_con.intent < con.intent and\
                        attr in sub_con.intent:
                    own_attributes[con].pop()
                    break
    return own_attributes  
    
               
def get_coordinates(concept_system):
    import tempfile
    import os
    import fca
    graphviz_path = "/usr/local/bin/"
    temp_dot_path = tempfile.mktemp()
    temp_plain_path = tempfile.mktemp()
    
    coordinates = {}
    
    fca.write_dot(concept_system, temp_dot_path)
    
    dot_path = os.path.join(graphviz_path, "dot")
    os.spawnl(os.P_WAIT, dot_path, "dot", "-Tplain",
               "-o{0}".format(temp_plain_path), temp_dot_path)
    
    plain_dot_file = open(temp_plain_path)
    
    for line in plain_dot_file:
        spl_line = line.split(" ")
        if spl_line[0] == "graph":
            canvas_width = float(spl_line[2])
            canvas_height = float(spl_line[3])
        elif spl_line[0] == "node":
            i = int(spl_line[1][1:])
            xy = (float(spl_line[2])/canvas_width, float(spl_line[3])/canvas_height)
            coordinates[concept_system[i]] = xy
    
    plain_dot_file.close()
    
    # now clean for ourselves
    os.unlink(temp_plain_path)
    os.unlink(temp_dot_path)
    
    return coordinates
          
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = wx.Frame(parent=None, title="Test Window")
    win = MyCanvas(frame, wx.ID_ANY)
    frame.Show()
    from fca import (Context, Concept, ConceptLattice)
    ct = [[True, False, False, True],\
          [True, False, True, False],\
          [False, True, True, True],\
          [False, True, True, True]]
    objs = ['1', '2', '3', '4']
    attrs = ['a', 'b', 'c', 'd']
    c = Context(ct, objs, attrs)
    cl = ConceptLattice(c)
    win.SetConceptSystem(cl)
    app.MainLoop()