#!/usr/bin/env python
# encoding: utf-8
"""
Contains image handlers
"""

import wx

icons = {
"New" : "img/tango/document-new.png",
"Open" : "img/tango/document-open.png",
"Save" : "img/tango/document-save.png",
"SaveAs" : "img/tango/document-save-as.png",
"Random" : "img/tango/emblem-important.png",
"Apply" : "img/tango/applications-system.png",
"AddRow" : "img/tango/go-bottom.png" ,
"AddColumn" : "img/tango/go-last.png",
"DeleteRow" : "img/tango/go-next.png",
"DeleteColumn" : "img/tango/go-down.png",
"AppIcon" : "img/fugue/application-sidebar-list.png",
"Context" : "img/fugue/document-attribute-c.png",
"MVContext" : "img/fugue/document-attribute-m.png",
"Scale" : "img/fugue/document-attribute-s.png",
"ConceptLattice" : "img/fugue/document-attribute-l.png",
"Text" : "img/fugue/document-text.png",
"HDir" : "img/fugue/folder-horizontal.png",
"OpenHDir" : "img/fugue/folder-horizontal-open.png",
"Image" : "img/fugue/document-image.png",
"Unknown" : "img/fugue/document.png"
}

bitmaps = {}

def initialize():
    for key in icons.keys():
        bitmaps[key] = GetIcon(key)

def GetBitmap(name):
    return bitmaps[name]

def GetIcon(name):
   return wx.Bitmap(icons[name], wx.BITMAP_TYPE_PNG)

