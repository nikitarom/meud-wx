# -*- coding: utf-8 -*-
"""Contains project class"""

import os, cPickle
import fca

default_names = { fca.Context : "context",
                fca.Scale : "scale",
                fca.ManyValuedContext : "mvcontext",
                fca.ConceptSystem : "conceptsystem"
                }

class Project(object):
    """project contains all elements (contexts, scales, etc.) 
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
        
        self.projectdirty = False
        
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
        if isinstance(new_element, fca.Scale):
            self._scales.append(new_element)
        elif isinstance(new_element, fca.Context):
            self._contexts.append(new_element)
        elif isinstance(new_element, fca.ManyValuedContext):
            self._mvcontexts.append(new_element)
        elif isinstance(new_element, fca.ConceptSystem):
            self._concept_systems.append(new_element)
            
    def delete_element(self, element):
        if isinstance(element, fca.Scale):
            self._scales.remove(element)
        elif isinstance(element, fca.Context):
            self._contexts.remove(element)
        elif isinstance(element, fca.ManyValuedContext):
            self._mvcontexts.remove(element)
        elif isinstance(element, fca.ConceptSystem):
            self._concept_systems.remove(element)
            
            
def save_project(project_, path):
    """Save project to directory in path"""
    try:
        os.makedirs(path)
    except:
        pass
    output = open(os.path.join(path, "meud.project"), "wb")
    project_.projectdirty = False
    cPickle.dump(project_, output)
    output.close()
   
def load_project(path):
    """Load project from directory in path
    
    Return project instance.
    """
    input = open(os.path.join(path, "meud.project"), "rb")
    project_ = cPickle.load(input)
    input.close()
    os.chdir(path)
    return project_


if __name__ == '__main__':
    """Test"""
    test_path = "tests/project/default"
    p = Project()
    c = fca.read_cxt("tests/imports/context.cxt")
    p.add_element(c)
    cs = fca.norris(c)
    p.add_element(cs)
    p.add_element(fca.Scale(fca.read_cxt("tests/imports/context.cxt")))
    save_project(p, test_path)
    p1 = load_project("tests/project/default/")
    