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


class MainFrame(wx.Frame):
    """
    make magic
    """

    def __init__(self, WD=None, name='Main Frame'):
        wx.GetDisplaySize()
        wx.Frame.__init__(self, None, wx.ID_ANY, name=name)

        self.grid_frame = None
        self.panel = wx.Panel(self, size=wx.GetDisplaySize(), name='main panel')
        print '-I- Fetching working directory'
        self.WD = os.path.realpath(WD) or os.getcwd()

        print '-I- Initializing magic data object'
        self.data_model = validate_upload.get_data_model()
        self.er_magic = builder.ErMagicBuilder(self.WD, self.data_model)

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
            print self.grid_frame
            return
        try:
            grid_type = event.GetButtonObj().Name[:-4] # remove '_btn'
        except AttributeError:
            grid_type = self.FindWindowById(event.Id).Name[:-4] # remove ('_btn')
        self.on_open_grid_frame()
        self.grid_frame = GridFrame(self.er_magic, self.WD, grid_type, grid_type, self.panel)
        #self.on_finish_change_dir(self.change_dir_dialog)

    def on_upload_file(self, event):
        upfile, error_message = ipmag.upload_magic(dir_path=self.WD)
        if upfile:
            text = "You are ready to upload.\nYour file:\n{}\nwas generated in directory: \n{}\nDrag and drop this file in the MagIC database.".format(os.path.split(upfile)[1], self.WD)
            dlg = wx.MessageDialog(self, caption="Saved", message=text, style=wx.OK)
        else:
            text = "There were some problems with the creation of your upload file.\nError message: {}\nSee Terminal/Command Prompt for details".format(error_message)
            dlg = wx.MessageDialog(self, caption="Error", message=text, style=wx.OK)
        result = dlg.ShowModal()
        if result == wx.ID_OK:            
            dlg.Destroy()


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
        parent.Bind(wx.EVT_MENU, self.on_quit, file_quit)
        parent.Bind(wx.EVT_MENU, self.on_clear, file_clear)
        parent.Bind(wx.EVT_MENU, self.on_help, file_help)

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
                    #self.Destroy()
                else:
                    dlg.Destroy()
                    return
        #self.parent.Destroy()
        if self.parent.grid_frame:
            self.parent.grid_frame.Destroy()
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



    
class GridFrame(wx.Frame):
    """
    make_magic
    """

    def __init__(self, ErMagic, WD=None, frame_name="grid frame",
                 panel_name="grid panel", parent=None):
        self.parent = parent
        wx.GetDisplaySize()
        wx.Frame.__init__(self, parent=parent, id=wx.ID_ANY, name=frame_name)

        self.remove_cols_mode = False
        self.deleteRowButton = None
        self.selected_rows = set()

        self.er_magic = ErMagic

        self.panel = wx.Panel(self, name=panel_name, size=wx.GetDisplaySize())
        self.grid_type = panel_name

        if self.parent:
            self.Bind(wx.EVT_WINDOW_DESTROY, self.parent.Parent.on_close_grid_frame)

        #ancestry = [None, 'specimen', 'sample', 'site', 'location', None]
        if self.grid_type == 'age':
            self.current_age_type = 'site'
            self.child_type = 'sample'
            self.parent_type = 'location'
        else:
            try:
                self.child_type = self.er_magic.ancestry[self.er_magic.ancestry.index(self.grid_type) - 1]
                self.parent_type = self.er_magic.ancestry[self.er_magic.ancestry.index(self.grid_type) + 1]
            except ValueError:
                self.child_type = None
                self.parent_type = None

        self.WD = WD
        self.InitUI()


    ## Initialization functions
    
    def InitUI(self):
        """
        initialize window
        """
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        #self.er_magic = ErMagicBuilder.ErMagicBuilder(self.WD)#,self.Data,self.Data_hierarchy)

        self.init_grid_headers()
        
        self.grid = self.make_grid(self.parent_type)

        self.grid.InitUI()

        
        self.add_cols_button = wx.Button(self.panel, label="Add additional columns", name='add_cols_btn')
        self.Bind(wx.EVT_BUTTON, self.on_add_cols, self.add_cols_button)
        self.remove_cols_button = wx.Button(self.panel, label="Remove columns", name='remove_cols_btn')
        self.Bind(wx.EVT_BUTTON, self.on_remove_cols, self.remove_cols_button)
        self.remove_row_button = wx.Button(self.panel, label="Remove last row", name='remove_last_row_btn')
        self.Bind(wx.EVT_BUTTON, self.on_remove_row, self.remove_row_button)
        many_rows_box = wx.BoxSizer(wx.HORIZONTAL)
        self.add_many_rows_button = wx.Button(self.panel, label="Add row(s)", name='add_many_rows_btn')
        self.rows_spin_ctrl = wx.SpinCtrl(self.panel, value='1', initial=1, name='rows_spin_ctrl')
        many_rows_box.Add(self.add_many_rows_button, flag=wx.ALIGN_CENTRE)
        many_rows_box.Add(self.rows_spin_ctrl)
        self.Bind(wx.EVT_BUTTON, self.on_add_rows, self.add_many_rows_button)

        #hbox_grid = pw.hbox_grid(self.panel, self.on_remove_row, self.panel.Name, self.grid)
        self.deleteRowButton = wx.Button(self.panel, id=-1, label='Delete selected row(s)', name='delete_row_btn')
        self.Bind(wx.EVT_BUTTON, lambda event: self.on_remove_row(event, False), self.deleteRowButton)
        self.deleteRowButton.Disable()
        #self.deleteRowButton = hbox_grid.deleteRowButton

        self.msg_boxsizer = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1, name='msg_boxsizer'), wx.VERTICAL)
        self.default_msg_text = 'Edit {} here.\nYou can add or remove both rows and columns, however required columns may not be deleted.\nControlled vocabularies are indicated by **, and will have drop-down-menus.\nTo edit all values in a column, click the column header.\nYou can cut and paste a column of values from an Excel-like file.\nJust click the top cell and use command "v".'.format(self.grid_type + 's')
        self.msg_text = wx.StaticText(self.panel, label=self.default_msg_text,
                                      style=wx.TE_CENTER, name='msg text')
        self.msg_boxsizer.Add(self.msg_text)

        self.exitButton = wx.Button(self.panel, id=-1, label='Save and quit', name='save_and_quit_btn')
        self.Bind(wx.EVT_BUTTON, self.onSave, self.exitButton)
        self.cancelButton = wx.Button(self.panel, id=-1, label='Cancel', name='cancel_btn')
        self.Bind(wx.EVT_BUTTON, self.onCancelButton, self.cancelButton)
        self.pmag_checkbox = pw.check_box(self.panel,
                                         "Interpretations at {} level".format(self.grid_type))
        if self.grid_type in ('location', 'age', 'result'):
            self.pmag_checkbox.cb.SetValue(False)
            self.pmag_checkbox.cb.Disable()
            self.pmag_checkbox.ShowItems(False)
        else:
            self.pmag_checkbox.cb.SetValue(True)
            self.Bind(wx.EVT_CHECKBOX, self.on_pmag_checkbox, self.pmag_checkbox.cb)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        col_btn_vbox = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1, label='Columns'), wx.VERTICAL)
        row_btn_vbox = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1, label='Rows'), wx.VERTICAL)
        main_btn_vbox = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1, label='Manage data'), wx.VERTICAL)
        col_btn_vbox.Add(self.add_cols_button, flag=wx.ALL, border=5)
        col_btn_vbox.Add(self.remove_cols_button, flag=wx.ALL, border=5)
        row_btn_vbox.Add(many_rows_box, flag=wx.ALL, border=5)
        row_btn_vbox.Add(self.remove_row_button, flag=wx.ALL, border=5)
        row_btn_vbox.Add(self.deleteRowButton, flag=wx.ALL, border=5)
        main_btn_vbox.Add(self.exitButton, flag=wx.ALL, border=5)
        main_btn_vbox.Add(self.cancelButton, flag=wx.ALL, border=5)
        main_btn_vbox.Add(self.pmag_checkbox, flag=wx.ALL, border=5)
        hbox.Add(col_btn_vbox)
        hbox.Add(row_btn_vbox)
        hbox.Add(main_btn_vbox)

        self.panel.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.onLeftClickLabel, self.grid)

        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.panel.Bind(wx.EVT_TEXT_PASTE, self.do_fit)


        
        # add actual data!
        self.add_data_to_grid()
        if self.grid_type == 'age':
            self.add_age_data_to_grid()

        # add drop_down menus
        if self.parent_type:
            belongs_to = sorted(self.er_magic.data_lists[self.parent_type][0], key=lambda item: item.name)
        else:
            belongs_to = ''
        self.drop_down_menu = drop_down_menus.Menus(self.grid_type, self, self.grid, belongs_to)
        
        self.grid_box = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1), wx.VERTICAL)
        self.grid_box.Add(self.grid, flag=wx.ALL, border=5)

        # a few special touches if it is an age grid
        if self.grid_type == 'age':
            self.remove_row_button.Disable()
            self.add_many_rows_button.Disable()
            self.grid.SetColLabelValue(0, 'er_site_name')
            toggle_box = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1, label='Ages level'), wx.VERTICAL)
            toggle_box.Add(pw.labeled_yes_or_no(self.panel, 'Choose level to assign ages', 'site', 'sample'))
            self.Bind(wx.EVT_RADIOBUTTON, self.toggle_ages)
            hbox.Add(toggle_box)
            

        # a few special touches if it is a result grid
        if self.grid_type == 'result':
            # populate specimen_names, sample_names, etc.
            for row in range(self.grid.GetNumberRows()):
                result_name = self.grid.GetCellValue(row, 0)
                result = self.er_magic.find_by_name(result_name, self.er_magic.results)
                if result:
                    if result.specimens:
                        self.grid.SetCellValue(row, 2, ' : '.join([spec.name for spec in result.specimens]))
                    self.drop_down_menu.choices[2] = [sorted([spec.name for spec in self.er_magic.specimens if spec]), False]
                    if result.samples:
                        self.grid.SetCellValue(row, 3, ' : '.join([samp.name for samp in result.samples]))
                    self.drop_down_menu.choices[3] = [sorted([samp.name for samp in self.er_magic.samples if samp]), False]
                    if result.sites:
                        self.grid.SetCellValue(row, 4, ' : '.join([site.name for site in result.sites]))
                    self.drop_down_menu.choices[4] = [sorted([site.name for site in self.er_magic.sites if site]), False]
                    if result.locations:
                        self.grid.SetCellValue(row, 5, ' : '.join([loc.name for loc in result.locations]))
                    self.drop_down_menu.choices[5] = [sorted([loc.name for loc in self.er_magic.locations if loc]), False]

        # final layout, set size
        self.main_sizer.Add(hbox, flag=wx.ALL, border=20)
        self.main_sizer.Add(self.msg_boxsizer, flag=wx.BOTTOM|wx.ALIGN_CENTRE, border=10)
        self.main_sizer.Add(self.grid_box, flag=wx.ALL, border=10)
        self.panel.SetSizer(self.main_sizer)

        self.main_sizer.Fit(self)
        ## this works for the initial sizing
        num_rows = len(self.grid.row_labels)
        if num_rows in range(0, 4):
            height = {0: 70, 1: 70, 2: 90, 3: 110, 4: 130}
            self.grid.SetSize((-1, height[num_rows]))
        ## this keeps sizing correct if the user resizes the window manually
        self.Bind(wx.EVT_SIZE, self.resize_grid)

                    
        self.Centre()
        self.Show()

    def on_key_down(self, event):
        """
        If user does command v, re-size window in case pasting has changed the content size.
        """
        keycode = event.GetKeyCode()
        meta_down = event.MetaDown()
        if keycode == 86 and meta_down:
            # treat it as if it were a wx.EVT_TEXT_SIZE
            self.do_fit(event)

        
    def do_fit(self, event):
        """
        Re-fit the window to the size of the content.
        """
        self.main_sizer.Fit(self)

    def toggle_ages(self, event):
        label = event.GetEventObject().Label
        if label == 'sample':
            new_parent_type = 'site'
            self.current_age_type = 'site'
        if label == 'site':
            new_parent_type = 'location'
            self.current_age_type = 'sample'
        self.onSave(None)

        self.grid.Destroy()
        # prevent mainframe from popping up in front of age grid
        # does create an unfortunate flashing effect, though.  
        self.parent.Parent.Hide()

        self.grid = self.make_grid(new_parent_type)

        self.grid.InitUI()
        self.panel.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.onLeftClickLabel, self.grid)
        
        self.add_data_to_grid(label)
        self.add_age_data_to_grid(label)

        belongs_to = sorted(self.er_magic.data_lists[new_parent_type][0], key=lambda item: item.name)
        self.drop_down_menu = drop_down_menus.Menus(self.grid_type, self, self.grid, belongs_to)

        self.grid.SetColLabelValue(1, 'er_' + new_parent_type + '_name')
        self.grid.SetColLabelValue(0, 'er_' + label + '_name')
        self.grid.size_grid()
        
        self.grid_box.Add(self.grid, flag=wx.ALL, border=5)

        ## this works for the initial sizing
        num_rows = len(self.grid.row_labels)
        if num_rows in range(0, 4):
            height = {0: 70, 1: 70, 2: 90, 3: 110, 4: 130}
            self.grid.SetSize((-1, height[num_rows]))

        self.main_sizer.Fit(self)


        
    def init_grid_headers(self):
        self.grid_headers = self.er_magic.headers
        

    def make_grid(self, parent_type=None):
        """
        return grid
        """
        er_header = self.grid_headers[self.grid_type]['er'][0]
        pmag_header = self.grid_headers[self.grid_type]['pmag'][0]
        header = sorted(list(set(er_header).union(pmag_header)))
        first_headers = []
        for string in ['citation', '{}_class'.format(self.grid_type),
                       '{}_lithology'.format(self.grid_type), '{}_type'.format(self.grid_type),
                      'site_definition']:
            for head in header[:]:
                if string in head:
                    header.remove(head)
                    first_headers.append(head)

        # do headers for results type grid
        if self.grid_type == 'result':
            header.remove('pmag_result_name')
            header[:0] = ['pmag_result_name', 'er_citation_names', 'er_specimen_names',
                          'er_sample_names', 'er_site_names', 'er_location_names']
        elif self.grid_type == 'age':
            for header_type in self.er_magic.first_age_headers:
                if header_type in header:
                    header.remove(header_type)
            lst = ['er_' + self.grid_type + '_name', 'er_' + self.parent_type + '_name']
            lst.extend(self.er_magic.first_age_headers)
            header[:0] = lst

        # do headers for all other data types without parents
        elif not parent_type:
            lst = ['er_' + self.grid_type + '_name']
            lst.extend(first_headers)
            header[:0] = lst
        # do headers for all data types with parents
        else:
            lst = ['er_' + self.grid_type + '_name', 'er_' + self.parent_type + '_name']
            lst.extend(first_headers)
            header[:0] = lst

        grid = magic_grid.MagicGrid(parent=self.panel, name=self.grid_type,
                                    row_labels=[], col_labels=header)
        grid.do_event_bindings()
        return grid


    def add_age_data_to_grid(self, dtype='site'):
        row_labels = [self.grid.GetCellValue(row, 0) for row in range(self.grid.GetNumberRows())]
        items_list = self.er_magic.data_lists[dtype][0]
        items = [self.er_magic.find_by_name(label, items_list) for label in row_labels if label]

        col_labels = self.grid.col_labels[2:]
        if not items:
            return
        for row_num, item in enumerate(items):
            for col_num, label in enumerate(col_labels):
                col_num += 2
                if not label in item.age_data.keys():
                    item.age_data[label] = ''
                cell_value = item.age_data[label]
                if cell_value:
                    self.grid.SetCellValue(row_num, col_num, cell_value)

    
    def add_data_to_grid(self, grid_type=None):
        if not grid_type:
            grid_type = self.grid_type
        rows = self.er_magic.data_lists[grid_type][0]
        self.grid.add_items(rows)
        self.grid.size_grid()

        # always start with at least one row:
        if not self.grid.row_labels:
            self.grid.add_row()


    ##  Grid event methods
    
    def resize_grid(self, event):
        if event:
            event.Skip()
        num_rows = len(self.grid.row_labels)
        if num_rows in range(0, 4):
            height = {0: 70, 1: 70, 2: 90, 3: 110, 4: 130}
            self.grid.SetSize((-1, height[num_rows]))
        self.main_sizer.Fit(self)
        # the last line means you can't resize the window to be bigger
        # than it naturally sizes to be based on its contents
        # (since every time a resize event is fired, the .Fit method is also fired)

    def remove_col_label(self, event):#, include_pmag=True):
        """
        check to see if column is required
        if it is not, delete it from grid
        """
        include_pmag = self.pmag_checkbox.cb.IsChecked()
        er_possible_headers = self.grid_headers[self.grid_type]['er'][2]
        pmag_possible_headers = self.grid_headers[self.grid_type]['pmag'][2]
        er_actual_headers = self.grid_headers[self.grid_type]['er'][0]
        pmag_actual_headers = self.grid_headers[self.grid_type]['pmag'][0]
        col = event.GetCol()
        label = self.grid.GetColLabelValue(col)
        if '**' in label:
            label = label.strip('**')
        if label in self.grid_headers[self.grid_type]['er'][1]:
            pw.simple_warning("That header is required, and cannot be removed")
            return False
        elif include_pmag and label in self.grid_headers[self.grid_type]['pmag'][1]:
            pw.simple_warning("That header is required, and cannot be removed")
            return False
        else:
            print 'That header is not required:', label
            #print 'self.grid_headers', self.grid_headers[self.grid_type]
            self.grid.remove_col(col)
            if label in er_possible_headers:
                try:
                    er_actual_headers.remove(label)
                except ValueError:
                    pass
            if label in pmag_possible_headers:
                try:
                    pmag_actual_headers.remove(label)
                except ValueError:
                    pass

    def on_add_cols(self, event):
        """
        Show simple dialog that allows user to add a new column name
        """

        col_labels = self.grid.col_labels
        er_items = [head for head in self.grid_headers[self.grid_type]['er'][2] if head not in col_labels]
        pmag_items = [head for head in self.grid_headers[self.grid_type]['pmag'][2] if head not in er_items and head not in col_labels]
        dia = pw.HeaderDialog(self, 'columns to add', er_items, pmag_items)
        result = dia.ShowModal()
        new_headers = []
        if result == 5100:
            new_headers = dia.text_list
        if not new_headers:
            return
        for name in new_headers:
            if name:
                if name not in self.grid.col_labels:
                    self.grid.add_col(name)
                    # add to appropriate headers list
                    if name in er_items:
                        self.grid_headers[self.grid_type]['er'][0].append(name)
                    if name in pmag_items:
                        self.grid_headers[self.grid_type]['pmag'][0].append(name)
                else:
                    pw.simple_warning('You are already using column header: {}'.format(name))
        self.main_sizer.Fit(self)
        self.grid.changes = set(range(self.grid.GetNumberRows()))


    def on_remove_cols(self, event):
        """
        enter 'remove columns' mode
        """
        # first unselect any selected cols/cells
        self.remove_cols_mode = True
        self.grid.ClearSelection()
        self.remove_cols_button.SetLabel("end delete column mode")
        # change button to exit the delete columns mode
        self.Unbind(wx.EVT_BUTTON, self.remove_cols_button)
        self.Bind(wx.EVT_BUTTON, self.exit_col_remove_mode, self.remove_cols_button)
        # then disable all other buttons
        for btn in [self.add_cols_button, self.remove_row_button, self.add_many_rows_button]:
            btn.Disable()
        # then make some visual changes
        self.msg_text.SetLabel("Remove grid columns: click on a column header to delete it.  Required headers for {}s may not be deleted.".format(self.grid_type))
        self.msg_boxsizer.Fit(self.msg_boxsizer.GetStaticBox())
        self.main_sizer.Fit(self)
        self.grid.SetWindowStyle(wx.DOUBLE_BORDER)
        self.grid_box.GetStaticBox().SetWindowStyle(wx.DOUBLE_BORDER)
        self.grid.Refresh()
        self.main_sizer.Fit(self) # might not need this one
        self.grid.changes = set(range(self.grid.GetNumberRows()))


    def on_add_rows(self, event):
        """
        add rows to grid
        """
        num_rows = self.rows_spin_ctrl.GetValue()
        last_row = self.grid.GetNumberRows()
        for row in range(num_rows):
            self.grid.add_row()
            #if not self.grid.changes:
            #    self.grid.changes = set([])
            #self.grid.changes.add(last_row)
            #last_row += 1
        self.main_sizer.Fit(self)

    def on_remove_row(self, event, row_num=-1):
        """
        Remove specified grid row.
        If no row number is given, remove the last row.
        """
        #data_type = self.Name
        if row_num == -1:
            default = (255, 255, 255, 255)
            # unhighlight any selected rows:
            for row in self.selected_rows:
                attr = wx.grid.GridCellAttr()
                attr.SetBackgroundColour(default)
                self.grid.SetRowAttr(row, attr)
            row_num = self.grid.GetNumberRows() - 1
            self.deleteRowButton.Disable()
            self.selected_rows = {row_num}
            
        #else:
        function_mapping = {'specimen': self.er_magic.delete_specimen,
                            'sample': self.er_magic.delete_sample,
                            'site': self.er_magic.delete_site,
                            'location': self.er_magic.delete_location,
                            'result': self.er_magic.delete_result}
        #ancestry = ['er_specimens', 'er_samples', 'er_sites', 'er_locations']
        #child_type = ancestry[ancestry.index(self.grid_type) - 1]
        
        names = [self.grid.GetCellValue(row, 0) for row in self.selected_rows]
        orphans = []
        for name in names:
            row = self.grid.row_labels.index(name)
            function_mapping[self.grid_type](name)
            orphans.extend([name])
            self.grid.remove_row(row)
        self.selected_rows = set()

        self.deleteRowButton.Disable()
        self.grid.Refresh()

        self.main_sizer.Fit(self)

    def exit_col_remove_mode(self, event):
        """
        go back from 'remove cols' mode to normal
        """
        self.remove_cols_mode = False
        # re-enable all buttons
        for btn in [self.add_cols_button, self.remove_row_button, self.add_many_rows_button]:
            btn.Enable()

        # unbind grid click for deletion
        self.Unbind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK)
        # undo visual cues
        self.grid.SetWindowStyle(wx.DEFAULT)
        self.grid_box.GetStaticBox().SetWindowStyle(wx.DEFAULT)
        self.msg_text.SetLabel(self.default_msg_text)
        self.msg_boxsizer.Fit(self.msg_boxsizer.GetStaticBox())
        self.main_sizer.Fit(self)
        # re-bind self.remove_cols_button
        self.Bind(wx.EVT_BUTTON, self.on_remove_cols, self.remove_cols_button)
        self.remove_cols_button.SetLabel("Remove columns")


    def onSelectRow(self, event):
        """
        Highlight or unhighlight a row for possible deletion.
        """
        grid = self.grid
        row = event.Row
        default = (255, 255, 255, 255)
        highlight = (191, 216, 216, 255)
        cell_color = grid.GetCellBackgroundColour(row, 0)
        attr = wx.grid.GridCellAttr()
        if cell_color == default:
            attr.SetBackgroundColour(highlight)
            self.selected_rows.add(row)
        else:
            attr.SetBackgroundColour(default)
            try:
                self.selected_rows.remove(row)
            except KeyError:
                pass
        if self.selected_rows and self.deleteRowButton:
            self.deleteRowButton.Enable()
        else:
            self.deleteRowButton.Disable()
        grid.SetRowAttr(row, attr)
        grid.Refresh()

    def onLeftClickLabel(self, event):
        """
        When user clicks on a grid label, determine if it is a row label or a col label.
        Pass along the event to the appropriate function.
        (It will either highlight a column for editing all values, or highlight a row for deletion).
        """
        if event.Col == -1 and event.Row == -1:
            pass
        if event.Row < 0:
            if self.remove_cols_mode:
                self.remove_col_label(event)
            else:
                self.drop_down_menu.on_label_click(event)
        else:
            if event.Col < 0  and self.grid_type != 'age':
                self.onSelectRow(event)


    ## Meta buttons -- cancel & save functions

    def on_pmag_checkbox(self, event):
        """
        Called when user changes status of pmag_checkbox.
        Removes pmag-specific columns if box is unchecked.
        Adds in pmag-specific columns if box is checked.
        """
        num_cols = self.grid.GetNumberCols()
        current_grid_col_labels = [self.grid.GetColLabelValue(num) for num in range(num_cols)]
        do_pmag = self.pmag_checkbox.cb.IsChecked()
        # add in pmag-specific headers
        if do_pmag:
            for col_label in self.er_magic.headers[self.grid_type]['pmag'][0]:
                if col_label not in current_grid_col_labels:
                    self.grid.add_col(col_label)
        # remove pmag-specific headers
        if not do_pmag:
            for col_label in self.er_magic.headers[self.grid_type]['pmag'][0]:
                if col_label not in self.er_magic.headers[self.grid_type]['er'][0]:
                    num_cols = self.grid.GetNumberCols()
                    current_grid_col_labels = [self.grid.GetColLabelValue(num) for num in range(num_cols)]
                    ind = current_grid_col_labels.index(col_label)
                    self.grid.remove_col(ind)
        self.main_sizer.Fit(self)
    
    def onCancelButton(self, event):
        if self.grid.changes:
            dlg1 = wx.MessageDialog(self,caption="Message:", message="Are you sure you want to exit this grid?\nYour changes will not be saved.\n ", style=wx.OK|wx.CANCEL)
            result = dlg1.ShowModal()
            if result == wx.ID_OK:
                dlg1.Destroy()    
                self.Destroy()
        else:
            self.Destroy()

    def onSave(self, event):#, age_data_type='site'):
        """
        Save grid data and write it to file
        """
        if not self.grid.changes:
            return

        if self.grid_type == 'age':
            age_data_type = self.current_age_type
        if self.drop_down_menu:
            self.drop_down_menu.clean_up()

        starred_cols = self.grid.remove_starred_labels()

        self.grid.SaveEditControlValue() # locks in value in cell currently edited
        
        if self.parent_type:
            parent_search_list = self.er_magic.data_lists[self.parent_type][0]
        item_search_list = self.er_magic.data_lists[self.grid_type][0]
        items_list = []
        if self.grid.changes:
            num_cols = self.grid.GetNumberCols()

            for change in self.grid.changes:
                if change == -1:
                    continue
                else:
                    old_item = self.grid.row_items[change]
                    new_item_name = self.grid.GetCellValue(change, 0)
                    new_er_data = {}
                    new_pmag_data = {}
                    er_header = self.grid_headers[self.grid_type]['er'][0]
                    pmag_header = self.grid_headers[self.grid_type]['pmag'][0]
                    start_num = 2 if self.parent_type else 1
                    result_data = {}

                    for col in range(start_num, num_cols):
                        col_label = str(self.grid.GetColLabelValue(col))
                        value = str(self.grid.GetCellValue(change, col))
                        #new_data[col_label] = value
                        if er_header and col_label in er_header:
                            new_er_data[col_label] = value

                        if pmag_header and col_label in pmag_header:
                            new_pmag_data[col_label] = value

                        if col_label in ['er_specimen_names', 'er_sample_names',
                                         'er_site_names', 'er_location_names']:
                            result_data[col_label] = value

                    # if there is an item
                    if isinstance(old_item, str):
                        old_item_name = None
                    else:
                        old_item_name = self.grid.row_items[change].name

                    if self.parent_type:
                        new_parent_name = self.grid.GetCellValue(change, 1)
                        #new_parent = self.er_magic.find_by_name(new_parent_name, parent_search_list)
                    else:
                        new_parent_name = ''

                    # create a new item
                    if new_item_name and not old_item_name:
                        
                        print 'make new item named', new_item_name
                        if self.grid_type == 'result':
                            specs, samps, sites, locs = self.get_result_children(result_data)
                            item = self.er_magic.add_result(new_item_name, specs, samps, sites,
                                                            locs, new_pmag_data)
                        else:
                            item = self.er_magic.add_methods[self.grid_type](new_item_name, new_parent_name,
                                                                             new_er_data, new_pmag_data)

                    # update an existing item
                    elif new_item_name and old_item_name:
                        print 'update existing {} formerly named {} to {}'.format(self.grid_type,
                                                                                  old_item_name,
                                                                                  new_item_name)
                        if self.grid_type == 'result':
                            specs, samps, sites, locs = self.get_result_children(result_data)
                            item = self.er_magic.update_methods['result'](old_item_name, new_item_name,
                                                                          new_er_data=None,
                                                                          new_pmag_data=new_pmag_data,
                                                                          spec_names=specs,
                                                                          samp_names=samps,
                                                                          site_names=sites,
                                                                          loc_names=locs,
                                                                          replace_data=True)
                        elif self.grid_type == 'age':
                            #  need to somehow specify site/sample here.....
                            site_or_sample = age_data_type
                            item = self.er_magic.update_methods['age'](old_item_name, new_er_data,
                                                                       site_or_sample, replace_data=True)
                        else:
                            item = self.er_magic.update_methods[self.grid_type](old_item_name, new_item_name,
                                                                                new_parent_name, new_er_data,
                                                                                new_pmag_data, replace_data=True)

        if self.grid_type == 'result':
            self.er_magic.write_result_file()
            wx.MessageBox('Saved!', 'Info',
              style=wx.OK | wx.ICON_INFORMATION)
            self.Destroy()
            return
        if self.grid_type == 'age':
            print 'self.grid.changes', self.grid.changes
            self.er_magic.write_age_file(age_data_type)
            wx.MessageBox('Saved!', 'Info',
              style=wx.OK | wx.ICON_INFORMATION)
            if not event:
                return
            self.Destroy()
            return

        
        do_pmag = self.pmag_checkbox.cb.IsChecked()
        self.er_magic.write_magic_file(self.grid_type, do_pmag=do_pmag)
        if not do_pmag:
            pmag_file = os.path.join(self.WD, 'pmag_' + self.grid_type + 's.txt')
            if os.path.isfile(pmag_file):
                os.remove(pmag_file)
                
        wx.MessageBox('Saved!', 'Info',
                      style=wx.OK | wx.ICON_INFORMATION)
        self.Destroy()


    def get_result_children(self, result_data):
        """
        takes in dict in form of {'er_specimen_names': 'name1:name2:name3'}
        and so forth.
        returns lists of specimens, samples, sites, and locations
        """
        if result_data['er_specimen_names']:
            specimens = result_data['er_specimen_names'].split(":")
        else:
            specimens = ''
        if result_data['er_sample_names']:
            samples = result_data['er_sample_names'].split(":")
        else:
            samples = ''
        if result_data['er_site_names']:
            sites = result_data['er_site_names'].split(":")
        else:
            sites = ''
        if result_data['er_location_names']:
            locations = result_data['er_location_names'].split(":")
        else:
            locations = ''
        return specimens, samples, sites, locations

        # for QuickMagIC er_magic_builder, this happens in ErMagicCheckFrame:
        
        ## check that all required data is present
        #validation_errors = self.validate(grid)



if __name__ == "__main__":
    #app = wx.App(redirect=True, filename="beta_log.log")
    # if redirect is true, wxpython makes its own output window for stdout/stderr
    #app = wx.PySimpleApp(redirect=False)
    print '-I- Creating application'
    app = wx.App(redirect=False)
    working_dir = pmag.get_named_arg_from_sys('-WD', '.')
    app.frame = MainFrame(working_dir)
    app.frame.Show()
    app.frame.Center()
    if '-i' in sys.argv:
        import wx.lib.inspection
        wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()

