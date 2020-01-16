
# --- Эту функцию программирует обучающийся!!! ----
def getNewCycleBegin(helpList):
    i = 0

    while i != len(helpList):
        if helpList[i] != -1:
            return i
        i += 1

    return -1



def graph_cycl_formula(GP):
    CF = []

    # Creation the matrix
    matrix = []
    numberOfElements = len(GP)
    for i in range(numberOfElements):
        newList = []
        for j in range(numberOfElements):
            newList.append(0)
        matrix.append(newList)

    for i in range(numberOfElements):
        matrix[i][ GP[i] - 1 ] = 1

    # Creation helpList
    helpList = []
    for i in range(numberOfElements):
        helpList.append(i)


    # Main loop
    while True:
        cycleBegin = getNewCycleBegin(helpList)
        newCycle = []
        if cycleBegin == -1:
            break

        helpList[cycleBegin] = -1
        nextElem = 0
        newCycle.append(cycleBegin + 1)

        for i in range(numberOfElements):
            if matrix[cycleBegin][i] == 1:
                nextElem = i
                break

        while nextElem != cycleBegin:
            newCycle.append(nextElem + 1)
            helpList[nextElem] = -1

            for i in range(numberOfElements):
                if matrix[nextElem][i] == 1:
                    nextElem = i
                    break
        CF.append(newCycle)


    return CF

# ---------------------- end of user fun ---------------------------

