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
        self.DEPTH = 4

    def generatePathFirstRigg(self):
        search_space = self.db.search_space
        #initialize variables
        maxInitValue = -math.inf
        initialX = 0
        initialY = 0

        #find the best initial position for the first rigg
        for i in range(100):
            for j in range(100):
                #check if position is land
                if search_space[i][j][0][0] == 0:
                    value = search_space[i][j][0][1]
                    if value > maxInitValue:
                        maxInitValue = value
                        initialX = i
                        initialY = j

        #set the initial position of the first rigg
        self.firstRiggPath.set_day_position(0,initialX, initialY, search_space[initialX][initialY][0][1])
        print(search_space[initialX][initialY][0][1], initialX, initialY)


        currentX = initialX
        currentY = initialY

        #generate the best path for the first rigg
        for i in range(1, 30):
            value, currentX, currentY = self.nextMoveRig(search_space, currentX, currentY, i, self.DEPTH, True)
            value = search_space[currentX][currentY][i][1]
            print(value, currentX, currentY)
            self.firstRiggPath.set_day_position(i, currentX, currentY, value)

        return self.firstRiggPath

    # The second rigg path is generated with the same method as the first rigg
    # but considers the first rigg path to avoid overlapping through time
    def generatePathSecondRigg(self):
        search_space = self.db.search_space
        #initialize variables
        maxInitValue = -math.inf
        initialX = 0
        initialY = 0

        #find the best initial position for the second rigg
        for i in range(100):
            for j in range(100):
                #check if the position is in the neigbourhood of the first rigg initial position
                if self.db.is_in_neigbourhood_of_first_rigg(i, j, self.firstRiggPath, 0):
                    continue
                #check if position is land
                if search_space[i][j][0][0] == 0:
                    value = search_space[i][j][0][1]
                    if value > maxInitValue:
                        maxInitValue = value
                        initialX = i
                        initialY = j

        #set the initial position of the second rigg
        self.secondRiggPath.set_day_position(0,initialX, initialY, search_space[initialX][initialY][0][1])
        print(search_space[initialX][initialY][0][1], initialX, initialY)

        currentX = initialX
        currentY = initialY

        #generate the best path for the second rigg
        for i in range(1, 30):
            value, currentX, currentY = self.nextMoveRig(search_space, currentX, currentY, i, self.DEPTH, False)
            value = search_space[currentX][currentY][i][1]
            print(value, currentX, currentY)
            self.secondRiggPath.set_day_position(i, currentX, currentY, value)

        return self.secondRiggPath
    

    # This function will return the best next move based on the total value accumulated after all moves
    # It simulates all possible moves up to a certain depth, and computes the total value accumulated for each path
    # This is an implementation of a recursive depth first search at a certain depth
    def nextMoveRig(self, search_space, Xposition, Yposition, day, depth, isFirstRig):
        if depth == 0:
            return search_space[Xposition][Yposition][day][1], Xposition, Yposition
        
        if isFirstRig:
            #if first rig, we take into account all possible moves
            possibleMoves = self.db.get_possible_moves(Xposition, Yposition)
        else:
            #if second rig, we take into account all possible moves except those in the neigbourhood of the first rigg
            possibleMoves = self.db.get_possible_moves(Xposition, Yposition, day, self.firstRiggPath)

        #initialize variables
        maxMove = -math.inf
        maxMoveX = 0
        maxMoveY = 0

        for move in possibleMoves:
            total = search_space[move[0]][move[1]][day][1]

            if day < 29:
                #recursive call to simulate the next move, at next depth
                value, _ , _ = self.nextMoveRig(search_space, move[0], move[1], day + 1, depth - 1, isFirstRig)
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
    



