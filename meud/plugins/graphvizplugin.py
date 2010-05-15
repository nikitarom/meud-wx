from _plugin import Plugin

class GraphvizPlugin(Plugin):
    name = "Graphviz"
    
    def get_actions(self, item):
        if item.type == "Graphviz dot":
            return ["Save as .png"]
    
    def do_action(self, item, workspace, action):
        if action == "Save as .png":
            return self.SaveDotAsPng(item)
        
    def SaveDotAsPng(self, item):
        try:
            pass
        except:
            pass
        