#!/usr/bin/env pythonw
"""
doc string
"""

# pylint: disable=C0103
print '-I- Importing dependencies'
import wx
import wx.lib.buttons as buttons
import sys
import os
#import ErMagicBuilder
import builder
import pmag
import ipmag
import drop_down_menus
import pmag_widgets as pw
import magic_grid
import pmag_menu_dialogs
import validate_upload
import grid_frame


class MainFrame(wx.Frame):
    """
    make magic
    """

    def __init__(self, WD=None, name='Main Frame'):
        wx.GetDisplaySize()
        wx.Frame.__init__(self, None, wx.ID_ANY, name=name)

        #
        self.grid_frame = None
        self.panel = wx.Panel(self, size=wx.GetDisplaySize(), name='main panel')
        print '-I- Fetching working directory'
        self.WD = os.path.realpath(WD) or os.getcwd()

        print '-I- Initializing magic data object'
        self.data_model = validate_upload.get_data_model()
        self.er_magic = builder.ErMagicBuilder(self.WD, self.data_model)
        self.edited = False

        # initialize magic data object
        # attempt to read magic_measurements.txt, and all er_* and pmag_* files
        print '-I- Read in any available data from working directory'
        self.er_magic.get_all_magic_info()
        
        # POSSIBLY RELOCATE THIS EVENTUALLY:
        print '-I- Initializing headers'
        self.er_magic.init_default_headers()
        self.er_magic.init_actual_headers()
        #
        print '-I- Initializing interface'
        self.InitUI()


    def InitUI(self):
        """
        Make main user interface
        """
        bSizer0 = wx.StaticBoxSizer(
            wx.StaticBox(self.panel, wx.ID_ANY, "Choose MagIC project directory", name='bSizer0'), wx.HORIZONTAL
        )
        self.dir_path = wx.TextCtrl(self.panel, id=-1, size=(600, 25), style=wx.TE_READONLY)
        self.dir_path.SetValue(self.WD)
        self.change_dir_button = buttons.GenButton(
            self.panel, id=-1, label="change dir", size=(-1, -1), name='change_dir_btn'
        )
        self.change_dir_button.SetBackgroundColour("#F8F8FF")
        self.change_dir_button.InitColours()
        self.Bind(wx.EVT_BUTTON, self.on_change_dir_button, self.change_dir_button)
        bSizer0.Add(self.change_dir_button, wx.ALIGN_LEFT)
        bSizer0.AddSpacer(40)
        bSizer0.Add(self.dir_path, wx.ALIGN_CENTER_VERTICAL)

        #---sizer 1 ----
        bSizer1 = wx.StaticBoxSizer(wx.StaticBox(self.panel, wx.ID_ANY, "Add information to the data model", name='bSizer1'), wx.HORIZONTAL)

        text = "1. add location data"
        self.btn1 = buttons.GenButton(self.panel, id=-1, label=text,
                                      size=(300, 50), name='location_btn')
        self.btn1.SetBackgroundColour("#FDC68A")
        self.btn1.InitColours()
        self.Bind(wx.EVT_BUTTON, self.make_grid_frame, self.btn1)

        text = "2. add site data"
        self.btn2 = buttons.GenButton(self.panel, id=-1, label=text,
                                      size=(300, 50), name='site_btn')
        self.btn2.SetBackgroundColour("#6ECFF6")
        self.btn2.InitColours()
        self.Bind(wx.EVT_BUTTON, self.make_grid_frame, self.btn2)


        text = "3. add sample data"
        self.btn3 = buttons.GenButton(self.panel, id=-1, label=text,
                                      size=(300, 50), name='sample_btn')
        self.btn3.SetBackgroundColour("#C4DF9B")
        self.btn3.InitColours()
        self.Bind(wx.EVT_BUTTON, self.make_grid_frame, self.btn3)

        
        text = "4. add specimen data"
        self.btn4 = buttons.GenButton(self.panel, id=-1,
                                      label=text, size=(300, 50), name='specimen_btn')
        self.btn4.SetBackgroundColour("#FDC68A")
        self.btn4.InitColours()
        self.Bind(wx.EVT_BUTTON, self.make_grid_frame, self.btn4)


        text = "5. add age data"
        self.btn5 = buttons.GenButton(self.panel, id=-1, label=text,
                                      size=(300, 50), name='age_btn')
        self.btn5.SetBackgroundColour("#6ECFF6")
        self.btn5.InitColours()
        self.Bind(wx.EVT_BUTTON, self.make_grid_frame, self.btn5)
        
        text = "6. add results data"
        self.btn6 = buttons.GenButton(self.panel, id=-1, label=text,
                                      size=(300, 50), name='result_btn')
        self.btn6.SetBackgroundColour("#C4DF9B")
        self.btn6.InitColours()
        self.Bind(wx.EVT_BUTTON, self.make_grid_frame, self.btn6)

        bsizer1a = wx.BoxSizer(wx.VERTICAL)
        bsizer1a.AddSpacer(20)
        bsizer1a.Add(self.btn1, wx.ALIGN_TOP)
        bsizer1a.AddSpacer(20)
        bsizer1a.Add(self.btn2, wx.ALIGN_TOP)
        bsizer1a.AddSpacer(20)
        bsizer1a.Add(self.btn3, wx.ALIGN_TOP)
        bsizer1a.AddSpacer(20)

        bSizer1.Add(bsizer1a, wx.ALIGN_CENTER, wx.EXPAND)
        bSizer1.AddSpacer(20)

        #bSizer1.Add(OR, 0, wx.ALIGN_CENTER, 0)
        bSizer1.AddSpacer(20)
        bsizer1b = wx.BoxSizer(wx.VERTICAL)
        #__init__(self, parent, id, label, pos, size, style, validator, name
        bsizer1b.Add(self.btn4, flag=wx.ALIGN_CENTER|wx.BOTTOM, border=20)
        bsizer1b.Add(self.btn5, 0, flag=wx.ALIGN_CENTER|wx.BOTTOM, border=20)
        bsizer1b.Add(self.btn6, 0, wx.ALIGN_CENTER, 0)
        bSizer1.Add(bsizer1b, 0, wx.ALIGN_CENTER, 0)
        bSizer1.AddSpacer(20)

        #---sizer 2 ----

        bSizer2 = wx.StaticBoxSizer(wx.StaticBox(self.panel, wx.ID_ANY, "Upload to MagIC database", name='bSizer2'), wx.HORIZONTAL)

        text = "prepare upload txt file"
        self.btn_upload = buttons.GenButton(self.panel, id=-1, label=text,
                                            size=(300, 50), name='upload_btn')
        self.btn_upload.SetBackgroundColour("#C4DF9B")
        self.btn_upload.InitColours()
        self.Bind(wx.EVT_BUTTON, self.on_upload_file, self.btn_upload)

        bSizer2.AddSpacer(20)
        bSizer2.Add(self.btn_upload, 0, wx.ALIGN_CENTER, 0)
        bSizer2.AddSpacer(20)
        #self.Bind(wx.EVT_BUTTON, self.on_btn_upload, self.btn_upload)


        #---arrange sizers ----

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(5)
        #vbox.Add(self.logo,0,wx.ALIGN_CENTER,0)
        vbox.AddSpacer(5)
        vbox.Add(bSizer0, 0, wx.ALIGN_CENTER, 0)
        vbox.AddSpacer(10)
        #vbox.Add(bSizer0_1, 0, wx.ALIGN_CENTER, 0)
        #vbox.AddSpacer(10)
        vbox.Add(bSizer1, 0, wx.ALIGN_CENTER, 0)
        vbox.AddSpacer(10)
        vbox.AddSpacer(10)
        hbox.AddSpacer(10)
        vbox.Add(bSizer2, 0, wx.ALIGN_CENTER, 0)
        vbox.AddSpacer(10)

        hbox.Add(vbox, 0, wx.ALIGN_CENTER, 0)
        hbox.AddSpacer(5)

        self.panel.SetSizer(hbox)
        hbox.Fit(self)

        # do menu
        menubar = MagICMenu(self)
        self.SetMenuBar(menubar)



    def on_change_dir_button(self, event):
        """
        create change directory frame
        """
        currentDirectory = self.WD #os.getcwd()
        change_dir_dialog = wx.DirDialog(self.panel, "choose directory:",
                                         defaultPath=currentDirectory,
                                         style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON | wx.DD_CHANGE_DIR)
        result = change_dir_dialog.ShowModal()
        if result == wx.ID_CANCEL:
            return
        if result == wx.ID_OK:
            self.WD = change_dir_dialog.GetPath()
            self.dir_path.SetValue(self.WD)
        change_dir_dialog.Destroy()
        wait = wx.BusyInfo('Initializing data object in new directory, please wait...')
        print '-I- Initializing magic data object'
        self.er_magic = builder.ErMagicBuilder(self.WD)
        print '-I- Read in any available data from working directory'
        self.er_magic.get_all_magic_info()
        print '-I- Initializing headers'
        self.er_magic.init_default_headers()
        self.er_magic.init_actual_headers()
        del wait


    def on_open_grid_frame(self):
        self.Hide()

    def on_close_grid_frame(self, event=None):
        if self.grid_frame.grid.changes:
            self.edited = True
        self.grid_frame = None
        self.Show()
        if event:
            event.Skip()    
        
    def make_grid_frame(self, event):
        """
        Create a GridFrame for data type of the button that was clicked
        """
        if self.grid_frame:
            print '-I- You already have a grid frame open'
            pw.simple_warning("You already have a grid open")
            return

        try:
            grid_type = event.GetButtonObj().Name[:-4] # remove '_btn'
        except AttributeError:
            grid_type = self.FindWindowById(event.Id).Name[:-4] # remove ('_btn')
        wait = wx.BusyInfo('Making {} grid, please wait...'.format(grid_type))
        self.on_open_grid_frame()
        self.grid_frame = grid_frame.GridFrame(self.er_magic, self.WD, grid_type, grid_type, self.panel)
        #self.on_finish_change_dir(self.change_dir_dialog)
        del wait

    def on_upload_file(self, event):
        """
        Write all data to appropriate er_* and pmag_* files.
        Then use those files to create a MagIC upload format file.
        Validate the upload file.
        """
        wait = wx.BusyInfo('Making upload file, please wait...')
        self.er_magic.write_files()
        upfile, error_message = ipmag.upload_magic(dir_path=self.WD)
        del wait
        if upfile:
            text = "You are ready to upload.\nYour file:\n{}\nwas generated in directory: \n{}\nDrag and drop this file in the MagIC database.".format(os.path.split(upfile)[1], self.WD)
            dlg = wx.MessageDialog(self, caption="Saved", message=text, style=wx.OK)
        else:
            text = "There were some problems with the creation of your upload file.\nError message: {}\nSee Terminal/Command Prompt for details".format(error_message)
            dlg = wx.MessageDialog(self, caption="Error", message=text, style=wx.OK)
        result = dlg.ShowModal()
        if result == wx.ID_OK:            
            dlg.Destroy()
        self.edited = False


