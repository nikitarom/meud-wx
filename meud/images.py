#!/usr/bin/env python
# encoding: utf-8
"""
Contains image handlers
"""

import wx

icons = {
"New" : "img/document-new.png",
"Open" : "img/document-open.png",
"Save" : "img/document-save.png",
"SaveAs" : "img/document-save-as.png",
"Random" : "img/emblem-important.png",
"Apply" : "img/applications-system.png",
"AddRow" : "img/go-bottom.png" ,
"AddColumn" : "img/go-last.png",
"DeleteRow" : "img/go-next.png",
"DeleteColumn" : "img/go-down.png"
}

bitmaps = {}

def initialize():
    for key in icons.keys():
        bitmaps[key] = GetIcon(key)

def GetBitmap(name):
    return bitmaps[name]

def GetIcon(name):
   return wx.Bitmap(icons[name], wx.BITMAP_TYPE_PNG)

