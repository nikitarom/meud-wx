"""Module to work with plugins"""
import wx

import plugins

class PluginsManager(object):
    
    _plugins = []
    
    def __init__(self, workspace):
        self._workspace = workspace
        
        superplugin = plugins._plugin.Plugin;
        for plugin in superplugin.__subclasses__():
            self._plugins.append(plugin())
            
    def GetPlugins(self):
        return self._plugins
        
    def GetItemMenu(self, item, tree):
        menu = wx.Menu()
        
        for plugin in self._plugins:
            submenu = wx.Menu()
            actions = plugin.get_actions(item)
            if actions and len(actions) != 0:
                for action in actions:
                    menu_item = submenu.Append(wx.NewId(), action)
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    f = lambda event, item=item, plugin=plugin, action=action:\
                        self.OnActionClick(item, plugin, action)
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    tree.Bind(wx.EVT_MENU, f, menu_item)
                menu.AppendMenu(wx.NewId(), plugin.name, submenu)
        return menu
            
    def OnActionClick(self, item, plugin, action):
        new_files = plugin.do_action(item, self._workspace, action)
        self._workspace.AddFiles(new_files)