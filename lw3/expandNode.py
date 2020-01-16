def getSuccessor(state, act):
    '''
    state: состояние игры в "8", например state = [1,2,3,4,5,6,7,8,0]
    функция возращает 'newstate' - соседнее состояние, если 'act' - действие, 
    которое переводит игру из состояния state в newstate
    функция возвращает [], если ход недопустимый
    '''
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

# ----------------------- begin of user function -------------------------
# ----- Данную функцию программирует обучающийся !!!                -----
# --- Функция для узла с номером nodeId из списка allnodeslist вида -----
# --- node0 = (act, cost, node_id, parentnode_id, state)            -----
# --- формирует список дочерних узлов дерева поиска и добавляет их  -----
# --- в список allnodeslist и выводит их номера nodeNumsList        ----- 
def expand(nodeId, allnodeslist):
    '''
    Вход: nodeId - номер узла в списке allnodeslist
    узел описывается словарем и имеет следующую структуру:
    node = {'act': 'Stop', 'cost': 0, 'node_id': 0, 'parentnode_id': -1, 'state': [1,2,3,4,5,6,7,8,0]}
    Выход:
    генерация дочерных узлов и включение их в список allnodeslist
    nodeNumsList = [node1, node2, ...]  - список номеров дочерних узлов в allnodeslist
    '''
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

# ---------------------- end of user fun ---------------------------
