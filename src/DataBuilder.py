import csv
import numpy as np
import json
import math

# Data source
ALGA_DATASET = '../data/algal_data_day_'
CORAL_DATASET = '../data/coral_data_day_'
HELIUM_DATASET = '../data/helium_data_day_'
METAL_DATASET = '../data/metal_data_day_'
OIL_DATASET = '../data/oil_data_day_'
SHIP_DATASET = '../data/ship_data_day_'
SPECIES_DATASET = '../data/species_data_day_'
TEMP_DATASET = '../data/temperature_data_day_'
WIND_DATASET = '../data/wind_data_day_'
WORLD_ARRAY_DATASET = '../data/world_array_data_day_'

class DataBuilder:
    def __init__(self):
        self.alga_array = None
        self.coral_array = None
        self.helium_array = None
        self.metal_array = None
        self.oil_array = None
        self.ship_array = None
        self.species_array = None
        self.temp_array = None
        self.wind_array = None
        self.world_array = None #0 is land, 1 is water

        self.search_space = None

        self.generate_arrays()
        self.search_space = self.get_search_space()

    def get_possible_moves(self, x, y, numberOfMoves=5):
        if numberOfMoves == 0:
            return 0
        if x < 0 or x > 99 or y < 0 or y > 99:
            return 0
        if self.world_array[x][y][0] == 1:
            return []
        possible_moves = [(x,y)]
        self.next_move(x, y, 0, possible_moves)
        return possible_moves

    #helper function to get all possible moves
    #recursively move by one step, until we reach the maximum number of moves
    #continue if we hit an obstacle
    def next_move(self, x, y, moveNb, moves, visited=[]):
        if moveNb == 5: #max number of moves
            return
        for i in range(-1, 2):
            newX = x + i
            if newX < 0 or newX > 99:
                continue
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                newY = y + j
                if newY < 0 or newY > 99:
                    continue
                if self.world_array[newX][newY][0] == 1:
                    continue
                if (newX, newY) not in moves:
                    moves.append((newX, newY))
                if (newX, newY, moveNb) not in visited:
                    visited.append((newX, newY, moveNb))
                    self.next_move(newX, newY, moveNb + 1, moves, visited)

    #get evaluated value at a certain point on a given day
    #to maximize, we add all the resources on a map, and substract the preserveration resource
    #this gives a set value used to evaluate a certain coordinate for our search
    def get_search_value_at(self, x, y, z):
        if x < 0 or x > 99 or y < 0 or y > 99 or z < 0 or z > 29:
            return 0
        value = 0
        for array in self.OBTAIN:
            value += array[x][y][z]
        for array in self.PRESERVE:
            value -= 4*array[x][y][z]
        return value
    
    def isLand(self, x, y):
        return self.world_array[x][y][0] == 0

    def get_search_space(self):
        search_array = np.zeros((100, 100, 30, 3))
        for i in range(100):
            for j in range(100):
                for k in range(30):
                    isLand = self.world_array[i][j][k]
                    value = self.get_search_value_at(i, j, k)
                    search_array[i][j][k][0] = isLand
                    search_array[i][j][k][1] = value

        # normalize between 0 and 1
        slice_of_interest = search_array[..., 1]

        # Compute min and max values of this slice
        min_val = np.min(slice_of_interest)
        max_val = np.max(slice_of_interest)

        # Normalize the slice
        normalized_slice = (slice_of_interest - min_val) / (max_val - min_val)

        # Assign the normalized values back to the original array
        search_array[..., 1] = normalized_slice

        return search_array
                    

    def generate_array(self, dataset):
        array = np.zeros((100, 100, 30))
        min_value = math.inf
        max_value = -math.inf
        for i in range(1, 31):
            with open(dataset + str(i) + '.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[1] == 'x':
                        continue
                    x = int(row[1])
                    y = int(row[2])
                    if row[3] != '':
                        value = float(row[3])
                        if value < min_value:
                            min_value = value
                        if value > max_value:
                            max_value = value
                        array[x][y][i - 1] = value

        #normalize between 0 and 1
        array = array - np.min(array)
        return array / np.max(array)
                        

    def generate_arrays(self):
        self.alga_array = self.generate_array(ALGA_DATASET)
        self.coral_array = self.generate_array(CORAL_DATASET)
        self.helium_array = self.generate_array(HELIUM_DATASET)
        self.metal_array = self.generate_array(METAL_DATASET)
        self.oil_array = self.generate_array(OIL_DATASET)
        self.ship_array = self.generate_array(SHIP_DATASET)
        self.species_array = self.generate_array(SPECIES_DATASET)
        self.temp_array = self.generate_array(TEMP_DATASET)
        self.wind_array = self.generate_array(WIND_DATASET)
        self.world_array = self.generate_array(WORLD_ARRAY_DATASET)

        self.OBTAIN = [self.helium_array, self.metal_array, self.oil_array, self.ship_array]
        self.PRESERVE = [self.coral_array]


if __name__ == '__main__':
    db = DataBuilder()
    search_space = db.search_space
    json.dump(search_space.tolist(), open('search_space.json', 'w'))
    # test = db.get_possible_moves(11, 45)
    # print(test)
    # print(len(test))
    

