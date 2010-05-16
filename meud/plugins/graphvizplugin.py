import os
import os.path

from _plugin import Plugin

class GraphvizPlugin(Plugin):
    name = "Graphviz"
    graphviz_path = "C:/Program Files/Graphviz2.26.3/bin/"
    
    def get_actions(self, item):
        if item.type == "Graphviz dot":
            return ["Save as .png"]
    
    def do_action(self, item, workspace, action):
        if action == "Save as .png":
            return self.SaveDotAsPng(item)
        
    def SaveDotAsPng(self, item):
        default_path = "".join([item.path[:-3], "png"])
        newpath = default_path
        i = 1
        while (os.path.exists(newpath)):
            newpath = default_path[:-4] + "-{0}".format(i) + newpath[-4:]
            i += 1
        
        dot_path = os.path.join(self.graphviz_path, "dot.exe")
        os.spawnl(os.P_WAIT, dot_path, "dot.exe", "-Tpng",
                   "-o{0}".format(newpath), item.path)
        return [newpath]
        