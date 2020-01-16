try:
    from getSuccessors import getSuccessors
except:
    print("unable to import getSuccessors")
    exit()
state0 = [1, 2, 3, 0, 4, 5, 6, 7, 8]

def includeNewState(tempState, allState):
    for i in range(len(tempState)):
        if (tempState[i] not in allState):
            allState.append(tempState[i])
    return(allState)

def getAllStates(state0, depth):
    allstatelist = []
    temp = []
    tempList = []
    tempList.append(state0)
    for i in range(depth):
        for j in range(len(tempList)):
            temp = getSuccessors(tempList[j])
            tempList = includeNewState(temp, allstatelist)
    return (allstatelist)

lol = getAllStates(state0, 8)
print(len(lol))
