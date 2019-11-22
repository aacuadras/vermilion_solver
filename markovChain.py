#Markov Chain workspace
import env as env
import numpy as np
import time

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
 
    def generate_states(self, current_state, no=10):
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

#Markov chain driver

tran_matrix = [
    [.7, .3],
    [.2, .8]
]

#Generate markov chain
switch_chain = MarkovChain(tran_matrix, states=[0, 1])
#Generate environment
g = env.Environment()

#observe first cell 50 times and output the states
for i in range(50):
    print("State " + str(i) + ": " + str(switch_chain.next_state(g.getGrid()[0][0])))
    time.sleep(0.5)
    g = env.Environment()

#generate states
# From 'switch_chain.generate_states(g.getGrid()[x][y]))' we can get the probability
#of getting new states, for that we have to get the probability of ones
stts = switch_chain.generate_states(g.getGrid()[0][0])
print(stts)
print("Probability: " + str(probability(stts)))
    