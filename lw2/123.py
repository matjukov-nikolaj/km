dirshift = {'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}
Xcoords = (0, 1, 2, 0, 1, 2, 0, 1, 2)
Ycoords = (0, 0, 0, 1, 1, 1, 2, 2, 2)
state0 = [1, 2, 3, 0, 4, 5, 6, 7, 8]


def getSuccessors(state):
    left = False
    right = False
    up = False
    down = False
    zeroIndex = state.index(0)
    zeroCoordX = Xcoords[zeroIndex]
    zeroCoordY = Ycoords[zeroIndex]
    if (((zeroCoordX + dirshift.get('left')[0]) > -1) and ((zeroCoordX + dirshift.get('left')[0]) < 3)
        and ((zeroCoordY + dirshift.get('left')[1]) > -1) and ((zeroCoordY + dirshift.get('left')[1]) < 3)):
        left = True
    if (((zeroCoordX + dirshift.get('right')[0]) > -1) and ((zeroCoordX + dirshift.get('right')[0]) < 3)
        and ((zeroCoordY + dirshift.get('right')[1]) > -1) and ((zeroCoordY + dirshift.get('right')[1]) < 3)):
        right = True
    if (((zeroCoordX + dirshift.get('up')[0]) > -1) and ((zeroCoordX + dirshift.get('up')[0]) < 3)
        and ((zeroCoordY + dirshift.get('up')[1]) > -1) and ((zeroCoordY + dirshift.get('up')[1]) < 3)):
        up = True
    if (((zeroCoordX + dirshift.get('down')[0]) > -1) and ((zeroCoordX + dirshift.get('down')[0]) < 3)
        and ((zeroCoordY + dirshift.get('down')[1]) > -1) and ((zeroCoordY + dirshift.get('down')[1]) < 3)):
        down = True
    nodeList = []

    if left:
        znach = state[zeroIndex - 1]
        leftState = []
        leftState = state.copy()
        leftState.pop(zeroIndex - 1)
        leftState.pop(zeroIndex - 1)
        leftState.insert(zeroIndex - 1, 0)
        leftState.insert(zeroIndex, znach)
        nodeList.append(leftState)

    if right:
        znach = state[zeroIndex + 1]
        rightState = []
        rightState = state.copy()
        rightState.pop(zeroIndex)
        rightState.pop(zeroIndex)
        rightState.insert(zeroIndex, 0)
        rightState.insert(zeroIndex, znach)
        nodeList.append(rightState)

    if up:
        znach = state[zeroIndex - 3]
        upState = []
        upState = state.copy()
        upState.pop(zeroIndex)
        upState.pop(zeroIndex - 3)
        upState.insert(zeroIndex - 3, 0)
        upState.insert(zeroIndex, znach)
        nodeList.append(upState)

    if down:
        znach = state[zeroIndex + 3]
        downState = []
        downState = state.copy()
        downState.pop(zeroIndex + 3)
        downState.pop(zeroIndex)
        downState.insert(zeroIndex, znach)
        downState.insert(zeroIndex + 3, 0)
        nodeList.append(downState)

    return (nodeList)

def getAllStates(state0, depth):
    allstatelist = []
    someStates = []
    commonState = []
    commonState.append(state0)
    for k in range(depth):
        for j in range(len(commonState)):
            someStates = getSuccessors(commonState[j])
            for i in range(len(someStates)):
                newState = someStates[i]
                if (newState not in allstatelist):
                    allstatelist.append(newState)
            commonState = allstatelist
    print(len(allstatelist))
    return (allstatelist)


getAllStates(state0, 8)
