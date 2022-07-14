""" Custom widgets for Adaptive Rating """

# Import GUI packages
import tkinter as tk
from tkinter import ttk


class ArrowGroup(tk.Frame):
    """ Group of arrow buttons indicating fast/slower 
        and big/small step size
     """
    def __init__(self, parent, button_text, command_args=None, **kwargs):
        super().__init__(parent, **kwargs)
        command_args = command_args or {}
        #button_text = button_text

        # Layout
        options = {'padx': 5, 'pady':5}

        # Style
        style = ttk.Style(self)
        style.configure('Big.TLabel', font=("Helvetica", 14))
        style.configure('Big.TButton', font=("Helvetica", 11))


        # LABELS
        # Faster label
        lbl_faster = ttk.Label(self, text="Faster", style="Big.TLabel")
        lbl_faster.grid(row=0, column=0)

        # Slower label
        lbl_faster = ttk.Label(self, text="Slower", style="Big.TLabel")
        lbl_faster.grid(row=1, column=0)


        # BUTTONS
        # Big step UP
        btn_big_up = ttk.Button(self, takefocus=0, 
            command=command_args["bigup"])
        btn_big_up.image = tk.PhotoImage(file="big_up4.png")
        btn_big_up['image'] = btn_big_up.image
        btn_big_up.grid(row=0, column=1, **options)

        # Small step UP
        btn_big_up = ttk.Button(self, takefocus=0,
            command=command_args["smallup"])
        btn_big_up.image = tk.PhotoImage(file="little_up4.png")
        btn_big_up['image'] = btn_big_up.image
        btn_big_up.grid(row=0, column=2, **options)

        # Big step DOWN
        self.btn_big_up = ttk.Button(self, takefocus=0,
            command=command_args["bigdown"])
        self.btn_big_up.image = tk.PhotoImage(file="big_down4.png")
        self.btn_big_up['image'] = self.btn_big_up.image
        self.btn_big_up.grid(row=1, column=1, **options)

        # Little step DOWN
        self.btn_big_up = ttk.Button(self, takefocus=0,
            command=command_args["smalldown"])
        self.btn_big_up.image = tk.PhotoImage(file="little_down4.png")
        self.btn_big_up['image'] = self.btn_big_up.image
        self.btn_big_up.grid(row=1, column=2, **options)

        # Repeat button
        self.btn_repeat = ttk.Button(self, 
            textvariable=button_text, 
            command=command_args["repeat"],
            style='Big.TButton',
            takefocus=0)
        self.btn_repeat.grid(row=2, column=1, columnspan=2, **options)
