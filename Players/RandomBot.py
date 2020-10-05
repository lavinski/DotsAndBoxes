import random

from Players.BotInterface import BotInterface


class RandomBot(BotInterface):
    name = "Random Bot"

    dimensions = None

    def __init__(self, in_dimensions=5):
        self.dimensions = in_dimensions

    def makeTheMove(self, all_the_moves):

        # all the moves will come in this format:
        # it will be a list of directories
        # all_the_moves = [
        #     {'point_to_x': 4, 'point_to_y': 1, 'point_from_x': 1, 'point_from_y': 3},
        #     {'point_to_x': 4, 'point_to_y': 1, 'point_from_x': 1, 'point_from_y': 3},
        #     {'point_to_x': 4, 'point_to_y': 1, 'point_from_x': 1, 'point_from_y': 3}
        # ]

        # this bot is returning the random move that has not been made yet

        moves_made = {}
        dimensions = self.dimensions

        total_count_of_moves = dimensions * (dimensions + 1) * 2

        # print(total_count_of_moves)
        # all the moves where made
        if total_count_of_moves <= len(all_the_moves) - 1:
            return None

        # creating hash table for constant lookup in the future
        for move in all_the_moves:
            hash_value = str(move['point_from_x']) + str(move['point_from_y']) + str(move['point_to_x']) + str(
                move['point_to_y'])
            moves_made[hash_value] = 1

        # get a random move
        while True:
            # get a random point in the grid
            random_x = random.randint(0, dimensions + 1)
            random_y = random.randint(0, dimensions + 1)

            # get direction of the line from that point

            random_variable = random.randint(1, 3)

            if random_variable == 1:
                # direction to the north
                random_to_x = random_x
                random_to_y = random_y + 1
            else:
                # direction to the east
                random_to_x = random_x + 1
                random_to_y = random_y

            # checking if the following generated move is valid:
            # 1. is it valid as a move (not off the grid)
            # 2. is it free

            # is the move out of bounds?
            if random_to_y > dimensions or random_to_y < 0 or random_to_x > dimensions or random_to_x < 0:
                # exit the loop
                continue

            # hash value of constant lookup
            hash_value = str(random_x) + str(random_y) + str(random_to_x) + str(random_to_y)
            if hash_value in moves_made:
                # this means that the move is already made
                # print("Yes")
                continue

            hash_value = str(random_to_x) + str(random_to_y) + str(random_x) + str(random_y)
            if hash_value in moves_made:
                # this means that the move is already made
                continue

            # if code passes all the testing this means that the move is valid
            # we can now return it
            break

        # we need to return it as
        move = {
            'point_from_x': random_x,
            'point_from_y': random_y,
            'point_to_x': random_to_x,
            'point_to_y': random_to_y
        }

        return move
