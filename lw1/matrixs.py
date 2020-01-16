import numpy as np

def graph_permutation(GM):
    n = np.shape(GM)[0]
    GP = np.array(range(n))

    for i in range(n):
        GP[i] = 0

    for i in range(n):
        vertical_sum   = 0
        horysontal_sum = 0

        for j in range(n):
            if GM[i][j] == 1:
                GP[i] = j + 1
                horysontal_sum += 1
                vertical_sum   += 1

        if vertical_sum != 1 or horysontal_sum != 1:
            return False


    return GP


def graph_cycl_formula(GP):
    CF = []

    check_cycles = {i for i in range(len(GP))}

    while len(check_cycles) != 0:
        new_cycle = 0
        start_cycle = check_cycles.pop()
        new_cycle += 1
        next = GP[start_cycle] - 1

        while start_cycle != next:
            check_cycles.remove(next)
            new_cycle += 1
            next = GP[next] - 1

        CF.append(new_cycle)
        CF.sort()

    return CF

def get_graph_cycl_formula(GP):
    CF = []
    check_cycles = []
    for i in range(len(GP)):
        check_cycles.append(i+1)
    check_cycles.reverse()

    while len(check_cycles) != 0:
        new_cycle = []
        start_cycle = check_cycles.pop()
        new_cycle.append(start_cycle)
        next = GP[start_cycle - 1]

        while start_cycle != next:
            check_cycles.remove(next)
            new_cycle.append(next)
            next = GP[next - 1]

        CF.append(new_cycle)


    return CF



def check_matrix(GM1, GM2):
    GM1_permutation = graph_permutation(GM1)
    GM2_permutation = graph_permutation(GM2)

    GM1_cycle = graph_cycl_formula(GM1_permutation)
    GM2_cycle = graph_cycl_formula(GM2_permutation)

    GM1_cycle_formula = get_graph_cycl_formula(GM1_permutation)
    GM2_cycle_fromula = get_graph_cycl_formula(GM2_permutation)

    if GM1_cycle == GM2_cycle:
        print("---")
        print(GM1_cycle)
        print(GM1_cycle_formula)
        print("---")
        print(GM2_cycle)
        print(GM2_cycle_fromula)

        return True

    return False

def showResult():
    filePath = "D:\\KM\\lw1\\mx\\M"
    exte = ".csv"
    for i in range(7):
        for g in range(7):
            print(i + 1, ' ', g + 1)
            path1 = filePath + str(i + 1) + exte
            path2 = filePath + str(g + 1) + exte
            M1 = np.loadtxt(path1, dtype=int, delimiter=',')
            M2 = np.loadtxt(path2, dtype=int, delimiter=',')
            print(check_matrix(M1, M2))

showResult()