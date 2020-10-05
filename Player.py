from tkinter import *


class Player(object):
    def __init__(self, name, color="black"):
        self.score = 0
        self.str = StringVar()
        self.name = name
        self.color = color

    def update(self):
        self.str.set(self.name + ": %d" % self.score)