class MagICMenu(wx.MenuBar):
    """
    initialize menu bar for QuickMagIC GUI
    """
    #pylint: disable=R0904
    #pylint: disable=R0914
    def __init__(self, parent):
        self.parent = parent
        super(MagICMenu, self).__init__()

        file_menu = wx.Menu()
        file_quit = file_menu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        file_clear = file_menu.Append(wx.ID_ANY, 'Clear directory', 'Delete all files from working directory')
        file_help = file_menu.Append(wx.ID_ANY, 'Help', 'More information about creating a MagIC contribution')
        file_show = file_menu.Append(wx.ID_ANY, 'Show main window', 'Show main window')
        file_close_grid = file_menu.Append(wx.ID_ANY, 'Close current grid', 'Close current grid')
        parent.Bind(wx.EVT_MENU, self.on_quit, file_quit)
        parent.Bind(wx.EVT_MENU, self.on_clear, file_clear)
        parent.Bind(wx.EVT_MENU, self.on_help, file_help)
        parent.Bind(wx.EVT_MENU, self.on_show_mainframe, file_show)
        parent.Bind(wx.EVT_MENU, self.on_close_grid, file_close_grid)

        self.Append(file_menu, 'File')

    def on_quit(self, event):
        """
        shut down application
        """
        if self.parent.grid_frame:
            if self.parent.grid_frame.grid.changes:
                dlg = wx.MessageDialog(self,caption="Message:", message="Are you sure you want to exit the program?\nYou have a grid open with unsaved changes.\n ", style=wx.OK|wx.CANCEL)
                result = dlg.ShowModal()
                if result == wx.ID_OK:
                    dlg.Destroy()
                else:
                    dlg.Destroy()
                    return
        if self.parent.grid_frame:
            self.parent.grid_frame.Destroy()
        # if there have been edits, save all data to files
        # before quitting
        if self.parent.edited:
            self.parent.er_magic.write_files()
        self.parent.Close()

    def on_clear(self, event):
        """
        initialize window to allow user to empty the working directory
        """
        dia = pmag_menu_dialogs.ClearWD(self.parent, self.parent.WD)
        clear = dia.do_clear()
        if clear:
            print '-I- Clear data object'
            self.parent.er_magic = builder.ErMagicBuilder(self.parent.WD, self.parent.data_model)
            print '-I- Initializing headers'
            self.parent.er_magic.init_default_headers()
            self.parent.er_magic.init_actual_headers()


    def on_help(self, event):
        """
        point user to Cookbook help
        """
        print "don't help yet"

    def on_show_mainframe(self, event):
        """
        Show main make_magic window
        """
        self.parent.Show()
        self.parent.Raise()

    def on_close_grid(self, event):
        """
        If there is an open grid, save its data and close it.
        """
        if self.parent.grid_frame:
            self.parent.grid_frame.onSave(None)
            self.parent.grid_frame.Destroy()


if __name__ == "__main__":
    #app = wx.App(redirect=True, filename="beta_log.log")
    # if redirect is true, wxpython makes its own output window for stdout/stderr
    #app = wx.App(redirect=False)
    print '-I- Creating application'
    # this sends stdout to terminal:
    #app = wx.App(redirect=False)
    # this sends stdout to wxPython:
    app = wx.App(redirect=True)
    working_dir = pmag.get_named_arg_from_sys('-WD', '.')
    app.frame = MainFrame(working_dir)
    if working_dir == '.':
        app.frame.on_change_dir_button(None)
    app.frame.Show()
    app.frame.Center()
    if '-i' in sys.argv:
        import wx.lib.inspection
        wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()

