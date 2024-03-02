import csv
import numpy as np

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
        self.world_array = None

        self.generate_arrays()

    #0 is land, 1 is water

    def get_search_value_at(self, x, y, z):
        if x < 0 or x > 99 or y < 0 or y > 99 or z < 0 or z > 29:
            return 0
        value = 0
        for array in self.OBTAIN:
            value += array[x][y][z]
        for array in self.PRESERVE:
            value -= array[x][y][z]
        return value
    
    def isLand(self, x, y):
        return self.world_array[x][y][0] == 0

    def get_search_space(self):
        search_array = np.zeros((100, 100, 30, 2))
        for i in range(100):
            for j in range(100):
                for k in range(30):
                    isLand = self.world_array[i][j][k]
                    value = self.get_search_value_at(i, j, k)
                    search_array[i][j][k][0] = isLand
                    search_array[i][j][k][1] = value

        return search_array
                    

    def generate_array(self, dataset):
        array = np.zeros((100, 100, 30))
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
                        array[x][y][i - 1] = value

        return array
                        

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
    search_space = db.get_search_space()
    print(search_space)
    

