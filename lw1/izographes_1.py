import numpy as np

# ----------------------- begin of user function --------------------------
# --- Эту функцию программирует обучающийся!!! ----
GM_1 = np.array([[0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 0, 0, 0, 0, 0]])



def graph_permutation(GM):
    GP = np.array(range(1, GM.shape[0] + 1))
    unitsAmount = 0
    for i in range(len(GM)):
        unitsAmount = 0
        for j in range(len(GM[i])):
            if GM[i][j] == 1:
                unitsAmount += 1
                GP[i] = j + 1
        if unitsAmount == 1:
            result = GP
        else:
            result = False
            break


    return result


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

    matrix = []
    numberOfElements = len(GP)
    for i in range(numberOfElements):
        newList = []
        for j in range(numberOfElements):
            newList.append(0)
        matrix.append(newList)

    for i in range(numberOfElements):
        matrix[i][GP[i] - 1] = 1

    helpList = []
    for i in range(numberOfElements):
        helpList.append(i)


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

def getMatrix():
    M1 = np.loadtxt("D:\\KM\\lw1\\m1.txt", dtype=int, delimiter=" ")
    return M1


def getQuantityCycles(CF):
    maxEl = 0
    for i in range(len(CF)):
        for j in range(len(CF[i])):
            if CF[i][j] > maxEl:
                maxEl = CF[i][j]

    NumCyclesArr = np.array(range(maxEl)) * 0

    for i in range(len(CF)):
        for j in range(len(CF[i])):
            lenCycle = len(CF[i])
            NumCyclesArr[lenCycle - 1] = lenCycle / 2
        lenCycle = 0

    return NumCyclesArr




M1 = getMatrix()
GM_2 = graph_permutation(M1)
print(M1)

GP1 = graph_permutation(GM_2)
print(GP1)

CF_1 = graph_cycl_formula(GP1)
print(CF_1)

GET_1 = getQuantityCycles(CF_1)
print(GET_1)
# ---------------------- end of user fun ---------------------------
