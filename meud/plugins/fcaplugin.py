"""FCA plugin"""
import os.path

import fca

from _plugin import Plugin

class FCAPlugin(Plugin):
    name = "FCA"
    
    def get_actions(self, item):
        if item.type == "Context":
            return ["Save concepts"]
    
    def do_action(self, item, action):
        if action == "Save concepts":
            (root, ext) = os.path.splitext(item.name)
            if ext == ".cxt":
                cxt = fca.read_cxt(item.path)
            elif ext == ".txt":
                cxt = fca.read_txt(item.path)
            cs = fca.norris(cxt)
