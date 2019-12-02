FIND_STATE = (2, 2)

def printMatrix(x, y):
    print("o-o-o-o-o-o")
    for i in range(3):
        print("|", end="")
        for j in range(5):
            if (i == x and j == y):
                print("O", end="")
            elif (i == FIND_STATE[0] and j == FIND_STATE[1]):
                print("X", end="")
            else:
                print(" ", end="")
            print("|", end="")
        print("\no-o-o-o-o-o")

printMatrix(2, 2)