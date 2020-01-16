try:
    from functions3_2 import expand, insertQueuer
except:
    print("unable to import functions3_2")
    exit()
print("--> good import functions3_2 !")

def SearchPath(allStates, allnodeslist, path):
    for i in allStates:
        if allnodeslist[i]['state'] == [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            index = i
            while index > 0:
                path.append(allnodeslist[index]['act'])
                index = allnodeslist[index]['parentnode_id']
            path.reverse()
            return path
    return False

def aStarSearch(curState, expandNodesQ):
    allnodeslist = []
    Queuer = []
    path = []
    nodeId = 0
    node0 = {'act': 'Stop', 'cost': 0, 'node_id': nodeId, 'parentnode_id': -1, 'state': curState}
    allnodeslist.append(node0)
    Queuer.append((nodeId, 0))
    while True:
        currNode = Queuer.pop(0)
        currNodeId = currNode[0]
        allStates = expand(currNodeId, allnodeslist)
        insertQueuer(allStates, Queuer, allnodeslist)
        getPath = SearchPath(allStates, allnodeslist, path)
        if getPath:
            return getPath

print(aStarSearch([6, 3, 8, 7, 5, 4, 0, 2, 1], 10000))