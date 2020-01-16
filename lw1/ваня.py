import numpy as np


# ----------------------- begin of user function --------------------------
# --- Эту функцию программирует обучающийся!!! ----
def graph_permutation(GM):
    GP = np.array(range(0, GM.shape[0]))
    isGraftedLine = True

    numberLine = 0
    numberVertex = 0

    for line in GM:
        amountArcsInLine = 0

        for itemLine in range(GM.shape[0]):
            if line[itemLine] == 1:
                if numberVertex != itemLine:
                    amountArcsInLine += 1
                    numberVertex = itemLine
                else:
                    print("В столбце больше одной единицы")
                    isGraftedLine = False
            elif line[itemLine] > 1:
                print("Стоимость выше единицы")
                isGraftedLine = False

        if amountArcsInLine == 1:
            GP[numberLine] = numberVertex + 1
        else:
            print("В строке больше одной единицы")
            isGraftedLine = False
        numberLine += 1

    if isGraftedLine:
        res = GP
    else:
        res = []

    return res


# --- Эту функцию программирует обучающийся!!! ----
def graph_cycle_formula(GP):
    CF = []

    for itemGP in GP:
        nextItemGP = GP[itemGP - 1]
        cycle = [itemGP]
        count = 0
        res = False
        while count <= GP.__len__():
            if GP[nextItemGP - 1] == itemGP:
                if nextItemGP != itemGP:
                    cycle += [nextItemGP]
                res = True
                break
            else:
                cycle += [nextItemGP]
            nextItemGP = GP[nextItemGP - 1]
            count += 1

        if res:
            cycle.sort()
            for itemCF in CF:
                if itemCF == cycle:
                    res = False
                    break
            if res:
                CF += [cycle]

    return CF


# ---------------------- end of user fun ---------------------------
GM_1 = np.array([[0,1,0], [1,0,0], [0,0,1]])
GP1 = graph_permutation(GM_1)
print(GP1)
CF_1 =  graph_cycl_formula(GP1)
print(CF_1)