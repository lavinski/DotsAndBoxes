import time
import random

from Players.BotInterface import BotInterface


class MiniMaxBot(BotInterface):
    name = "MiniMax"

    infinity = float('inf')
    dimensions = None;
    HUMAN = -1
    COMP = +1

    def __init__(self, dimensions):
        # lets create a grid to work with
        self.dimensions = dimensions

    def getFreeLines(self, movesMade):
        # will store all the lines in dictionary
        # as a key I will use str representation of the vector cords
        # latter when forming unused lines we will check if the value exist
        usedLines = {}
        for move in movesMade:
            key = move["point_from_x"] * 1000 + move["point_from_y"] * 100 + move["point_to_x"] * 10 + move[
                "point_to_y"]

            usedLines[key] = 1

        allLines = []

        # first lest do it for horizontal lines
        for y in range(0, self.dimensions + 1):
            for x in range(0, self.dimensions):
                # key = x_from + y_from + x_to + y_to
                # because it is horizontal vector just x changes
                key = x * 1000 + y * 100 + (x + 1) * 10 + y

                # lets check if the line is not used
                # who means who filled the box
                if key not in usedLines:
                    appending_move = {
                        'point_from_x': x,
                        'point_from_y': y,
                        'point_to_x': x + 1,
                        'point_to_y': y,
                        'who': 0
                    }

                    allLines.append(appending_move)

        # now lest do it for vertical lines
        for y in range(0, self.dimensions):
            for x in range(0, self.dimensions + 1):
                # key = x_from + y_from + x_to + y_to
                # because it is vertical vector just y changes
                key = x * 1000 + y * 100 + x * 10 + (y + 1)

                # lets check if the line is not used
                # who means who filled the box
                if key not in usedLines:
                    appending_move = {
                        'point_from_x': x,
                        'point_from_y': y,
                        'point_to_x': x,
                        'point_to_y': y + 1,
                        'who': 0
                    }

                    allLines.append(appending_move)

        # lets return free lines
        return allLines

    def makeTheMove(self, movesMade):
        aRange = range(0, self.dimensions)

        freeLines = self.getFreeLines(movesMade)

        # testing
        for free in freeLines:
            if free["point_from_x"] == 0 and free["point_from_y"] == 0 and free["point_to_x"] == 1 and free[
                "point_to_y"] == 0:
                break;

        # how much moves you can take before the end
        depth = len(freeLines)
        totalMoves = ((self.dimensions + 1) * self.dimensions) * 2
        if depth == 0:
            return None

        whenToStop = depth - (totalMoves // depth) - 2
        whenToStop = depth - 2

        while depth - whenToStop > 4:
            whenToStop += 1

        # program will not pass who made the move so it will be set to 0
        # for unknown state
        # latter on this will be used to count score
        movesMadeNew = []
        for moves in movesMade:
            moves["who"] = 0
            movesMadeNew.append(moves)

        # computer always starts first so player is 1
        move = self.minimax(movesMadeNew, depth, 1, whenToStop, 0, 0, time.time())
        bestmove = move[0]
        score = move[1]

        # lets remove who key from move and return it

        if score == 0:
            # print("generate random")
            # this means that all moves are equal value
            # so we need to make random move
            freeMoves = self.getFreeLines(movesMadeNew)
            randomMoveId = random.randint(0, len(freeMoves) - 1)
            bestmove = freeMoves[randomMoveId]

        bestmove.pop('who', None)
        return bestmove

    def minimax(self, state, depth, player, whenToStop, opponent1_score_before, opponent2_score_before, startTime):
        if player == 1:
            best = [-1, -self.infinity]
        else:
            best = [-1, +self.infinity]

        # if it is the end we need to exit the recursion
        if depth == whenToStop or depth == 0:
            # this is not working
            return [-1, opponent1_score_before - opponent2_score_before]

        for move in self.getFreeLines(state):
            move["who"] = player

            state.append(move)
            opponent1_score, opponent2_score = self.evaluate(state)

            if opponent1_score == 0 and opponent2_score == 0:
                nextturn = -1 * player
                # print("Equal")
            else:
                # print("Not Equal")
                nextturn = player

            # print("Next will play:" + str(nextturn))
            # print("----------------------")
            # print(depth)
            score = self.minimax(state, depth - 1, nextturn, whenToStop, opponent1_score, opponent2_score, startTime)

            state.pop()
            score[0] = move

            # if player is computer
            if player == 1:
                if score[1] > best[1]:
                    best = score  # max value
            else:
                if score[1] < best[1]:
                    best = score  # min value

        return best

    def evaluate(self, state):
        dimensions = 5

        # each box will has its own unique id based on the bottom left corner cords
        # so the first box will have 00
        # it will work as hash function and will help to save time

        box_dic = {}

        for y in range(0, dimensions):
            for x in range(0, dimensions):
                key = x * 10 + y
                # each box has 4 walls
                box_dic[key] = 4

        opponent1_score = 0
        opponent2_score = 0

        # check for score

        for move in state:
            # each move can have inpact on 2 boxes
            # horizontal on top and bottom
            # and vertical on left and right

            # checking if it is horizontal or vertical line
            keys = []
            if move["point_from_x"] == move["point_to_x"]:
                # its vertical

                # because box id is made of bottom left corners cords
                # program needs to now which point to smaller and the cords
                # of that point will be box id on the right

                box_x = move["point_from_x"]
                box_y = min(move["point_from_y"], move["point_to_y"])

                keys.append(box_x * 10 + box_y)
                # we need to do the same thing for the box on the left
                keys.append((box_x - 1) * 10 + box_y)

            else:
                # its horizontal
                box_x = min(move["point_from_x"], move["point_to_x"])
                box_y = move["point_from_y"]

                keys.append(box_x * 10 + box_y)
                # we need to do the same thing for the box on the left
                keys.append(box_x * 10 + (box_y - 1))

            for key in keys:
                if key in box_dic:
                    # box can not exist if the values are on the sides of the grid
                    box_dic[key] -= 1
                    if box_dic[key] == 0:
                        # the box has been filled
                        if move["who"] == 1:
                            opponent1_score += 1
                        elif move["who"] == -1:
                            opponent2_score += 1

        return opponent1_score, opponent2_score
