import wx
 
class ChangeDepthDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        self.initui()
        self.SetSize((250, 200))
        self.SetTitle('Change Color Depth')
 
    def initui(self):
        panel = wx.Panel(self)
        verticalbox = wx.BoxSizer(wx.VERTICAL)
 
        staticbox = wx.StaticBox(panel, label='Colors')
        staticboxsizer = wx.StaticBoxSizer(staticbox, orient=wx.VERTICAL)
        staticboxsizer.Add(wx.RadioButton(panel, label='256 Colors', style=wx.RB_GROUP))
        staticboxsizer.Add(wx.RadioButton(panel, label='16 Colors'))
        staticboxsizer.Add(wx.RadioButton(panel, label='2 Colors'))
 
        horizontalbox1 = wx.BoxSizer(wx.HORIZONTAL)
        horizontalbox1.Add(wx.RadioButton(panel, label='Custom'))
        horizontalbox1.Add(wx.TextCtrl(panel), flag=wx.LEFT, border=5)
        staticboxsizer.Add(horizontalbox1)
 
        panel.SetSizer(staticboxsizer)
 
        horizontalbox2 = wx.BoxSizer(wx.HORIZONTAL)
        button_ok = wx.Button(self, label='OK')
        button_close = wx.Button(self, label='Close')
        horizontalbox2.Add(button_ok)
        horizontalbox2.Add(button_close, flag=wx.LEFT, border=5)
 
        verticalbox.Add(panel, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        verticalbox.Add(horizontalbox2, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
 
        self.SetSizer(verticalbox)
 
        button_ok.Bind(wx.EVT_BUTTON, self.onclose)
        button_close.Bind(wx.EVT_BUTTON, self.onclose)
 
    def onclose(self, e):
        self.Close()
 
 
class Example(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        self.initui()
 
    def initui(self):
        ID_DEPTH = wx.NewId()
 
        toolbar = self.CreateToolBar()
        # wxPython Classic 에서는 AddLabelTool() 사용
        toolbar.AddTool(ID_DEPTH, '', wx.Bitmap('icon/eye.png'))
        toolbar.Realize()
 
        self.Bind(wx.EVT_TOOL, self.onchangedepth, id=ID_DEPTH)
 
        self.SetSize((300, 200))
        self.SetTitle('Custom dialog')
        self.Center()
        self.Show(True)
 
    def onchangedepth(self, e):
        changedepth = ChangeDepthDialog(None, title='Change Color Depth')
        changedepth.ShowModal()
        changedepth.Destroy()
 
 
if __name__ == '__main__':
    app = wx.App()
    Example(None)
    app.MainLoop()
