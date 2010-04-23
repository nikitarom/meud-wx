"""Plugins should be placed there"""
# Plugins are loaded automatically, filename should not start with _.
import os
import os.path
import re

import _plugin

files = os.listdir(__path__[0])
pattern = r"^[^_].*(\.py)$"
plugin_re = re.compile(pattern)
for str in files:
    if plugin_re.match(str):
        (root, ext) = os.path.splitext(str)
        exec "import " + root
