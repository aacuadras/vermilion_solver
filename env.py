#CSCI 4352 Team 4
#Emtpy file to write the environment
#TODO: Make sure that there is only one 1 
import numpy as np

def validMatrix(grid) ->bool:
    for i in range(3):
        for j in range(5):
            if(grid[i][j] == 1):
                if(i % 2 == j % 2):
                    return True
    return False

class Environment:
    def __init__(self):
        self.grid = np.random.binomial(1, 0.01, size=(3,5))
        while(not validMatrix(self.grid)):
            self.grid = np.random.binomial(1, 0.01, size=(3,5))

    def getGrid(self):
        return self.grid
