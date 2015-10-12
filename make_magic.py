#!/usr/bin/env pythonw
"""
doc string
"""

# pylint: disable=C0103

import wx
import wx.lib.buttons as buttons
import sys
import ErMagicBuilder
import pmag
import pmag_er_magic_dialogs
import pmag_widgets as pw



class MainFrame(wx.Frame):
    """
    make magic
    """

    def __init__(self, WD=None):
        wx.GetDisplaySize()
        wx.Frame.__init__(self, None, wx.ID_ANY, 'Title')
        self.panel = wx.Panel(self, size=wx.GetDisplaySize())
        self.WD = WD
        self.InitUI()

    def InitUI(self):
        bSizer0 = wx.StaticBoxSizer(wx.StaticBox(self.panel, wx.ID_ANY, "Choose MagIC project directory"), wx.HORIZONTAL)
        self.dir_path = wx.TextCtrl(self.panel, id=-1, size=(600,25), style=wx.TE_READONLY)
        self.change_dir_button = buttons.GenButton(self.panel, id=-1, label="change dir",size=(-1, -1))
        self.change_dir_button.SetBackgroundColour("#F8F8FF")
        self.change_dir_button.InitColours()
        self.Bind(wx.EVT_BUTTON, self.on_change_dir_button, self.change_dir_button)
        bSizer0.Add(self.change_dir_button, wx.ALIGN_LEFT)
        bSizer0.AddSpacer(40)
        bSizer0.Add(self.dir_path, wx.ALIGN_CENTER_VERTICAL)

    def on_change_dir_button(self, event):
        pass


    def InitMenubar(self):
        pass



