#Random Player Workspace
import env as env
import numpy as np

#Create environment
g = env.Environment()

prob = [
    [.5, .5, .5, .5, .5],
    [.5, .5, .5, .5, .5],
    [.5, .5, .5, .5, .5]
]

col = int(np.random.randint(0, high=5, size=1))
row = int(np.random.randint(0, high=3, size=1))
it = 1
totIt = 1
'''
print(g.getGrid())
print("(%d, %d)\n"%(row, col))
print(g.getGrid()[row][col])
'''
for i in range(10000):
    while(g.getGrid()[row][col] == 0):
        prob[row][col] -= (prob[row][col] * .05)
        col = int(np.random.randint(0, high=5, size=1))
        row = int(np.random.randint(0, high=3, size=1))
        it += 1
        totIt += 1
    print("Iterations: %d"%it)
    it = 1
    prob[row][col] = 1
    g = env.Environment()
    col = int(np.random.randint(0, high=5, size=1))
    row = int(np.random.randint(0, high=3, size=1))

print("\n Total Iterations: %d"%totIt)
print(prob)