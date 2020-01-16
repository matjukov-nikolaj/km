state0 = [0, 3, 2, 4, 5, 8, 6, 1, 7]

dirshift = {'left': (-1,0),'right': (1,0), 'up': (0,-1), 'down': (0,1)}
Xcoords = (0,1,2,0,1,2,0,1,2)
Ycoords = (0,0,0,1,1,1,2,2,2)
state0 = [1, 2, 3, 0, 4, 5, 6, 7, 8]

# [[0, 3, 2, 4, 5, 8, 6, 1, 7]]
# [[3, 5, 2, 4, 0, 8, 6, 1, 7]]
# [[3, 2, 0, 4, 5, 8, 6, 1, 7]]
def getMovingDirection(states, delta, zeroIndex):
    tempList = []
    exchEl = 0
    currState = []
    currState += states
    lenCurrState = len(currState)
    for i in range(lenCurrState):
        if i == zeroIndex:
            exchEl = currState[i + delta]
            currState[i + delta] = currState[i]
            currState[i] = exchEl
    tempList += currState
    return tempList


def getSuccessors(state):
    nodeList = []
    lenState = len(state)
    zeroIndex = 0
    for i in range(lenState):
        if state[i] == 0:
            zeroIndex = i
    if (zeroIndex >= 0) and (zeroIndex < 6):
        nodeList.append(getMovingDirection(state, +3, zeroIndex))
    if (zeroIndex != 8) and (zeroIndex != 5) and (zeroIndex != 2):
        nodeList.append(getMovingDirection(state, +1, zeroIndex))
    if (zeroIndex != 0) and (zeroIndex != 3) and (zeroIndex != 6):
        nodeList.append(getMovingDirection(state, -1, zeroIndex))
    if (zeroIndex >= 3) and (zeroIndex <= 8):
        nodeList.append(getMovingDirection(state, -3, zeroIndex))

    return(nodeList)
