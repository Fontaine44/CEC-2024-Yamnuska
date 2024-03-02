import numpy as np

class Path: 
    def __init__(self, length):
        self.path = np.empty((length, 3), dtype=int)
    
    def set_day_position(self, index, x, y, value):
            self.path[index][0] = x
            self.path[index][1] = y
            self.path[index][2] = value

    def get_day_value(self, index):
        return self.path[:, index]
        
    def get_total_value(self):
        return np.sum(self.path[2, :])