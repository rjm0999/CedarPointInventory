import tkinter as tk
import math
import pandas as pd
from datetime import date, datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from constants import *

# google account info username: CedarPointInventory
#                     password: CedarPoint2022
#                     birthday: 1 January 1902


class Gui(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.destroy_children()

    def destroy_children(self):
        """
        Retrieve the parent of this widget and call the destroy method on all children of the parent, excluding itself
        """
        for i in self.parent.winfo_children():
            if i is not self:
                i.destroy()

    def configure_parent(self):
        """
        Call the clear_grid method on the parent object of this widget. Acts as default configure_parent for all
        classes that inherit from this one
        """
        self.parent.clear_grid()

    def frame_buttons(self):
        """
        Create two buttons, one that closes the program and one that returns to the main menu, and pack them into a
        frame

        Returns
        -------
        Frm : tkinter.Frame
            Frame containing the "Main Menu" and "Quit" buttons
        """
        frm = tk.Frame(self.parent)

        back_button = tk.Button(frm, text="Main Menu", command=self.parent.main_gui, font=(FONT, 25))
        back_button.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=50, pady=50)
        back_button.config(width=1)

        quit_button = tk.Button(frm, text="Quit", command=self.quit, font=(FONT, 25))
        quit_button.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT, padx=50, pady=50)
        quit_button.config(width=1)

        return frm
