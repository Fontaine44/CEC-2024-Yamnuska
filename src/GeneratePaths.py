import numpy as np
from Path import Path
from DataBuilder import DataBuilder
import math
import json

class GeneratePaths:

    def __init__(self):
        self.db = DataBuilder()
        self.firstRiggPath = Path(30)
        self.secondRiggPath = Path(30)

    def generatePathFirstRigg(self):
        search_space = self.db.search_space
        maxInitValue = -math.inf
        initialX = 49
        initialY = 28
        DEPTH = 5

        for i in range(100):
            for j in range(100):
                if search_space[i][j][0][0] == 0:
                    value = search_space[i][j][0][1]
                    if value > maxInitValue:
                        maxInitValue = value
                        initialX = i
                        initialY = j

        self.firstRiggPath.set_day_position(0,initialX, initialY, search_space[initialX][initialY][0][1])

        currentX = initialX
        currentY = initialY

        for i in range(1, 30):
            value, currentX, currentY = self.nextMoveFirstRigg(search_space, currentX, currentY, i, DEPTH)
            value = search_space[currentX][currentY][i][1]
            print(value, currentX, currentY)
            self.firstRiggPath.set_day_position(i, currentX, currentY, value)

        return self.firstRiggPath

    ## This function will generate the best path based on the best next moves 
    def generatePathSecondRigg(self):
        search_space = self.db.search_space
        maxInitValue = -math.inf
        initialX = 49
        initialY = 28
        DEPTH = 5

        # for i in range(100):
        #     for j in range(100):
        #         if search_space[i][j][0][0] == 0:
        #             value = search_space[i][j][0][1]
        #             if value > maxInitValue:
        #                 maxInitValue = value
        #                 initialX = i
        #                 initialY = j

        self.secondRiggPath.set_day_position(0,initialX, initialY, search_space[initialX][initialY][0][1])

        currentX = initialX
        currentY = initialY

        for i in range(1, 30):
            value, currentX, currentY = self.nextMoveSecondRigg(search_space, currentX, currentY, i, DEPTH)
            value = search_space[currentX][currentY][i][1]
            print(value, currentX, currentY)
            self.secondRiggPath.set_day_position(i, currentX, currentY, value)

        return self.secondRiggPath

    ## This function will return best next move based on the total value after a specific number of days
    def nextMoveFirstRigg(self, search_space, Xposition, Yposition, day, depth):

        if depth == 0:
            return search_space[Xposition][Yposition][day][1], Xposition, Yposition
        
        possibleMoves = self.db.get_possible_moves(Xposition, Yposition)
        maxMove = -math.inf
        maxMoveX = 0
        maxMoveY = 0
        
        for move in possibleMoves:
            total = search_space[move[0]][move[1]][day][1]

            if day < 29:
                value, _ , _ = self.nextMoveFirstRigg(search_space, move[0], move[1], day + 1, depth - 1)
                total = total + value

            if total > maxMove:
                maxMove = total
                maxMoveX = move[0]
                maxMoveY = move[1]

        return maxMove, maxMoveX, maxMoveY
    
    def nextMoveSecondRigg(self, search_space, Xposition, Yposition, day, depth):

        if depth == 0:
            return search_space[Xposition][Yposition][day][1], Xposition, Yposition
        
        possibleMoves = self.db.get_possible_moves(Xposition, Yposition, day, self.firstRiggPath)
        maxMove = -math.inf
        maxMoveX = 0
        maxMoveY = 0
        
        for move in possibleMoves:
            total = search_space[move[0]][move[1]][day][1]

            if day < 29:
                value, _ , _ = self.nextMoveSecondRigg(search_space, move[0], move[1], day + 1, depth - 1)
                total = total + value

            if total > maxMove:
                maxMove = total
                maxMoveX = move[0]
                maxMoveY = move[1]

        return maxMove, maxMoveX, maxMoveY


if __name__ == "__main__":
    gp = GeneratePaths()
    gp.generatePathFirstRigg()
    print("Value First Rigg:" + str(gp.firstRiggPath.get_total_value()))
    gp.generatePathSecondRigg()
    print("Value Second Rigg:" + str(gp.secondRiggPath.get_total_value()))
    json.dump(gp.firstRiggPath.path.tolist(), open('firstRiggPath.json', 'w'))
    json.dump(gp.secondRiggPath.path.tolist(), open('secondRiggPath.json', 'w'))
    



