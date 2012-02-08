#!/usr/bin/env python
# encoding: utf-8
DEBUG = True

files_categories = {
"mvcontexts" : "Many-valued contexts",
"scales" : "Scales",
"contexts" : "Contexts",
"concept_systems" : "Concept Systems"
}

workspace_path = None
if not workspace_path:
    import codecs
    pth_file = codecs.open("workspace.pth", "r", "utf-8")
    workspace_path = pth_file.readline().strip()
    dot_path = pth_file.readline().strip()
    
plugins_path = r"meud/plugins"