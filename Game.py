import tkinter as tk
from tkinter import font

import Player
from Pages import StartPage, SelectPlayersPage, GameBoardPage
from Players import AlphaBetaBot, MiniMaxBot, RandomBot, Human
import Configurations as cfg

class Game(tk.Tk):
    opponent = None
    opponent2 = None
    player = None

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}
        self.GO_font = font.Font(self, name="GOFont", family="Times", weight="bold",size=50)

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage.StartPage, SelectPlayersPage.SelectPlayersPage, GameBoardPage.GameBoardPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage.StartPage)

    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def select_opponent(self, opponent):
        if opponent is cfg.EASY:
            self.opponent = RandomBot.RandomBot(cfg.GAME_GRID_SIZE - 1)
        elif opponent is cfg.MEDIUM:
            self.opponent = MiniMaxBot.MiniMaxBot(cfg.GAME_GRID_SIZE - 1)
        elif opponent is cfg.HARD:
            self.opponent = AlphaBetaBot.AlphaBetaBot(cfg.GAME_GRID_SIZE - 1)
        else:
            self.opponent = Human.Human()

    def select_opponent2(self, opponent2):
        if opponent2 is cfg.EASY:
            self.opponent2 = RandomBot.RandomBot(cfg.GAME_GRID_SIZE - 1)
        elif opponent2 is cfg.MEDIUM:
            self.opponent2 = MiniMaxBot.MiniMaxBot(cfg.GAME_GRID_SIZE - 1)
        elif opponent2 is cfg.HARD:
            self.opponent2 = AlphaBetaBot.AlphaBetaBot(cfg.GAME_GRID_SIZE - 1)
        else:
            self.opponent2 = Human.Human()

    def proceed_to_game(self):
        if self.opponent is not None and self.opponent2 is not None:
            self.frames[GameBoardPage.GameBoardPage].update_player_info(Player.Player(self.opponent.name, "blue"), Player.Player(self.opponent2.name, "red"))
            self.show_frame(GameBoardPage.GameBoardPage)
            self.frames[GameBoardPage.GameBoardPage].begin()


app = Game()
app.mainloop()