class GridFrame(wx.Frame):
    """
    make_magic
    """

    def __init__(self, WD=None, panel_name="panel"):
        wx.GetDisplaySize()
        wx.Frame.__init__(self, None, wx.ID_ANY, 'Title')
        self.panel = wx.Panel(self, name=panel_name, size=wx.GetDisplaySize())
        self.WD = WD
        self.InitUI()


    def InitUI(self):
        """
        initialize window
        """
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.ErMagic = ErMagicBuilder.ErMagicBuilder(self.WD)#,self.Data,self.Data_hierarchy)
        self.ErMagic.init_default_headers()

        # have this set in a more reasonable way
        self.grid_type = 'er_specimens'
        self.grid_headers = {'er_specimens': [self.ErMagic.er_specimens_header, self.ErMagic.er_specimens_reqd_header, self.ErMagic.er_specimens_optional_header], 'er_samples': [self.ErMagic.er_samples_header, self.ErMagic.er_samples_reqd_header, self.ErMagic.er_samples_optional_header]}

        self.grid = self.make_grid()

        self.grid.InitUI()
        self.add_col_button = wx.Button(self.panel, label="Add additional column")
        self.Bind(wx.EVT_BUTTON, self.on_add_col, self.add_col_button)
        self.remove_cols_button = wx.Button(self.panel, label="Remove columns")
        self.Bind(wx.EVT_BUTTON, self.on_remove_cols, self.remove_cols_button)
        self.remove_row_button = wx.Button(self.panel, label="Remove last row")
        self.Bind(wx.EVT_BUTTON, self.on_remove_row, self.remove_row_button)
        many_rows_box = wx.BoxSizer(wx.HORIZONTAL)
        self.add_many_rows_button = wx.Button(self.panel, label="Add row(s)")
        self.rows_spin_ctrl = wx.SpinCtrl(self.panel, value='1', initial=1)
        many_rows_box.Add(self.add_many_rows_button, flag=wx.ALIGN_CENTRE)
        many_rows_box.Add(self.rows_spin_ctrl)
        self.Bind(wx.EVT_BUTTON, self.on_add_rows, self.add_many_rows_button)

        self.msg_boxsizer = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1), wx.VERTICAL)
        self.msg_text = wx.StaticText(self.panel, label='blah blah blah', style=wx.TE_CENTER, name='msg text')
        self.msg_boxsizer.Add(self.msg_text)
        self.msg_boxsizer.ShowItems(False)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        col_btn_vbox = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1), wx.VERTICAL)
        row_btn_vbox = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1), wx.VERTICAL)
        col_btn_vbox.Add(self.add_col_button, flag=wx.ALL, border=5)
        col_btn_vbox.Add(self.remove_cols_button, flag=wx.ALL, border=5)
        row_btn_vbox.Add(many_rows_box, flag=wx.ALL, border=5)
        row_btn_vbox.Add(self.remove_row_button, flag=wx.ALL, border=5)
        hbox.Add(col_btn_vbox)
        hbox.Add(row_btn_vbox)

        self.grid.size_grid()
        self.grid_box = wx.StaticBoxSizer(wx.StaticBox(self.panel, -1), wx.VERTICAL)
        self.grid_box.Add(self.grid, flag=wx.ALL, border=5)

        #grid_box.GetStaticBox().SetBackgroundColour(wx.RED)
        #self.grid.SetBackgroundColour(wx.RED)

        self.main_sizer.Add(hbox, flag=wx.ALL, border=20)
        self.main_sizer.Add(self.msg_boxsizer, flag=wx.BOTTOM|wx.ALIGN_CENTRE, border=10)
        self.main_sizer.Add(self.grid_box, flag=wx.ALL, border=10)
        self.panel.SetSizer(self.main_sizer)

        self.main_sizer.Fit(self)

    def remove_col_label(self, event):
        """
        check to see if column is required
        if it is not, delete it from grid
        """
        col = event.GetCol()
        label = self.grid.GetColLabelValue(col)
        if label in self.grid_headers[self.grid_type][1]:
            pw.simple_warning("That header is required, and cannot be removed")
            return False
        else:
            self.grid.remove_col(col)

    def make_grid(self):
        """
        return grid
        """
        header = self.grid_headers[self.grid_type][0]
        #col_labels = self.ErMagic.er_locations_header
        grid = pmag_er_magic_dialogs.MagicGrid(self.panel, self.grid_type, [''], header)#, (300, 300))
        return grid

    def on_add_col(self, event):
        """
        Show simple dialog that allows user to add a new column name
        """
        items = self.grid_headers[self.grid_type][2]
        #dia = pw.TextDialog(self, 'column name: ')
        dia = pw.ComboboxDialog(self, 'new column name:', items)
        result = dia.ShowModal()
        if result == wx.ID_OK:
            name = dia.combobox.GetValue()
            if name:
                self.grid.add_col(name)
            else:
                pw.simple_warning("New column must have a name")
        self.main_sizer.Fit(self)

    def on_remove_cols(self, event):
        """
        enter 'remove columns' mode
        """
        # first unselect any selected cols/cells
        self.grid.ClearSelection()
        self.remove_cols_button.SetLabel("end delete column mode")
        # change button to exit the delete columns mode
        self.Unbind(wx.EVT_BUTTON, self.remove_cols_button)
        self.Bind(wx.EVT_BUTTON, self.exit_col_remove_mode, self.remove_cols_button)
        # then disable all other buttons
        for btn in [self.add_col_button, self.remove_row_button, self.add_many_rows_button]:
            btn.Disable()
        # then make some visual changes
        self.msg_text.SetLabel("Edit grid columns: click on a column header to delete it")
        self.msg_boxsizer.ShowItems(True)
        self.main_sizer.Fit(self)
        self.grid.SetWindowStyle(wx.DOUBLE_BORDER)
        self.grid_box.GetStaticBox().SetWindowStyle(wx.DOUBLE_BORDER)
        self.grid.Refresh()
        self.main_sizer.Fit(self) # might not need this one
        # then make binding so that clicking on a label makes that column disappear
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.remove_col_label)
        # make sure reqd cols do not disappear, or at least come with a warning

    def on_add_rows(self, event):
        """
        add rows to grid
        """
        num_rows = self.rows_spin_ctrl.GetValue()
        for row in range(num_rows):
            self.grid.add_row()
        self.main_sizer.Fit(self)

    def on_remove_row(self, event):
        """
        remove the last row in the grid
        """
        self.grid.remove_row()
        self.main_sizer.Fit(self)

    def exit_col_remove_mode(self, event):
        """
        go back from 'remove cols' mode to normal
        """
        # re-enable all buttons
        for btn in [self.add_col_button, self.remove_row_button, self.add_many_rows_button]:
            btn.Enable()

        # unbind grid click for deletion
        self.Unbind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK)
        # undo visual cues
        self.grid.SetWindowStyle(wx.DEFAULT)
        self.grid_box.GetStaticBox().SetWindowStyle(wx.DEFAULT)
        self.msg_boxsizer.ShowItems(False)
        self.main_sizer.Fit(self)
        # re-bind self.remove_cols_button
        self.Bind(wx.EVT_BUTTON, self.on_remove_cols, self.remove_cols_button)
        self.remove_cols_button.SetLabel("Remove columns")



if __name__ == "__main__":
    #app = wx.App(redirect=True, filename="beta_log.log")
    # if redirect is true, wxpython makes its own output window for stdout/stderr
    #app = wx.PySimpleApp(redirect=False)
    app = wx.App(redirect=False)
    working_dir = pmag.get_named_arg_from_sys('-WD', '.')
    app.frame = MainFrame(working_dir)
    app.frame.Show()
    app.frame.Center()
    if '-i' in sys.argv:
        import wx.lib.inspection
        wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()

