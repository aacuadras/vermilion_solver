#Random Player Workspace
import env as env
import numpy as np
import time

#Create environment
def validCoord(row, column) ->bool:
    if(row % 2 == column % 2):
        return True
    else:
        return False

def generateFIND_STATE():
    column = int(np.random.randint(0, high=5, size=1))
    row = int(np.random.randint(0, high=3, size=1))
    while(not validCoord(row, column)):
        column = int(np.random.randint(0, high=5, size=1))
        row = int(np.random.randint(0, high=3, size=1))
    
    return (row, column)

BOARD_ROWS = 3
BOARD_COLS = 5
FIND_STATE = generateFIND_STATE()
START = (0, 0)

class Environment:
    def __init__(self, state=START):
        self.board = np.zeros([BOARD_ROWS, BOARD_COLS])
        self.state = state
        self.isEnd = False
        self.secondSwitch = (0, 0)


    def isEndFunc(self):
        if (self.state == FIND_STATE):
            self.isEnd = True
            print("Found Switch!")
            print("Generating second switch")
            print("---------------------")
            self.generateSecondSwitch()
            self.printMatrix()
            time.sleep(1.)
            self.move(np.random.choice(["up", "down", "left", "right"]))
            self.printMatrix()
            time.sleep(.5)
            if(g.state == g.secondSwitch):
                print("Found second switch")


    def generateSecondSwitch(self):
        if(self.state == (0, 0)):
            self.secondSwitch = (0, 1)
        elif(self.state == (0, 4) or self.state == (1, 3) or self.state == (2, 4)):
            self.secondSwitch = (1, 4)
        elif(self.state == (1, 1)):
            self.secondSwitch = (1, 2)
        elif(self.state == (2, 0)):
            self.secondSwitch = (2, 1)
        elif(self.state == (0, 2)):
            second = [(0, 1), (1, 2), (0, 3)]
            indices = np.arange(len(second))
            choose = np.random.choice(indices)
            self.secondSwitch = second[choose]
        elif(self.state == (2, 2)):
            second = [(2, 1), (1, 2), (2, 3)]
            indices = np.arange(len(second))
            choose = np.random.choice(indices)
            self.secondSwitch = second[choose]


    def move(self, action):
        if action == "up":
            nxtState = (self.state[0] - 1, self.state[1])
        elif action == "down":
            nxtState = (self.state[0] + 1, self.state[1])
        elif action == "left":
            nxtState = (self.state[0], self.state[1] - 1)
        elif action == "right":
            nxtState = (self.state[0], self.state[1] + 1)

        if (nxtState[0] >= 0) and (nxtState[0] <= 2):
            if (nxtState[1] >= 0) and (nxtState[1] <= 4):
                #self.isEndFunc()
                self.state = nxtState
                return nxtState
        return self.state

    def reset(self):
        self.state = START
        self.isEnd = False
        self.secondSwitch = START

    def printMatrix(self):
        print("o-o-o-o-o-o")
        for i in range(3):
            print("|", end="")
            for j in range(5):
                if(self.isEnd):
                    if (i == self.state[0] and j == self.state[1]):
                        print("O", end="")
                    elif(i == self.secondSwitch[0] and j == self.secondSwitch[1]):
                        print("2", end="")
                    else:
                        print(" ", end="")
                else:
                    if (i == self.state[0] and j == self.state[1]):
                        print("O", end="")
                    elif (i == FIND_STATE[0] and j == FIND_STATE[1]):
                        print("X", end="")
                    else:
                        print(" ", end="")
                print("|", end="")
            print("\no-o-o-o-o-o")



g = Environment()

for i in range(10000):
    while(not g.isEnd):
        g.move(np.random.choice(["up", "down", "left", "right"]))
        g.printMatrix()
        g.isEndFunc()
        print("---------------------")
        time.sleep(.50)
    g.reset()
    FIND_STATE = generateFIND_STATE()
    