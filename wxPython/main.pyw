#!/usr/bin/env python

import wx
import wx.aui as aui
from settings import SettingsDialog

class ParentFrame(aui.AuiMDIParentFrame):
    def __init__(self, parent):
        aui.AuiMDIParentFrame.__init__(
            self, parent, -1,
            title = "AuiMDIParentFrame",
            size = (640,480),
            style = wx.DEFAULT_FRAME_STYLE)
        self.count = 0
        self.mb = self.makeMenuBar()
        self.SetMenuBar(self.mb)
        self.CreateStatusBar()
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        self.Center()
        self.SetBackgroundColour(wx.Colour(255, 0, 0))
#        self.showSettingsDialog()

    def showSettingsDialog(self):
        dlg = SettingsDialog(self, title='Change Color Depth')
        dlg.CenterOnParent()

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            print("You pressed OK\n")
        else:
            print("You pressed Cancel\n")
        dlg.Destroy()

    def makeMenuBar(self):
        mb = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "Settings...\t")
        self.Bind(wx.EVT_MENU, self.onDoSettingsDialog, item)
        item = menu.Append(-1, "New child window\tCtrl-N")
        self.Bind(wx.EVT_MENU, self.onNewChild, item)
        item = menu.Append(-1, "Close parent")
        self.Bind(wx.EVT_MENU, self.onDoClose, item)
        mb.Append(menu, "&File")
        return mb

    def onNewChild(self, evt):
        self.count += 1
        child = ChildFrame(self, self.count)
        #child.Show()

    def onDoSettingsDialog(self, evt):
        self.showSettingsDialog()

    def onDoClose(self, evt):
        self.Close()

    def onCloseWindow(self, evt):
        # Close all ChildFrames first else Python crashes
        for m in self.GetChildren():
            if isinstance(m, aui.AuiMDIClientWindow):
                for k in list(m.GetChildren()):
                    if isinstance(k, ChildFrame):
                        k.Close()
        evt.Skip()


#----------------------------------------------------------------------

class ChildFrame(aui.AuiMDIChildFrame):
    def __init__(self, parent, count):
        aui.AuiMDIChildFrame.__init__(self, parent, -1,
                                         title="Child: %d" % count)
        mb = parent.MakeMenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "This is child %d's menu" % count)
        mb.Append(menu, "&Child")
        self.SetMenuBar(mb)

        p = wx.Panel(self)
        wx.StaticText(p, -1, "This is child %d" % count, (10,10))
        p.SetBackgroundColour('light blue')

        sizer = wx.BoxSizer()
        sizer.Add(p, 1, wx.EXPAND)
        self.SetSizer(sizer)

        wx.CallAfter(self.Layout)


if __name__ == "__main__":
    app = wx.App(False)
    pf = ParentFrame(None)
    pf.Show()
    app.MainLoop()
