import numpy as np

class Path: 

    # Constructor
    def __init__(self, length):
        self.path = np.empty((length, 3), dtype=float)
    
    # Sets the position of the rigg at a certain day
    def set_day_position(self, index, x, y, value):
            self.path[index][0] = x
            self.path[index][1] = y
            self.path[index][2] = value

    # Gets the value extracted by the rigg at a certain day
    def get_day_value(self, index):
        return self.path[:, index]
    
    # Gets the position of the rigg at a certain day 
    def get_day_position(self, index):
        return self.path[index][0], self.path[index][1]
        
    # Gets the total value extracted by the rigg
    def get_total_value(self):
        return np.sum(self.path[:, 2])