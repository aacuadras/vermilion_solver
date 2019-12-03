#Markov Chain workspace
#import env as env
import numpy as np
import time
import matplotlib.pyplot as plt

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

    def isEndFunc(self):
        if (self.state == FIND_STATE):
            self.isEnd = True

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
                self.isEndFunc()
                self.state = nxtState
                return nxtState
        return self.state

    def reset(self):
        self.state = START
        self.isEnd = False

    def printMatrix(self):
        print("o-o-o-o-o-o")
        for i in range(3):
            print("|", end="")
            for j in range(5):
                if (i == self.state[0] and j == self.state[1]):
                    print("O", end="")
                elif (i == FIND_STATE[0] and j == FIND_STATE[1]):
                    print("X", end="")
                else:
                    print(" ", end="")
                print("|", end="")
            print("\no-o-o-o-o-o")


class MarkovChain:
    def __init__(self, transition_matrix, states):
        self.transition_matrix = np.atleast_2d(transition_matrix)
        self.states = states
        self.index_dict = {self.states[index]: index for index in 
                           range(len(self.states))}
        self.state_dict = {index: self.states[index] for index in
                           range(len(self.states))}
 
    def next_state(self, current_state):
        return np.random.choice(
         self.states, 
         p=self.transition_matrix[self.index_dict[current_state], :]
        )
 
    def generate_states(self, current_state, no=50):
        future_states = []
        for i in range(no):
            next_state = self.next_state(current_state)
            future_states.append(next_state)
            current_state = next_state
        return future_states

    def getMatrix(self):
        return self.transition_matrix


def probability(arr) ->float:
    count = 0
    for i in arr:
        if(i == 1):
            count += 1
    
    return count / len(arr)


'''Markov chain driver'''
tran_matrix = [
    [.5, 0, .25, .25],
    [0, .5, .25, .25],
    [.25, .25, .5, 0],
    [.25, .25, 0, .5]
]


#Create a markov chain for every trashcan
if __name__ == "__main__":
    env = Environment()
    agent = MarkovChain(tran_matrix, states=["up", "down", "left", "right"])
    t = []
    s =[]
    timeTaken = np.array([], dtype=np.float32)
    switchNum = np.array([], dtype=np.float32)
    currState = "right"

    for j in range(300):
        startTime = time.time()

        while(not env.isEnd):
            currState = agent.next_state(currState)
            print(currState)
            print("----------------")
            env.move(currState)
            env.printMatrix()
            time.sleep(.25) 
        env.reset()       
        s.append(j + 1)
        t.append(time.time() - startTime)
    '''
    timeTaken = np.append(timeTaken, t)
    switchNum = np.append(switchNum, s)
    plt.plot(switchNum, timeTaken)
    plt.xlabel("Switch number")
    plt.ylabel("Time taken")
    plt.title("Markov Chain")
    plt.show()
    '''