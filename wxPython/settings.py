#!/usr/bin/env python

import wx
import images
try:
    import wx.lib.platebtn as platebtn
except ImportError:
    import platebtn

#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------

class SettingsDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(SettingsDialog, self).__init__(parent, title = title, size = wx.DefaultSize)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
#        self.Create(parent, id, title)
        self.initUI()

    def initUI(self):
        # FONT
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        panel = wx.Panel(self)
        bagsizer = wx.GridBagSizer(3, 3)
        # ROW 1
        bitmap_wheel = wx.Bitmap("images/Settings.png")
        bitmap_wheel.SetSize((32, 32))
        sbitmap_wheel = wx.StaticBitmap(panel, bitmap=bitmap_wheel)
        st1 = wx.StaticText(panel, label="Settings")
        st1.SetFont(font)
        bagsizer.Add(st1, pos=(0,0), flag=wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)
        bagsizer.Add(sbitmap_wheel, pos=(0, 5), flag= wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_RIGHT, border = 5)
        # ROW 2
        sl = wx.StaticLine(panel)
        bagsizer.Add(sl, pos=(1, 0), span=(1, 7), flag = wx.EXPAND, border=10)
        # ROW 3
        st2 = wx.StaticText(panel, label="File:")
        st2.SetFont(font)
        tc_file = wx.TextCtrl(panel)
        bagsizer.Add(st2, pos=(2, 0), flag=wx.ALIGN_RIGHT, border=10)
        bagsizer.Add(tc_file, pos=(2, 1), span=(1, 4), flag=wx.EXPAND|wx.ALIGN_LEFT)
        img_open = wx.Bitmap("images/Open.png")
        img_open.SetSize((24, 24))
        tbtn = platebtn.PlateButton(panel, wx.ID_ANY, "", img_open, size=((16, 16)), style=platebtn.PB_STYLE_DEFAULT)
        bagsizer.Add(tbtn, pos=(2, 5), flag= wx.RIGHT | wx.EXPAND)
        # ROW 4
        st_equip = wx.StaticText(panel, label="Equipment")
        st_equip.SetFont(font)
        tc_equip = wx.TextCtrl(panel)
        button_package = wx.Button(panel, label="Browse...")
        bagsizer.Add(st_equip, pos=(3, 0), flag= wx.LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, border=10)
        bagsizer.Add(tc_equip, pos=(3, 1), span=(1, 4), flag= wx.EXPAND | wx.TOP, border=5)
        bagsizer.Add(button_package, pos=(3, 5), flag= wx.TOP | wx.RIGHT, border = 5)
        # ROW 5
        st_extends = wx.StaticText(panel, label="Extends")
        st_extends.SetFont(font)
        cb_extends = wx.ComboBox(panel)
        btn_extends = wx.Button(panel, label="Browse...")
        bagsizer.Add(st_extends, pos=(4, 0), flag= wx.LEFT | wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, border=10)
        bagsizer.Add(cb_extends, pos=(4, 1), span=(1, 4), flag= wx.EXPAND | wx.TOP, border=5)
        bagsizer.Add(btn_extends, pos=(4, 5), flag= wx.TOP | wx.RIGHT, border = 5)
        # ROW 6
        sb = wx.StaticBox(panel, label="Optional Attributes")
        sboxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
        cb_public = wx.CheckBox(panel, wx.ID_ANY, label="Public")
        cb_default = wx.CheckBox(panel, wx.ID_ANY, label="Generate Default Constructor")
        cb_main = wx.CheckBox(panel, wx.ID_ANY, label="Generate Main Method")
        sboxsizer.Add(cb_public, flag= wx.LEFT | wx.TOP | wx.BOTTOM, border=5)
        sboxsizer.Add(cb_default, flag= wx.LEFT | wx.BOTTOM, border=5)
        sboxsizer.Add(cb_main, flag= wx.LEFT | wx.BOTTOM, border=5)
        bagsizer.Add(sboxsizer, pos=(5, 0), span=(1, 6), flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=5)
        # ROW 7
        btn_help = wx.Button(panel, wx.ID_ANY, label="Help")
        btn_ok = wx.Button(panel, wx.ID_ANY, label="Ok")
        btn_close = wx.Button(panel, wx.ID_ANY, label="Cancel")
        bagsizer.Add(btn_help, pos=(7, 0), flag= wx.LEFT | wx.BOTTOM, border=5)
        bagsizer.Add(btn_ok, pos=(7, 4), flag=wx.RIGHT | wx.BOTTOM, border=5)
        bagsizer.Add(btn_close, pos=(7, 5), flag=wx.BOTTOM, border=5)
        # ENDUP
        bagsizer.AddGrowableCol(2)
        panel.SetSizer(bagsizer)
        bagsizer.Fit(self)
