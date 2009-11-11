# -*- coding: utf-8 -*-
"""Contains workspace class"""

import os, cPickle
import fca

default_names = { fca.Context : "context",
                fca.Scale : "scale",
                fca.ManyValuedContext : "mvcontext",
                fca.ConceptSystem : "conceptsystem"
                }

class Workspace(object):
    """Workspace contains all elements (contexts, scales, etc.) 
    which is used by user during his work with application.
    Can be stored at the hard drive.
    
    Examples
    ========
    
    
    """
    
    def get_contexts(self):
        return self._contexts
    
    contexts = property(get_contexts)
    
    def get_scales(self):
        return self._scales
    
    scales = property(get_scales)
    
    def get_mvcontexts(self):
        return self._mvcontexts
    
    mvcontexts = property(get_mvcontexts)
    
    def get_concept_systems(self):
        return self._concept_systems
    
    concept_systems = property(get_concept_systems)
    
    def get_name(self):
        return self._name
    
    def set_name(self, value):
        if type(value) == str:
            self._name = value
            
    name = property(get_name, set_name)
    
    def __init__(self, name="default"):
        """Constructor"""
        self._name = name
        self._contexts = []
        self._scales = []
        self._mvcontexts = []
        self._concept_systems = []
        
        self._name_indexes = {}
        
    def add_element(self, new_element, name="default"):
        if name == "default":
            dname = default_names[new_element.__class__]
            if not self._name_indexes.has_key(dname):
                self._name_indexes[dname] = 0
            new_element.name = "".join([dname, str(self._name_indexes[dname])])
            self._name_indexes[dname] += 1
        else:
            if not self._name_indexes.has_key(name):
                self._name_indexes[name] = 0
                suffix = ""
            else:
                suffix = str(self._name_indexes[name])
            new_element.name = "".join([name, suffix])
            self._name_indexes[name] += 1
        if isinstance(new_element, fca.Context):
            self._contexts.append(new_element)
        elif isinstance(new_element, fca.Scale):
            self._scales.append(new_element)
        elif isinstance(new_element, fca.ManyValuedContext):
            self._mvcontexts.append(new_element)
        elif isinstance(new_element, fca.ConceptSystem):
            self._concept_systems.append(new_element)
            
            
def save_workspace(workspace, path):
    """Save workspace to directory in path"""
    try:
        # TODO: how better?
        os.chdir(os.path.join(path, workspace.name))
    except:
        os.makedirs(os.path.join(path, workspace.name))
        os.chdir(os.path.join(path, workspace.name))
    output = open("meud.workspace", "wb")
    cPickle.dump(workspace, output)
    output.close()
   
def load_workspace(path):
    """Load workspace from directory in path
    
    Return workspace instance.
    """
    os.chdir(path)
    input = open("meud.workspace", "rb")
    workspace = cPickle.load(input)
    input.close()
    return workspace


if __name__ == '__main__':
    """Test"""
    test_path = "tests/workspace"
    ws = Workspace()
    c = fca.read_cxt("tests/imports/context.cxt")
    ws.add_element(c)
    cs = fca.norris(c)
    ws.add_element(cs)
    ws.add_element(fca.Scale(fca.read_cxt("tests/imports/context.cxt")))
    save_workspace(ws, test_path)
    ws1 = load_workspace("../default")
    