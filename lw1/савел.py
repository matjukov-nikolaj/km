import numpy as np

# ----------------------- begin of user function --------------------------
# --- Эту функцию программирует обучающийся!!! ----
def graph_permutation(GM):
    n = np.shape(GM)[0]
    GP = np.array(range(n))
    print(n)
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

GM_1 = np.array([[0,1,0], [1,0,0], [0,0,1]])
GP1 = graph_permutation(GM_1)
print(GP1)

# --- Эту функцию программирует обучающийся!!! ----
def graph_cycl_formula(GP):
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

# ---------------------- end of user fun ---------------------------
GM_1 =  np.array([[1, 0, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 1]])
GP1 = graph_permutation(GM_1)
print(GP1)

CF_1 = graph_cycl_formula(GP1)
print(CF_1)