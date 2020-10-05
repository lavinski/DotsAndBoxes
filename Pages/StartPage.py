import tkinter as tk
from tkinter import ttk
import Configurations as cfg

from Pages import SelectPlayersPage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.general_frame = tk.Frame(self)

        ttk.Label(self.general_frame, text="Dots & Boxes", font="GOFont", foreground="#888", justify=tk.CENTER).grid()
        ttk.Button(self.general_frame, text="Start", command=lambda: controller.show_frame(SelectPlayersPage.SelectPlayersPage)).grid()

        self.general_frame.place(x=cfg.GAME_W / 2, y=cfg.GAME_H / 2, anchor="center")
