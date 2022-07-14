""" Adaptive Rating:
    Wav-file-based adaptive rating task. Arrow buttons 
    allow for large and small step sizes of the 
    parameter under investigation. Data are saved as 
    .csv files.

    Written by: Travis M. Moore
    Created: Jul 11, 2022
"""

# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Import data science packages
import numpy as np
import pandas as pd
import random

# Import custom modules
import views as v
import models as m
from mainmenu import MainMenu


class Application(tk.Tk):
    """ Application root window """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.withdraw()
        self.title("Adaptive Rating Tool")

        # Not really using this here
        self.settings_model = m.SettingsModel()
        self._load_settings()

        # Load current session parameters (or defaults)
        self.sessionpars_model = m.SessionParsModel()
        self._load_sessionpars()

        # Set up file tracker counter
        # Set this here before loading the model
        # or counter is overriden to 0!
        self.counter = 0

        # Make audio files list model
        self._audio_list = pd.DataFrame()
        self.audio_data = pd.DataFrame()
        #self.audiolist_model = m.AudioList(self.sessionpars)
        self._load_audiolist_model()

        # Initialize objects
        self.model = m.CSVModel(self.sessionpars)
        self.main_frame = v.MainFrame(self, self.model, self.settings, self.sessionpars)
        self.main_frame.grid(row=1, column=0)
        self.main_frame.bind('<<SaveRecord>>', self._on_submit)
        self.main_frame.bind('<<RepeatAudio>>', self.present_audio)
        self.main_frame.bind('<<PlayAudio>>', self._get_audio)

        # Menu
        menu = MainMenu(self, self.settings, self.sessionpars)
        self.config(menu=menu)
        # Create callback dictionary
        event_callbacks = {
            '<<FileSession>>': lambda _: self._show_sessionpars(),
            '<<FileQuit>>': lambda _: self.quit(),
            '<<ParsDialogOk>>': lambda _: self._save_sessionpars(),
            '<<ParsDialogCancel>>': lambda _: self._load_sessionpars()
        }
        # Bind callbacks to sequences
        for sequence, callback in event_callbacks.items():
            self.bind(sequence, callback)

        # Status label to display trial count
        self.status = tk.StringVar(value="Trials Completed: 0")
        ttk.Label(self, textvariable=self.status).grid(sticky='w', padx=15, pady=(0,5))
        # Track trial number
        self._records_saved = 0

        # Set up root window
        self.deiconify()

        self.center_window()


    def center_window(toplevel):
        """ Center the root window """
        toplevel.update_idletasks()
        screen_width = toplevel.winfo_screenwidth()
        screen_height = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        toplevel.geometry("+%d+%d" % (x, y)) 


    def _show_sessionpars(self):
        """ Show the session parameters dialog """
        print("App_93: Calling sessionpars dialog...")
        v.SessionParams(self, sessionpars=self.sessionpars, title="Parameters", error='')


    def _load_sessionpars(self):
        """ Load parameters into self.sessionpars dict """
        vartypes = {
        'bool': tk.BooleanVar,
        'str': tk.StringVar,
        'int': tk.IntVar,
        'float': tk.DoubleVar
        }

        # Create dict of settings variables from the model's settings.
        self.sessionpars = dict()
        for key, data in self.sessionpars_model.fields.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.sessionpars[key] = vartype(value=data['value'])
        print("App_120: Loaded sessionpars model fields into running sessionpars dict")


    def _save_sessionpars(self, *_):
        """ Save the current settings to a preferences file """
        print("App_125: Calling sessionpar model set vars and save functions")
        for key, variable in self.sessionpars.items():
            self.sessionpars_model.set(key, variable.get())
            self.sessionpars_model.save()


    def _load_audiolist_model(self):
        self.audiolist_model = m.AudioList(self.sessionpars)
        #self._audio_list = self.audiolist_model.fields
        try:
            self.df_audio_data = self.audiolist_model.audio_data
        except:
            print("App_139: Problem creating list of audio files...")
            return
        #if len(self._audio_list) > 0:
        if len(self.df_audio_data.index) > 0:
            print("App_143: Loaded audio files from AudioList model into runtime environment")
            self.counter = random.choice(np.arange(0,len(self.df_audio_data.index)-1))
            print(f"App_145: Starting record number: {self.counter}") # Add record name here!!!!
        else:
            print("App_147: No audio files in list!")
            messagebox.showwarning(
                title="No path selected",
                message="Please use File>Session to selected a valid audio file directory!"
            )


    def _get_audio(self, *_):
        """ Increment counter, pull audio file, present audio """
        # Get what button was pressed
        data = self.main_frame.get()
        if data['Button ID'] == "bigup":
            self.counter -= 4
        elif data['Button ID'] == "smallup":
            self.counter -= 1
        elif data['Button ID'] == "bigdown":
            self.counter += 4
        elif data['Button ID'] == "smalldown":
            self.counter += 1

        # Make sure counter stays within bounds
        df_len = int(len(self.df_audio_data.index)-1)
        if self.counter >= df_len:
            self.counter = df_len
        elif self.counter <= 0:
            self.counter = 0

        # Present audio
        self.present_audio()


    def present_audio(self, *_):
        # Present audio
        print(f"App_175: Playing record #: {self.counter}")
        filename = self.df_audio_data["Audio List"].iloc[self.counter]
        print(f"App_177: Record name: {filename}")
        # Audio object expects a full file path and a presentation level
        audio_obj = m.Audio(filename, self.sessionpars['Presentation Level'].get())
        audio_obj.play()
        

    def _on_submit(self, *_):
        """ Save trial ratings, update trial counter,
            and reset sliders.
         """
        # Get _vars from main_frame view
        data = self.main_frame.get()



        ###########################################
        # For tomorrow:
        # Need to get file name from self.audiodata



        # Update _vars with current audio file name
        data["Audio Filename"] = self._audio_list[self._records_saved]
        # Pass data dict to CSVModel for saving
        self.model.save_record(data)
        self._records_saved += 1
        self.status.set(f"Trials Completed: {self._records_saved}")
        self.main_frame.reset()


    def _quit(self):
        """ Exit the program """
        self.destroy()






    def _load_settings(self):
        """Load settings into our self.settings dict."""

        vartypes = {
        'bool': tk.BooleanVar,
        'str': tk.StringVar,
        'int': tk.IntVar,
        'float': tk.DoubleVar
        }

        # Create dict of settings variables from the model's settings.
        self.settings = dict()
        for key, data in self.settings_model.fields.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.settings[key] = vartype(value=data['value'])

        # Put a trace on the variables so they get stored when changed.
        for var in self.settings.values():
            var.trace_add('write', self._save_settings)


    def _save_settings(self, *_):
        """ Save the current settings to a preferences file """
        for key, variable in self.settings.items():
            self.settings_model.set(key, variable.get())
            self.settings_model.save()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
