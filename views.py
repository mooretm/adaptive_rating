""" View for Adaptive Rating """

# Import GUI packages
from sre_parse import State
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.simpledialog import Dialog
from turtle import title

# Import data science packages
from pandastable import Table
import numpy as np
import pandas as pd

# Import audio packages
import sounddevice as sd

# Import custom modules
import widgets as w


##########################
# Main Application Frame #
##########################
class MainFrame(ttk.Frame):
    def __init__(self, parent, model, sessionpars, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Initialize
        self.model = model
        self.fields = self.model.fields
        self.sessionpars = sessionpars

        # Data dictionary
        self._vars = {
            'Button ID': tk.StringVar(),
            'Audio Filename': tk.StringVar()
        }


        # Button functions
        def do_big_up():
            """ Send button ID and play event """
            self._vars['Button ID'].set("bigup")
            self.event_generate('<<PlayAudio>>')


        def do_small_up():
            """ Send button ID and play event """
            self._vars['Button ID'].set("smallup")
            self.event_generate('<<PlayAudio>>')


        def do_big_down():
            """ Send button ID and play event """
            self._vars['Button ID'].set("bigdown")
            self.event_generate('<<PlayAudio>>')


        def do_small_down():
            """ Send button ID and play event """
            self._vars['Button ID'].set("smalldown")
            self.event_generate('<<PlayAudio>>')


        # Styles
        # These are global settings
        style = ttk.Style(self)
        style.configure('Big.TLabel', font=("Helvetica", 14))
        style.configure('Big.TLabelframe.Label', font=("Helvetica", 11))
        style.configure('Big.TButton', font=("Helvetica", 11))

        # Arrow frame
        frm_arrows = ttk.LabelFrame(self, text="Presentation Controls")
        frm_arrows.grid(row=1, column=0, padx=15, pady=15)

        # Arrow controls
        self.button_text = tk.StringVar(value="Start")
        w.ArrowGroup(frm_arrows, button_text=self.button_text, 
            command_args = {
                'bigup':do_big_up,
                'smallup':do_small_up,
                'bigdown':do_big_down,
                'smalldown':do_small_down
            },
            repeat_args = {
                'repeat':self._repeat
            }).grid(row=0, column=0)

        # Button frame
        frm_button = ttk.Frame(self)
        frm_button.grid(row=1, column=1)

        # Submit button
        self.btn_submit = ttk.Button(frm_button, text="Submit", 
            command=self._on_submit, style='Big.TButton',
            state="disabled", takefocus=0)
        self.btn_submit.grid(row=0, column=0, padx=(0,15))


    # FUNCTIONS
    def _repeat(self):
        """ Present audio. Can be repeated as many times as 
            the listener wants without incrementing the 
            file list.
        """
        # Send play audio event to app
        self.button_text.set("Repeat")
        self.btn_submit.config(state="enabled")
        self.event_generate('<<RepeatAudio>>')

    
    def _on_submit(self):
        # Send save data event to app
        self.button_text.set("Start")
        self.event_generate('<<SaveRecord>>')


    def get(self):
        """ Retrieve data as dictionary """
        data = dict()
        for key, variable in self._vars.items():
            try:
                data[key] = variable.get()
            except tk.TclError:
                message=f'Error with: {key}.'
                raise ValueError(message)
        return data


    def reset(self):
        """ Clear all values """   
        for var in self._vars.values():
            var.set('')
        # Disable submit button on press
        # Set focus to play button
        self.btn_submit.config(state="disabled")


######################
# Calibration Dialog #
######################
class Calibration(tk.Toplevel):
    def __init__(self, parent, sessionpars, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.sessionpars = sessionpars

        self.withdraw()
        self.focus()
        self.title("Calibration")

        options = {'padx':10, 'pady':10}
        options_small = {'padx':2.5, 'pady':2.5}

        lf_present = ttk.Labelframe(self, text='Presentation Parameters')
        lf_present.grid(column=0, row=0, **options)

        lf_record = ttk.Labelframe(self, text='Save SLM Value')
        lf_record.grid(column=1, row=0, **options)

        # Raw level
        lbl_play = ttk.Label(lf_present, text="Raw Level:").grid(
            column=5, row=5, sticky='e', **options_small)
        ent_slm = ttk.Entry(lf_present, textvariable=self.sessionpars['Raw Level'],
            width=6)
        ent_slm.grid(column=10, row=5, sticky='w', **options_small)
 
        # Play calibration stimulus
        lbl_play = ttk.Label(lf_present, text="Calibration Stimulus:").grid(
            column=5, row=10, sticky='e', **options_small)
        btn_play = ttk.Button(lf_present, text="Play", command=self._on_play)
        btn_play.grid(column=10, row=10, sticky='w', **options_small)
        btn_play.focus()

        # SLM Reading 
        lbl_slm = ttk.Label(lf_record, text="SLM Reading (dB):").grid(
            column=5, row=15, sticky='e', **options_small)
        self.ent_slm = ttk.Entry(lf_record, textvariable=self.sessionpars['SLM Reading'],
            width=6, state='disabled')
        self.ent_slm.grid(column=10, row=15, sticky='w', **options_small)

        # Submit button
        self.btn_submit = ttk.Button(lf_record, text="Submit", 
            command=self._on_submit, state='disabled')
        self.btn_submit.grid(column=5, columnspan=10, row=20, **options_small)

        # Center calibration window dialog
        self.center_window()


    def center_window(self):
        # Center window based on new size
        self.update_idletasks()
        #root.attributes('-topmost',1)
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(False, False)
        self.deiconify()


    def _on_play(self):
        self.parent.event_generate('<<PlayCalibration>>')
        self.btn_submit.config(state='enabled')
        self.ent_slm.config(state='enabled')


    def _on_submit(self):
        print("View_195: Sending save calibration event...")
        self.parent.event_generate('<<CalibrationSubmit>>')
        self.destroy()


###########################
# Audio Parameters Dialog #
###########################
class AudioParams(tk.Toplevel):
    #def __init__(self, parent, sessionpars, title, error=''):
    def __init__(self, parent, sessionpars, *args, **kwargs):
        super().__init__(parent, *args, *kwargs)
        self.parent = parent
        self.sessionpars = sessionpars

        self.withdraw()
        self.focus()
        self.title("Audio Settings")
        #self.grab_set() # Disable root window (toplevel as modal window)

        options = {'padx':10, 'pady':10}
        options_small = {'padx':2.5, 'pady':2.5}

        #frmID = ttk.Frame(self)
        #frmID.grid(column=0, row=0, **options)

        lblfrm_settings = ttk.Labelframe(self, text='Audio Settings')
        lblfrm_settings.grid(column=0, row=0, sticky='nsew', **options)
        lblfrm_settings.columnconfigure([0,1,2,3,4,5], weight=1)

        frmTable = ttk.Frame(self)
        frmTable.grid(column=0, row=15, **options)

        # Speaker number
        lbl_speaker = ttk.Label(lblfrm_settings, text='Output Speaker(s):').grid(
            column=0, row=5, sticky='e', **options_small)
        ent_speaker = ttk.Entry(lblfrm_settings, 
            textvariable=self.sessionpars['Speaker Number'], width=6)
        ent_speaker.grid(column=1, row=5, sticky='w', **options_small)

        # Level
        lbl_level = ttk.Label(lblfrm_settings, text='Raw Level:').grid(
            column=2, row=5, sticky='e', **options_small)
        ent_speaker = ttk.Entry(lblfrm_settings, 
            textvariable=self.sessionpars['Raw Level'], width=6)
        ent_speaker.grid(column=3, row=5, sticky='w', **options_small)

        # Audio device ID
        lbl_device = ttk.Label(lblfrm_settings, text="Audio Device ID:").grid(
            column=4, row=5, sticky='e', **options_small)
        ent_deviceID = ttk.Entry(lblfrm_settings, 
            textvariable=self.sessionpars['Audio Device ID'], width=6)
        ent_deviceID.grid(column=5, row=5, sticky='w', **options_small)

        # Submit button
        btnDeviceID = ttk.Button(self, text="Submit", 
            command=self._on_submit)
        btnDeviceID.grid(column=0, columnspan=10, row=10, **options_small)

        # Get list of audio devices
        deviceList = sd.query_devices()
        names = [deviceList[x]['name'] for x in np.arange(0,len(deviceList))]
        chans_out =  [deviceList[x]['max_output_channels'] for x in np.arange(0,len(deviceList))]
        ids = np.arange(0,len(deviceList))
        df = pd.DataFrame({
            "device_id": ids, 
            "name": names, 
            "chans_out": chans_out})
        #df = df[df['chans_out'] > 0]

        pt = Table(frmTable, dataframe=df, showtoolbar=True, showstatusbar=True)
        table = pt = Table(frmTable, dataframe=df)
        table.grid(column=0, row=0)
        pt.show()

        # Center window based on new size
        self.update_idletasks()
        #root.attributes('-topmost',1)
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(False, False)
        self.deiconify()


    def _on_submit(self):
        print("View_194: Sending save audio config event...")
        self.parent.event_generate('<<AudioParsSubmit>>')
        self.destroy()


#############################
# Session Parameters Dialog #
#############################
class SessionParams(Dialog):
    """ A dialog for setting session parameters """
    def __init__(self, parent, sessionpars, title, error=''):
        self.sessionpars = sessionpars
        self._error = tk.StringVar(value=error)
        super().__init__(parent, title=title)


    def body(self, main_frame):
        options = {'padx':5, 'pady':5}

        if self._error.get():
            ttk.Label(main_frame, textvariable=self._error).grid(row=1, column=0, **options)

        #ttk.Label(frame, text="Please Enter Session Parameters").grid(row=0, column=0, columnspan=3, **options)
        frame = ttk.Labelframe(main_frame, text='Session Information')
        frame.grid()

        # Subject
        ttk.Label(frame, text="Subject:"
            ).grid(row=2, column=0, sticky='e', **options)
        ttk.Entry(frame, width=20, 
            textvariable=self.sessionpars['Subject']
            ).grid(row=2, column=1, sticky='w')
        
        # Condition
        ttk.Label(frame, text="Condition:"
            ).grid(row=3, column=0, sticky='e', **options)
        ttk.Entry(frame, width=20, 
            textvariable=self.sessionpars['Condition']
            ).grid(row=3, column=1, sticky='w')

        # Level
        ttk.Label(frame, text="Presentation Level (dB):"
            ).grid(row=4, column=0, sticky='e', **options)
        ttk.Entry(frame, width=20, 
            textvariable=self.sessionpars['Presentation Level']
            ).grid(row=4, column=1, sticky='w')

        # Directory
        frm_path = ttk.LabelFrame(frame, text="Please select audio file directory")
        frm_path.grid(row=5, column=0, columnspan=2, **options, ipadx=5, ipady=5)
        my_frame = frame
        ttk.Label(my_frame, text="Audio File Path:"
            ).grid(row=5, column=0, sticky='e', **options)
        ttk.Label(my_frame, textvariable=self.sessionpars['Audio Files Path'], 
            borderwidth=2, relief="solid", width=60
            ).grid(row=5, column=1, sticky='w')
        ttk.Button(my_frame, text="Browse", command=self._get_directory
            ).grid(row=6, column=1, sticky='w', pady=(0, 5))


    def _get_directory(self):
        # Ask user to specify audio files directory
        self.sessionpars['Audio Files Path'].set(filedialog.askdirectory())


    def ok(self):
        print("View:184: Sending save event...")
        self.parent.event_generate('<<ParsDialogOk>>')
        self.destroy()

    
    def cancel(self):
        print("View:190: Sending load event...")
        self.parent.event_generate('<<ParsDialogCancel>>')
        self.destroy()
