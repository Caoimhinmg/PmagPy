#!/usr/bin/env pythonw
import wx
import wx.lib.buttons as buttons
#import thellier_gui_dialogs
import os
import sys
import datetime
import pmag
import pmag_basic_dialogs
import pmag_menu




class MagMainFrame(wx.Frame):
    """"""
    try:
        version= pmag.get_version()
    except:
        version=""
    title = "QuickMagIC   version: %s"%version

    def __init__(self):
        
        self.FIRST_RUN=True
        wx.Frame.__init__(self, None, wx.ID_ANY, self.title)
        self.panel = wx.Panel(self)
        self.InitUI()
        #self.create_menu()
        self.get_DIR()        # choose directory dialog                    
        self.HtmlIsOpen=False
        self.first_time_messsage=False
        self.Bind(wx.EVT_CLOSE, self.on_menu_exit)
        self.Data, self.Data_hierarchy = {}, {}


    def InitUI(self):

        menubar = pmag_menu.MagICMenu(self)
        self.SetMenuBar(menubar)


        #pnl = self.panel

        #---sizer logo ----
                
        #start_image = wx.Image("/Users/ronshaar/PmagPy/images/logo2.png")
        #start_image = wx.Image("/Users/Python/simple_examples/001.png")
        #start_image.Rescale(start_image.GetWidth(), start_image.GetHeight())
        #image = wx.BitmapFromImage(start_image)
        #self.logo = wx.StaticBitmap(self.panel, -1, image) 


        #---sizer 0 ----


        bSizer0 = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, "Choose MagIC project directory" ), wx.HORIZONTAL )
        self.dir_path = wx.TextCtrl(self.panel, id=-1, size=(600,25), style=wx.TE_READONLY)
        self.change_dir_button = buttons.GenButton(self.panel, id=-1, label="change dir",size=(-1, -1))
        self.change_dir_button.SetBackgroundColour("#F8F8FF")
        self.change_dir_button.InitColours()
        self.Bind(wx.EVT_BUTTON, self.on_change_dir_button,self.change_dir_button)
        bSizer0.Add(self.change_dir_button,wx.ALIGN_LEFT)
        bSizer0.AddSpacer(40)
        bSizer0.Add(self.dir_path,wx.ALIGN_CENTER_VERTICAL)
        
        #
        # last saved: []
        bSizer0_1 = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, "Save MagIC project directory in current state or revert to last-saved state" ), wx.HORIZONTAL ) 
        saved_label = wx.StaticText(self.panel, -1, "Last saved:", (20, 120))
        self.last_saved= wx.TextCtrl(self.panel, id=-1, size=(100,25), style=wx.TE_READONLY)
        now = datetime.datetime.now()
        now_string = "{}:{}:{}".format(now.hour, now.minute, now.second)
        self.last_saved.write(now_string)
        self.save_dir_button = buttons.GenButton(self.panel, id=-1, label = "save dir", size=(-1, -1))
        self.revert_dir_button = buttons.GenButton(self.panel, id=-1, label = "revert dir", size=(-1, -1))

        self.Bind(wx.EVT_BUTTON, self.on_revert_dir_button, self.revert_dir_button)
        self.Bind(wx.EVT_BUTTON, self.on_save_dir_button, self.save_dir_button)

        bSizer0_1.Add(saved_label, flag=wx.RIGHT, border=10)
        bSizer0_1.Add(self.last_saved, flag=wx.RIGHT, border=10)
        bSizer0_1.Add(self.save_dir_button,flag=wx.ALIGN_LEFT|wx.RIGHT, border=10)
        bSizer0_1.Add(self.revert_dir_button,wx.ALIGN_LEFT)

        #
    
                
                                
        #---sizer 1 ----
        bSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, "Import MagIC formatted data to working directory" ), wx.HORIZONTAL )
        
        TEXT="1. convert magnetometer files to MagIC format"
        self.btn1=buttons.GenButton(self.panel, id=-1, label=TEXT,size=(450, 50))        
        self.btn1.SetBackgroundColour("#FDC68A")
        self.btn1.InitColours()
        self.Bind(wx.EVT_BUTTON, self.on_convert_file,self.btn1)
        TEXT="2. (optional) calculate geographic/tilt-corrected directions"
        self.btn2 =buttons.GenButton(self.panel, id=-1, label=TEXT,size=(450, 50))
        self.btn2.SetBackgroundColour("#FDC68A")
        self.btn2.InitColours()
        self.Bind(wx.EVT_BUTTON, self.on_orientation_button,self.btn2)
        TEXT="3. fill Earth-Ref data using EarthRef Magic-Builder "
        self.btn3 =buttons.GenButton(self.panel, id=-1, label=TEXT,size=(450, 50))
        self.btn3.SetBackgroundColour("#FDC68A")
        self.btn3.InitColours()
        self.Bind(wx.EVT_BUTTON, self.on_er_data,self.btn3)

        TEXT="unpack downloaded txt file "
        self.btn4 =buttons.GenButton(self.panel, id=-1, label=TEXT,size=(300, 50))
        self.btn4.SetBackgroundColour("#FDC68A")
        self.btn4.InitColours()
        self.Bind(wx.EVT_BUTTON, self.on_unpack,self.btn4)
 
        #str = "OR"
        OR = wx.StaticText(self.panel, -1, "or", (20, 120))
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL)
        OR.SetFont(font)
            
                                  
        #bSizer0.Add(self.panel,self.btn1,wx.ALIGN_TOP)
        bSizer1_1 = wx.BoxSizer(wx.VERTICAL)
        bSizer1_1.AddSpacer(20)
        bSizer1_1.Add(self.btn1,wx.ALIGN_TOP)
        bSizer1_1.AddSpacer(20)
        bSizer1_1.Add(self.btn2,wx.ALIGN_TOP)
        bSizer1_1.AddSpacer(20)
        bSizer1_1.Add(self.btn3,wx.ALIGN_TOP)
        bSizer1_1.AddSpacer(20)
                
        bSizer1.Add(bSizer1_1,wx.ALIGN_CENTER,wx.EXPAND)
        bSizer1.AddSpacer(20)
        
        bSizer1.Add(OR, 0, wx.ALIGN_CENTER, 0)
        bSizer1.AddSpacer(20)
        bSizer1.Add(self.btn4, 0, wx.ALIGN_CENTER, 0)
        bSizer1.AddSpacer(20)


        #---sizer 2 ----
        bSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, "Analysis and plots" ), wx.HORIZONTAL )
        
        TEXT="Demag GUI"
        self.btn_demag_gui =buttons.GenButton(self.panel, id=-1, label=TEXT,size=(300, 50))
        self.btn_demag_gui.SetBackgroundColour("#6ECFF6")
        self.btn_demag_gui.InitColours()
        self.Bind(wx.EVT_BUTTON, self.on_run_demag_gui,self.btn_demag_gui)

        TEXT="Thellier GUI"
        self.btn_thellier_gui =buttons.GenButton(self.panel, id=-1, label=TEXT,size=(300, 50))
        self.btn_thellier_gui.SetBackgroundColour("#6ECFF6")
        self.btn_thellier_gui.InitColours()
        self.Bind(wx.EVT_BUTTON, self.on_run_thellier_gui,self.btn_thellier_gui)

        bSizer2.AddSpacer(20)
        bSizer2.Add(self.btn_demag_gui, 0, wx.ALIGN_CENTER, 0)
        bSizer2.AddSpacer(20)
        bSizer2.Add(self.btn_thellier_gui, 0, wx.ALIGN_CENTER, 0)
        bSizer2.AddSpacer(20)
        
        #---sizer 3 ----
        bSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.panel, wx.ID_ANY, "Upload to MagIC database" ), wx.HORIZONTAL )
        
        TEXT="prepare upload txt file"
        self.btn_upload =buttons.GenButton(self.panel, id=-1, label=TEXT,size=(300, 50))
        self.btn_upload.SetBackgroundColour("#C4DF9B")
        self.btn_upload.InitColours()

        bSizer3.AddSpacer(20)
        bSizer3.Add(self.btn_upload, 0, wx.ALIGN_CENTER, 0)
        bSizer3.AddSpacer(20)
        self.Bind(wx.EVT_BUTTON, self.on_btn_upload,self.btn_upload)



        #---arange sizers ----
        
        hbox=wx.BoxSizer(wx.HORIZONTAL)
        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(5)
        #vbox.Add(self.logo,0,wx.ALIGN_CENTER,0)
        vbox.AddSpacer(5)        
        vbox.Add(bSizer0,0,wx.ALIGN_CENTER,0)
        vbox.AddSpacer(10)        
        vbox.Add(bSizer0_1, 0, wx.ALIGN_CENTER, 0)
        vbox.AddSpacer(10)
        vbox.Add(bSizer1,0,wx.ALIGN_CENTER,0)
        vbox.AddSpacer(10)        
        vbox.Add(bSizer2,0,wx.ALIGN_CENTER,0)
        vbox.AddSpacer(10)        
        vbox.Add(bSizer3,0,wx.ALIGN_CENTER,0)
        vbox.AddSpacer(10)        
        #vbox.Add(bSizer1)
        #vbox.AddSpacer(20)        
        #vbox.Add(bSizer2)
        #vbox.AddSpacer(20)  
        hbox.AddSpacer(10)      
        hbox.Add(vbox,0,wx.ALIGN_CENTER,0)
        hbox.AddSpacer(5)      
              
        self.panel.SetSizer(hbox)
        hbox.Fit(self)
        

    #----------------------------------------------------------------------


    def get_DIR(self):
        """ Choose a working directory dialog
        """

        if "-WD" in sys.argv and self.FIRST_RUN:
            ind=sys.argv.index('-WD')
            self.WD=sys.argv[ind+1]            
        
        else:
            self.WD = os.getcwd() + '/'
            
        os.chdir(self.WD)
        self.WD=str(os.getcwd())+"/"
        self.dir_path.SetValue(self.WD)
        self.FIRST_RUN=False


    #----------------------------------------------------------------------
    
    def getFolderBitmap():
        img = folder_icon.GetImage().Rescale(50, 50)
        return img.ConvertToBitmap()   
                 
                  
    def on_change_dir_button(self,event):
        currentDirectory=os.getcwd()
        dialog = wx.DirDialog(None, "choose directory:",defaultPath = currentDirectory ,style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON | wx.DD_CHANGE_DIR)
        if dialog.ShowModal() == wx.ID_OK:
            self.WD=dialog.GetPath()
            os.chdir(self.WD)
            self.dir_path.SetValue(self.WD)
            dialog.Destroy()


    def on_revert_dir_button(self, event):
        print "REVERT!"

    def on_save_dir_button(self, event):
        print "SAVE!"


    def on_run_thellier_gui(self,event):
        outstring="thellier_gui.py -WD %s"%self.WD
        print "-I- running python script:\n %s"%(outstring)
        os.system(outstring)

    def on_run_demag_gui(self,event):
        outstring="demag_gui.py -WD %s"%self.WD
        print "-I- running python script:\n %s"%(outstring)
        os.system(outstring)
        
    def on_convert_file(self,event):
        pmag_dialogs_dia=pmag_basic_dialogs.import_magnetometer_data(self, wx.ID_ANY, '',self.WD)
        pmag_dialogs_dia.Show()
        pmag_dialogs_dia.Center()


    
    def on_er_data(self, event):
        import ErMagicBuilder
        self.ErMagic = ErMagicBuilder.MagIC_model_builder(self.WD, self)#,self.Data,self.Data_hierarchy)
        self.ErMagic.Show()
        self.ErMagic.Center()

        SIZE=wx.DisplaySize()
        SIZE=(SIZE[0]-0.3*SIZE[0],SIZE[1]-0.3*SIZE[1]) # gets total available screen space - 10%
        self.ErMagic.Raise()

    def init_check_window(self):
        import pmag_basic_dialogs
        self.check_dia = pmag_basic_dialogs.check(self, -1, 'Check', self.WD, self.ErMagic)# initiates the object that will control steps 1-6 of checking headers, filling in cell values, etc.


    def get_data(self):
        
      Data={}
      Data_hierarchy={}
      Data_hierarchy['sites']={}
      Data_hierarchy['samples']={}
      Data_hierarchy['specimens']={}
      Data_hierarchy['sample_of_specimen']={} 
      Data_hierarchy['site_of_specimen']={}   
      Data_hierarchy['site_of_sample']={}   
      try:
          meas_data,file_type=pmag.magic_read(self.WD+"/magic_measurements.txt")
      except:
          print "-E- ERROR: Cant read magic_measurement.txt file. File is corrupted."
          return {},{}
         
      sids=pmag.get_specs(meas_data) # samples ID's
      
      for s in sids:
          if s not in Data.keys():
              Data[s]={}
      for rec in meas_data:
          s=rec["er_specimen_name"]
          sample=rec["er_sample_name"]
          site=rec["er_site_name"]
          if sample not in Data_hierarchy['samples'].keys():
              Data_hierarchy['samples'][sample]=[]

          if site not in Data_hierarchy['sites'].keys():
              Data_hierarchy['sites'][site]=[]         
          
          if s not in Data_hierarchy['samples'][sample]:
              Data_hierarchy['samples'][sample].append(s)

          if sample not in Data_hierarchy['sites'][site]:
              Data_hierarchy['sites'][site].append(sample)

          Data_hierarchy['specimens'][s]=sample
          Data_hierarchy['sample_of_specimen'][s]=sample  
          Data_hierarchy['site_of_specimen'][s]=site  
          Data_hierarchy['site_of_sample'][sample]=site
      self.Data = Data
      self.Data_hierarchy = Data_hierarchy
      return(Data,Data_hierarchy)
                                                                                                                                                                                                                               
    def on_orientation_button(self,event):
        #dw, dh = wx.DisplaySize()
        SIZE=wx.DisplaySize()
        SIZE=(SIZE[0]-0.1*SIZE[0],SIZE[1]-0.1*SIZE[1])
        Data,Data_hierarchy=self.get_data()
        frame = pmag_basic_dialogs.OrientFrameGrid (None, -1, 'demag_orient.txt',self.WD,Data_hierarchy,SIZE)        
        frame.Show(True)
        frame.Centre()

    def on_unpack(self,event):  

        dlg = wx.FileDialog(
            None,message="choose txt file to unpack",
            defaultDir=self.WD, 
            defaultFile="",
            style=wx.OPEN #| wx.CHANGE_DIR
            )        
        if dlg.ShowModal() == wx.ID_OK:
            FILE = dlg.GetFilename()                
        outstring="download_magic.py -f %s"%FILE
        print "-I- running python script:\n %s"%(outstring)
        os.system(outstring)
        TXT="Running download_magic.py program. Check terminal (Mac) or command prompt (windows) for error/warnings\n If no errors occur then MagIC files were save in MagIC Prpject Directory"
        dlg = wx.MessageDialog(self, caption="Saved",message=TXT,style=wx.OK)
        result = dlg.ShowModal()
        if result == wx.ID_OK:            
            dlg.Destroy()
        
    def on_btn_upload(self,event):
        outstring="upload_magic.py"
        print "-I- running python script:\n %s"%(outstring)
        os.system(outstring)
        TXT="Check terminal (Mac) or command prompt (windows) for error/warnings.\nA file name upload_dos.txt was generated in MagIC Project Directory.\nDrag and drop this file in the MagIC database."
        dlg = wx.MessageDialog(self, caption="Saved",message=TXT,style=wx.OK)
        result = dlg.ShowModal()
        if result == wx.ID_OK:            
            dlg.Destroy()
        
       
           
    def on_menu_exit(self, event):
        try:
            self.help_window.Destroy()
        except:
            pass
        if '-i' in sys.argv:
            self.Destroy()
        try:
            exit() # can raise TypeError if wx inspector was used
        except Exception as ex:
            if type(ex) == TypeError:  # suppress that TypeError, but raise others
                pass
            else:
                raise(ex)
            


    




if __name__ == "__main__":
    #app = wx.App(redirect=True, filename="beta_log.log")
    app = wx.PySimpleApp()
    app.frame = MagMainFrame()
    app.frame.Show()
    app.frame.Center()
    if '-i' in sys.argv:
        import wx.lib.inspection
        wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
