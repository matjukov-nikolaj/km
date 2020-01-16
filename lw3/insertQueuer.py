# ----------------------- begin of user function --------------------------
# ----- Данную функцию программирует обучающийся !!!  -----
# ----- Функция вставляет номера новых узлов в очередь на раскрытие -----
# ----- в соответствии с их стоимостью
def insertQueuer(nodeNumsList, Queuer, allnodeslist):
    '''
    nodeNumsList - список номеров узлов,
    Queuer  - очередь номеров узлов на раскрытие в порядке неубывания стоимости пути до узла вида
    Queuer = [(1,1), (2,1), (3,1), (4,2)]. Реализуется в виде списка кортежей вида (nodeId, cost)
    ФУНКЦИя берет список узлов с номерами nodeNumsList из списка allnodeslist и затем номера этих узлов
    ставит в очередь Queuer в соответствии с требованием неубывания cost - стоимости пути до  узла.
    При этом, если два узла имеют одинаковую стоимость cost, то первым в очереди оказывается тот узел,
    который раньше поставлен в очередь.
    функция ничего не возвращает, просто изменяет очередь Queuer
    '''
    if(len(nodeNumsList) > 0):
        # добавляем номера новых узлов в очередь в соответствии со стоимостью пути
        for num in nodeNumsList:
            Queuer.append((allnodeslist[num]['node_id'], allnodeslist[num]['cost']))
    return(True) # не обязательно - просто символизирует завершение функции

# ---------------------- end of user fun ---------------------------