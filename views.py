""" View for Adaptive Rating """

# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.simpledialog import Dialog

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


#############################
# Session Parameters Dialog #
#############################
class SessionParams(Dialog):
    """ A dialog for setting session parameters """
    def __init__(self, parent, sessionpars, title, error=''):
        self.sessionpars = sessionpars
        self._error = tk.StringVar(value=error)
        super().__init__(parent, title=title)


    def body(self, frame):
        options = {'padx':5, 'pady':5}
        ttk.Label(frame, text="Please Enter Session Parameters").grid(row=0, column=0, columnspan=3, **options)
        if self._error.get():
            ttk.Label(frame, textvariable=self._error).grid(row=1, column=0, **options)

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
        ttk.Label(frame, text="Level:"
            ).grid(row=4, column=0, sticky='e', **options)
        ttk.Entry(frame, width=20, 
            textvariable=self.sessionpars['Presentation Level']
            ).grid(row=4, column=1, sticky='w')

        # Directory
        frm_path = ttk.LabelFrame(frame, text="Please select audio file directory")
        frm_path.grid(row=5, column=0, columnspan=2, **options, ipadx=5, ipady=5)
        my_frame = frame
        ttk.Label(my_frame, text="Path:"
            ).grid(row=5, column=0, sticky='e', **options)
        ttk.Label(my_frame, textvariable=self.sessionpars['Audio Files Path'], 
            borderwidth=2, relief="solid", width=60
            ).grid(row=5, column=1, sticky='w')
        ttk.Button(my_frame, text="Browse", command=self._get_directory
            ).grid(row=6, column=1, sticky='w')


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
