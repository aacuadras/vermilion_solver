#Q-Tables workspace
import numpy as np
import time 

def validCoord(row, column) ->bool:
    if(row % 2 == column % 2):
        return True
    else:
        return False

#Set up FIND_STATE
def generateFIND_STATE():
    column = int(np.random.randint(0, high=5, size=1))
    row = int(np.random.randint(0, high=3, size=1))
    while(not validCoord(row, column)):
        column = int(np.random.randint(0, high=5, size=1))
        row = int(np.random.randint(0, high=3, size=1))
    
    return (row, column)


#Environment variables for agent
BOARD_ROWS = 3
BOARD_COLS = 5
FIND_STATE = generateFIND_STATE()
START = (0, 0)
DETERMINISTIC = False


class State:
    def __init__(self, state=START):
        self.board = np.zeros([BOARD_ROWS, BOARD_COLS])
        self.state = state
        self.isEnd = False
        self.determine = DETERMINISTIC

    def giveReward(self):
        if (self.state == FIND_STATE):
            return 1
        else:
            return 0

    def isEndFunc(self):
        if (self.state == FIND_STATE):
            self.isEnd = True
    
    def _chooseActionProb(self, action):
        #TODO: Enter probabilities
        if(action == "up"):
            return np.random.choice(["up", "left", "right"], p=[.8, .1, .1])
        if(action == "down"):
            return np.random.choice(["down", "left", "right"], p=[.8, .1, .1])
        if(action == "left"):
            return np.random.choice(["up", "down", "left"], p=[.1, .1, .8])
        if(action == "right"):
            return np.random.choice(["up", "down", "right"], p=[.1, .1, .8])

    def nxtPosition(self, action):
        """
        action: up, down, left, right
        -------------
        0 | 1 | 2| 3|
        1 |
        2 |
        return next position on board
        """
        #state = (0, 0)
        if self.determine:
            if action == "up":
                nxtState = (self.state[0] - 1, self.state[1])
            elif action == "down":
                nxtState = (self.state[0] + 1, self.state[1])
            elif action == "left":
                nxtState = (self.state[0], self.state[1] - 1)
            elif action == "right":
                nxtState = (self.state[0], self.state[1] + 1)
                #'check' state
            self.determine = False
        else:
            # non-deterministic
            action = self._chooseActionProb(action)
            self.determine = True
            nxtState = self.nxtPosition(action)

        # if next state is legal
        if (nxtState[0] >= 0) and (nxtState[0] <= 2):
            if (nxtState[1] >= 0) and (nxtState[1] <= 4):
                    return nxtState
        return self.state
    '''
    def showBoard(self):
        self.board[self.state] = 1
        for i in range(0, BOARD_ROWS):
            print('-----------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                if self.board[i, j] == 1:
                    token = '*'
                if self.board[i, j] == -1:
                    token = 'z'
                if self.board[i, j] == 0:
                    token = '0'
                out += token + ' | '
            print(out)
        print('-----------------')
    '''
class Agent:
    def __init__(self):
        self.states = []  # record position and action taken at the position
        self.actions = ["up", "down", "left", "right"]
        self.State = State()
        self.isEnd = self.State.isEnd
        #learning rate
        self.lr = 0.2
        self.exp_rate = 0.3
        #exploration rate
        self.decay_gamma = 0.9

        # initial Q values
        self.Q_values = {}
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.Q_values[(i, j)] = {}
                for a in self.actions:
                    self.Q_values[(i, j)][a] = 0  # Q value is a dict of dict

    def chooseAction(self):
    # choose action with most expected value
        mx_nxt_reward = 0
        action = ""

        if np.random.uniform(0, 1) <= self.exp_rate:
            action = np.random.choice(self.actions)
        else:
            # greedy action
            for a in self.actions:
                current_position = self.State.state
                nxt_reward = self.Q_values[current_position][a]
                if nxt_reward >= mx_nxt_reward:
                    action = a
                    mx_nxt_reward = nxt_reward
            # print("current pos: {}, greedy aciton: {}".format(self.State.state, action))
        return action

    def takeAction(self, action):
        position = self.State.nxtPosition(action)
        # update State
        return State(state=position)

    def reset(self):
        self.states = []
        self.State = State()
        self.isEnd = self.State.isEnd

    def play(self, rounds=10):
        i = 0
        while i < rounds:
            # to the end of game back propagate reward
            if(i == rounds / 2):
                FIND_STATE = generateFIND_STATE()
            if self.State.isEnd:
                # back propagate
                reward = self.State.giveReward()    #coordinate where switch is located
                for a in self.actions:
                    self.Q_values[self.State.state][a] = reward #sets all q-values
                print("Found switch!", reward)
                for s in reversed(self.states):
                    current_q_value = self.Q_values[s[0]][s[1]] 
                    reward = current_q_value + self.lr * (self.decay_gamma * reward - current_q_value)  #sets the rewards for the path taken
                    self.Q_values[s[0]][s[1]] = round(reward, 3)    #round to 3 decimals
                self.reset()
                i += 1
            else:
                action = self.chooseAction()
                # append trace
                self.states.append([(self.State.state), action])    #[position, action taken @ that position]
                print("current position {} action {}".format(self.State.state, action))
                # by taking the action, it reaches the next state
                self.State = self.takeAction(action)
                # mark is end
                self.State.isEndFunc()
                print("nxt state", self.State.state)
                print("---------------------")
                time.sleep(.25)
                self.isEnd = self.State.isEnd

if __name__ == "__main__":
    ag = Agent()
    print("initial Q-values ... \n")
    print(ag.Q_values)

    ag.play(50)
    print("latest Q-values ... \n")
    for key in ag.Q_values:
        print(key)
        for values in ag.Q_values[key]:
            print("     ", values, ':', ag.Q_values[key][values])