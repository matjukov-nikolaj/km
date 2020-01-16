dirshift = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}
Xcoords = (0, 1, 2, 0, 1, 2, 0, 1, 2)
Ycoords = (0, 0, 0, 1, 1, 1, 2, 2, 2)

def getSuccessor(state, act):
    dirshift = {'left': (-1,0),'right': (1,0), 'up': (0,-1), 'down': (0,1)}
    Xcoords = (0,1,2,0,1,2,0,1,2)
    Ycoords = (0,0,0,1,1,1,2,2,2)
    zeroindex = state.index(0)
    Xzero = Xcoords[zeroindex]
    Yzero = Ycoords[zeroindex]
    nextRow = Yzero + dirshift[act][1]
    nextCol = Xzero + dirshift[act][0]
    if(not(nextRow in range(3) and nextCol in range(3))):
        return([])
    nextstate = state[:]
    nextNum = nextCol + 3*nextRow
    nextstate[zeroindex] = state[nextNum]
    nextstate[nextNum] = 0
    return(nextstate)


def expand(nodeId, allnodeslist):
    node = allnodeslist[nodeId]
    nodeNumsList = []
    stepsList = ['left', 'right', 'up', 'down']
    newId = len(allnodeslist) - 1
    for i in range(len(stepsList)):
        currStep = stepsList[i]
        newState = getSuccessor(node['state'], currStep)
        if newState != []:
            newId += 1
            nodeObject = {'act': currStep, 'cost': node['cost'] + 1, 'node_id': newId, 'parentnode_id': node['node_id'], 'state': newState}
            allnodeslist.append(nodeObject)
            nodeNumsList.append(newId)
    return(nodeNumsList)


def heuristicfun(state):
    h = 0
    for i in range(9):
        h = h + abs(Xcoords[i] - Xcoords[state[i]]) + abs(Ycoords[i] - Ycoords[state[i]])
    return h


def priorityfun(node):
    priority = node['cost'] + heuristicfun(node['state'])
    return priority

def insertQueuer(nodeNumsList, Queuer, allnodeslist):
    if len(nodeNumsList) >= 0:
        for num in nodeNumsList:
            Queuer.append((allnodeslist[num]['node_id'], priorityfun(allnodeslist[num])))
    Queuer.sort(key=lambda numKey: numKey[1])

    return True
