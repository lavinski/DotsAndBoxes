import tkinter as tk
from tkinter import ttk
import Configurations as cfg


class SelectPlayersPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.general_frame = tk.Frame(self)

        ttk.Label(self.general_frame, text="Select Players", font="GOFont", foreground="#888",
                  justify=tk.CENTER).grid()

        self.select_opponent_frame = tk.Frame(self.general_frame)

        # SELECT opponent 1
        button1 = ttk.Button(self.select_opponent_frame, text="Easy",
                             command=lambda: controller.select_opponent(cfg.EASY))
        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self.select_opponent_frame, text="Medium",
                             command=lambda: controller.select_opponent(cfg.MEDIUM))
        button2.grid(row=2, column=1, padx=10, pady=10)

        button3 = ttk.Button(self.select_opponent_frame, text="Hard",
                             command=lambda: controller.select_opponent(cfg.HARD))
        button3.grid(row=3, column=1, padx=10, pady=10)

        button1 = ttk.Button(self.select_opponent_frame, text="Human",
                             command=lambda: controller.select_opponent(cfg.HUMAN))
        button1.grid(row=4, column=1, padx=10, pady=10)

        # SELECT opponent 2
        button1 = ttk.Button(self.select_opponent_frame, text="Easy",
                             command=lambda: controller.select_opponent2(cfg.EASY))
        button1.grid(row=1, column=3, padx=10, pady=10)

        button2 = ttk.Button(self.select_opponent_frame, text="Medium",
                             command=lambda: controller.select_opponent2(cfg.MEDIUM))
        button2.grid(row=2, column=3, padx=10, pady=10)

        button3 = ttk.Button(self.select_opponent_frame, text="Hard",
                             command=lambda: controller.select_opponent2(cfg.HARD))
        button3.grid(row=3, column=3, padx=10, pady=10)

        button1 = ttk.Button(self.select_opponent_frame, text="Human",
                             command=lambda: controller.select_opponent2(cfg.HUMAN))
        button1.grid(row=4, column=3, padx=10, pady=10)

        # proceed to game
        button1 = ttk.Button(self.select_opponent_frame, text="Play",
                             command=lambda: controller.proceed_to_game())
        button1.grid(row=5, column=2, padx=10, pady=10)

        self.select_opponent_frame.grid()
        self.general_frame.place(x=cfg.GAME_W / 2, y=cfg.GAME_H / 2, anchor="center")
