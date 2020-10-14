import time
import tkinter as tk
import Player
import Configurations as cfg
from Players.Human import Human
from Pages.SelectPlayersPage import SelectPlayersPage


class GameBoardPage(tk.Frame):
    moves = []
    controller = None

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.start_game()

    def start_game(self):
        self.canvas = tk.Canvas(self, height=cfg.GAME_H, width=cfg.GAME_W)

        self.players = [
            Player.Player("Human", "red")
        ]

        self.canvas.grid(row=0, column=0)

        self.canvas.bind("<Key>", lambda e: self.keyPress(e))

        self.dots = [[self.canvas.create_oval(cfg.CELLSIZE * i + cfg.OFFSET,
                                              cfg.CELLSIZE * j + cfg.OFFSET,
                                              cfg.CELLSIZE * i + cfg.OFFSET + 2 * cfg.CIRCLERAD,
                                              cfg.CELLSIZE * j + cfg.OFFSET + 2 * cfg.CIRCLERAD,
                                              fill="black") \
                      for j in range(cfg.GAME_GRID_SIZE)] for i in range(cfg.GAME_GRID_SIZE)]

        self.lines = []
        self.infoframe = tk.Frame(self)

    def keyPress(self, e):
        # print("reset")
        if e.char == 'r':
            self.reset()
        elif e.char == 'b':
            self.reset()
            self.controller.show_frame(SelectPlayersPage)

    def reset(self):
        players = self.players
        self.moves = []
        self.start_game()
        if len(players) == 2:
            self.update_player_info(Player.Player(players[0].name, players[0].color),
                                    Player.Player(players[1].name, players[1].color))

    def begin(self):
        self.canvas.update_idletasks()

        self.canvas.focus_set()

        if isinstance(self.controller.opponent,Human):
            self.canvas.bind("<Button-1>", lambda e: self.click(e))
        else:
            if isinstance(self.controller.opponent2, Human):
                self.canvas.bind("<Button-1>", lambda e: self.click(e))
            self.canvas.bind("<space>", lambda e: self.first_move())

    def first_move(self):
        if len(self.moves)==0:
            self.update_current_player(0)

    def update_players(self):
        for i in self.players:
            i.update()

    def click(self, event):
        x, y = event.x, event.y
        # print("Human made {} {}".format(x, y))
        self.check_the_move(x, y)

    def update_player_info(self, player1, player2):
        self.players = [
            player1, player2
        ]
        # create labels for players
        for widget in self.infoframe.winfo_children():
            widget.destroy()

        self.infoframe.destroy()

        self.infoframe = tk.Frame(self)

        self.infoframe.players = [
            tk.Label(self.infoframe, textvariable=i.str,fg=i.color) for i in self.players
        ]

        self.infoframe.grid_forget()
        for i in self.infoframe.players:
            i.grid()

        self.current_player = self.players[0]
        self.update_players()
        self.infoframe.grid(row=0, column=1, sticky='n')
        self.grid()

    def bot_click(self, move):
        if self.check_game_over():
            return

        if move == None:
            self.check_game_over()
            return

        x = int(((move['point_to_x'] + move['point_from_x']) / 2 * cfg.CELLSIZE) + cfg.OFFSET)
        y = int(((move['point_to_y'] + move['point_from_y']) / 2 * cfg.CELLSIZE) + cfg.OFFSET)

        oriantation = self.isclose(x, y)
        if oriantation:
            if self.line_exists(x, y, oriantation):
                # print("line exist")
                # move = self.controller.opponent.makeTheMove(self.moves)
                # self.bot_click(move)
                return

        self.check_the_move(x, y)

    def check_the_move(self, x, y):
        oriantation = self.isclose(x, y)
        if oriantation:
            if self.line_exists(x, y, oriantation):
                #print("line does not exist")
                return

            # print(x)
            # print("y", y)
            # print("oriantation", oriantation)

            index = self.players.index(self.current_player)

            l = self.create_line(x, y, oriantation, self.players[index].color)
            score = self.new_box_made(l)

            if score:
                self.current_player.score += score
                self.current_player.update()
                self.check_game_over()

            else:
                index = self.players.index(self.current_player)
                index = 1 - index

            self.lines.append(l)
            self.canvas.update_idletasks()
            self.update_current_player(index)

    def update_current_player(self, index):
        self.current_player = self.players[index]
        time.sleep(0.1)

        if index == 0 and self.controller.opponent is not None:
            move = self.controller.opponent.makeTheMove(self.moves)
            self.bot_click(move)

        if index == 1 and self.controller.opponent2 is not None:
            move = self.controller.opponent2.makeTheMove(self.moves)
            self.bot_click(move)

    def create_line(self, x, y, orient, color):
        startx = cfg.CELLSIZE * ((x - cfg.OFFSET) // cfg.CELLSIZE) + cfg.DOTOFFSET
        starty = cfg.CELLSIZE * ((y - cfg.OFFSET) // cfg.CELLSIZE) + cfg.DOTOFFSET
        tmpx = (x - cfg.OFFSET) // cfg.CELLSIZE
        tmpy = (y - cfg.OFFSET) // cfg.CELLSIZE

        if orient == tk.HORIZONTAL:
            endx = startx + cfg.CELLSIZE
            endy = starty
        else:
            endx = startx
            endy = starty + cfg.CELLSIZE

        # normalized_x = startx // cfg.CELLSIZE
        # normalized_y = starty // cfg.CELLSIZE
        # normalized_x2 = endx // cfg.CELLSIZE
        # normalized_y2 = endy // cfg.CELLSIZE

        self.moves.append({
            "point_from_x": startx // cfg.CELLSIZE,
            "point_from_y": starty // cfg.CELLSIZE,
            "point_to_x": endx // cfg.CELLSIZE,
            "point_to_y": endy // cfg.CELLSIZE,
        })

        # print("line drawn: %d,%d to %d,%d" % (normalized_x, normalized_y, normalized_x2, normalized_y2))
        # print "line drawn: %d,%d to %d,%d" % (startx,starty,endx,endy)
        return self.canvas.create_line(startx, starty, endx, endy, fill=color)

    def new_box_made(self, line):
        score = 0
        x0, y0, x1, y1 = self.canvas.coords(line)
        if x0 == x1:  # vertical line
            midx = x0
            midy = (y0 + y1) / 2
            pre = (x0 - cfg.CELLSIZE / 2, midy)
            post = (x0 + cfg.CELLSIZE / 2, midy)
        elif y0 == y1:  # horizontal line
            midx = (x0 + x1) / 2
            midy = y0
            pre = (midx, y0 - cfg.CELLSIZE / 2)
            post = (midx, y0 + cfg.CELLSIZE / 2)

        if len(self.find_lines(pre)) == 3:  # not 4, because newly created line is
            self.fill_in(pre)  # is not returned (?!)
            score += 1
        if len(self.find_lines(post)) == 3:
            self.fill_in(post)
            score += 1
        return score

    def find_lines(self, coords):
        x, y = coords
        if x < 0 or x > cfg.GAME_W:
            return []
        if y < 0 or y > cfg.GAME_W:
            return []
        # print "Cell center: %d,%d" % (x,y)
        lines = [x for x in self.canvas.find_enclosed(x - cfg.CELLSIZE, \
                                                      y - cfg.CELLSIZE, \
                                                      x + cfg.CELLSIZE, \
                                                      y + cfg.CELLSIZE) \
                 if x in self.lines]
        # print lines
        return lines

    def fill_in(self, coords):
        x, y = coords
        self.canvas.create_text(x, y, text=self.current_player.name, fill=self.current_player.color)

    def isclose(self, x, y):
        x -= cfg.OFFSET
        y -= cfg.OFFSET
        dx = x - (x // cfg.CELLSIZE) * cfg.CELLSIZE
        dy = y - (y // cfg.CELLSIZE) * cfg.CELLSIZE

        if abs(dx) < cfg.TOL:
            if abs(dy) < cfg.TOL:
                return None  # mouse in corner of box; ignore
            else:
                return tk.VERTICAL
        elif abs(dy) < cfg.TOL:
            return tk.HORIZONTAL
        else:
            return None

    def line_exists(self, x, y, orient):
        id_ = self.canvas.find_closest(x, y, halo=cfg.TOL)[0]
        if id_ in self.lines:
            return True
        else:
            return False

    def check_game_over(self):
        total = sum([x.score for x in self.players])
        if total == (cfg.GAME_GRID_SIZE - 1) * (cfg.GAME_GRID_SIZE - 1):
            self.canvas.create_text(cfg.GAME_W / 2, cfg.GAME_H / 2, text="GAME OVER", font="GOFont", fill="#888")
            return True
        return False