import numpy as np
from Path import Path
from DataBuilder import DataBuilder
import math
import json

class GeneratePath:

    def __init__(self):
        self.db = DataBuilder()

    def GeneratePath(self, search_space):
        initialX = 49
        initialY = 28
        DEPTH = 5

        # print("generating path")

        # for i in range(100):
        #     for j in range(100):
        #         if search_space[i][j][0][0] == 0:
        #             value = search_space[i][j][0][1]
        #             if value > maxInitValue:
        #                 maxInitValue = value
        #                 initialX = i
        #                 initialY = j

        path = Path(30)
        path.set_day_position(0,initialX, initialY, search_space[initialX][initialY][0][1])

        currentX = initialX
        currentY = initialY

        for i in range(1, 30):
            value, currentX, currentY = self.nextMove(search_space, currentX, currentY, i, DEPTH)
            value = search_space[currentX][currentY][i][1]
            print(value, currentX, currentY)
            path.set_day_position(i, currentX, currentY, value)

        return path

    def nextMove(self, search_space, Xposition, Yposition, day, depth):

        if depth == 0:
            return search_space[Xposition][Yposition][day][1], Xposition, Yposition
        
        possibleMoves = self.db.get_possible_moves(Xposition, Yposition)
        maxMove = -math.inf
        maxMoveX = 0
        maxMoveY = 0
        
        for move in possibleMoves:
            total = search_space[move[0]][move[1]][day][1]

            if day < 29:
                value, _ , _ = self.nextMove(search_space, move[0], move[1], day + 1, depth - 1)
                total = total + value

            if total > maxMove:
                maxMove = total
                maxMoveX = move[0]
                maxMoveY = move[1]

        return maxMove, maxMoveX, maxMoveY

if __name__ == "__main__":
    db = DataBuilder()
    search_space = db.search_space
    gp = GeneratePath()
    path = gp.GeneratePath(search_space)
    print(path.path)
    print("Value:" + str(path.get_total_value()))
    json.dump(path.path.tolist(), open('path.json', 'w'))



