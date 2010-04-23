import wx

from _plugin import Plugin

class TestPlugin(Plugin):
    name = "Test"
    
    def get_actions(self, item):
        return ["Who am I?"]
    
    def do_action(self, item, action):
        if action == "Who am I?":
            dlg = wx.MessageDialog(None, "You are " + item.name,
                               "Test",
                               wx.OK | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            dlg.Destroy()