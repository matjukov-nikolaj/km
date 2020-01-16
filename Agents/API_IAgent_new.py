# -*- coding: utf-8 -*-
"""
Created on Fri May  5 12:26:57 2017

@author: nehaevin
"""

import requests;
import random

url = 'https://mooped.net/local/its/index.php?module=game&action=agentaction'
url = 'https://mooped.net/local/its/game/agentaction/?gameid=GAMEID&userid=USERID&act=ACT'
url = 'https://mooped.net/local/its/game/agentaction/?id=2&userid=2&act=noAct noAct'
url = 'https://mooped.net/local/its/game/agentaction/'
http_proxy = "http://10.0.0.4:3128"
https_proxy = "https://10.0.0.4:3128"
proxyDict = {
    "http": http_proxy,
    "https": https_proxy
}

passivMoves = ['noAct', 'onLeft', 'upSideDn', 'onRight']
activMoves = ['Go', 'Shoot', 'Take', 'noAct']
alldirsN = {'Up': 0, 'Right': 1, 'Down': 2, 'Left': 3}
alldirs = ['Up', 'Right', 'Down', 'Left']

allkeys = alldirsN.keys()
type(alldirsN.values())

# заменить на свой user_id
user_id = 2845

# Выбор кейса
case_id = 1  # L-1 (Поиск клада. Известный Лабиринт. 2 обвала. 1 монстр.)
# case_id = 6  #L-2 (Поиск клада. Неизвестный Лабиринт. Без обвалов. Без монстра.)
# case_id = 7 #L-3 (Поиск клада. Неизвестный Лабиринт. 1 обвал. Без монстра)
# case_id = 4 #L-4 (Поиск клада. Неизвестный Лабиринт. 2 обвала. Без монстра. )
# case_id = 2 #L-5 (Поиск клада. Неизвестный Лабиринт. 2 обвала. 1 монстр.)

# Выбор карты
mapnum = 120


def connect(case_id, user_id, mapnum=1, passivAct='noAct', activAct='noAct'):
    # url1 = url + "?gameid=129&userid=7&act=noAct+noAct"
    resp = requests.get(url, params={'caseid': case_id, 'userid': user_id, 'mapnum': mapnum, 'passive': passivAct,
                                     'active': activAct}, verify=False)  # proxies = proxyDict, verify=False)
    # проверка успешности установки связи с сервером
    if resp.status_code == 200:
        # Print the status code of the response.
        print("----- соединение установлено -----")
        print("Выбран ход:", " ".join([passivAct, activAct]))
        json1 = resp.json()
        # print(json1['error'])
        # str(json2)
    else:
        json1 = None
    return (json1)


# определение противоположного направления движения
def backdir(curdir="Up"):
    # type: (object) -> object
    newdirN = (alldirsN[curdir] + 2) % 4
    # if(newdir > 3) newdir = newdir - 4
    newdir = alldirs[newdirN]
    return (newdir)


# print(backdir("Left"))
# print(backdir("Right"))

# определение номера противоположного направления движения
def backdirN(curdirN=0):
    newdirN = (curdirN + 2) % 4
    return (newdirN)


# backdirN(3)

# определение того, куда надо повернуться от текущего направления движения Агента к новому направлению
def chooseRotation(IAdirN=2, newdirN=0):
    dirdiff = (IAdirN - newdirN + 4) % 4
    return (passivMoves[dirdiff])


# chooseRotation(3,1)
def getNextCave(currCave, direction):
    nextCave = ''
    if direction == 'Left':
        nextCave = currCave[0] + '_' + str(int(currCave[2]) - 1)
    if direction == 'Right':
        nextCave = currCave[0] + '_' + str(int(currCave[2]) + 1)
    if direction == 'Up':
        nextCave = str(int(currCave[0]) - 1) + '_' + currCave[2]
    if direction == 'Down':
        nextCave = str(int(currCave[0]) + 1) + '_' + currCave[2]
    return nextCave


# Выбор хода по текущему восприятию
# Реагируем по особому на кости. Никак не реагируем на ветер. Может погибнуть в обвалах.
def chooseAct(percept, caveWithGold, caveWithMonster, cavesWithHoles):
    # * currentcave	- информация о текущей пещере
    # * worldinfo		- информация о мире
    # * iagent			- информация об агенте
    # * userid			- идентификатор пользователя
    curcave = percept['currentcave']
    worldinfo = percept['worldinfo']
    AgentState = percept['iagent']
    dirs = curcave['dirList']
    IAdir = AgentState['dir']
    lastMove = AgentState['choosenact']
    passivAct = 'noAct'
    if (curcave['isGold']):  # берем золото
        passivAct = 'noAct'
        activAct = 'Take'
    elif (curcave['isBones'] and worldinfo['ismonsteralive'] == 1):  # стреляем в монстра
        dirlist = list(dirs.keys())
        if backdir(IAdir) in dirlist:
            dirlist.remove(backdir(IAdir))
        for i in range(len(dirlist)):
            nextCave = getNextCave(curcave['cNum'], dirlist[i])
            if nextCave == caveWithMonster[0]:
                passivAct = chooseRotation(alldirsN[IAdir], alldirsN[dirlist[i]])
        activAct = 'Shoot'
        print('выстрелил сука')
    else:  # остальные случаи
        # elif(not curcave['isBones'] or worldinfo['ismonsteralive']=='0' or not worldinfo['ismonsteralive']) :
        # рядом нет живого монстра - случайный ход в новом направлении
        dirlist = list(dirs.keys())
        if backdir(IAdir) in dirlist:
            dirlist.remove(backdir(IAdir))
        nextCave = ''
        if worldinfo['ismonsteralive'] == 1:
            for i in range(len(dirlist)):
                nextCave = getNextCave(curcave['cNum'], dirlist[i])
                if ((nextCave == cavesWithHoles[0]) or (nextCave == cavesWithHoles[1])):
                    print('следующая пещера с обвалом')
                    newdirlist = list(dirs.keys())
                    newdirlist.remove(dirlist[i])
                    nextCave = ''
                    for i in range(len(newdirlist)):
                        nextCave = getNextCave(curcave['cNum'], newdirlist[i])
                        if int(caveWithMonster[0][0]) > int(curcave['cNum'][0]) and newdirlist[i] == 'Down':
                            passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Down'])
                        elif int(caveWithMonster[0][0]) < int(curcave['cNum'][0]) and newdirlist[i] == 'Up':
                            passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Up'])
                        else:
                            if int(caveWithMonster[0][2]) > int(curcave['cNum'][2]) and newdirlist[i] == 'Right':
                                passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Right'])
                            elif int(caveWithMonster[0][2]) < int(curcave['cNum'][2]) and newdirlist[i] == 'Left':
                                passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Left'])
                else:
                    if int(caveWithMonster[0][0]) > int(curcave['cNum'][0]) and dirlist[i] == 'Down':
                        passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Down'])
                    elif int(caveWithMonster[0][0]) < int(curcave['cNum'][0]) and dirlist[i] == 'Up':
                        passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Up'])
                    else:
                        if int(caveWithMonster[0][2]) > int(curcave['cNum'][2]) and dirlist[i] == 'Right':
                            passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Right'])
                        elif int(caveWithMonster[0][2]) < int(curcave['cNum'][2]) and dirlist[i] == 'Left':
                            passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Left'])
        else:
            for i in range(len(dirlist)):
                nextCave = getNextCave(curcave['cNum'], dirlist[i])
                if ((caveWithGold == cavesWithHoles[0]) or (caveWithGold == cavesWithHoles[1])):
                    if int(caveWithGold[0][0]) > int(curcave['cNum'][0]) and dirlist[i] == 'Down':
                        passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Down'])
                    elif int(caveWithGold[0][0]) < int(curcave['cNum'][0]) and dirlist[i] == 'Up':
                        passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Up'])
                    else:
                        if int(caveWithGold[0][2]) > int(curcave['cNum'][2]) and dirlist[i] == 'Right':
                            passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Right'])
                        elif int(caveWithGold[0][2]) < int(curcave['cNum'][2]) and dirlist[i] == 'Left':
                            passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Left'])
                elif ((nextCave == cavesWithHoles[0]) or (nextCave == cavesWithHoles[1])):
                    print('следующая пещера с обвалом, монстр убит иду к золоту')
                    newdirlist = list(dirs.keys())
                    newdirlist.remove(dirlist[i])
                    nextCave = ''
                    for i in range(len(newdirlist)):
                        nextCave = getNextCave(curcave['cNum'], newdirlist[i])
                        if int(caveWithGold[0][0]) > int(curcave['cNum'][0]) and newdirlist[i] == 'Down':
                            passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Down'])
                        elif int(caveWithGold[0][0]) < int(curcave['cNum'][0]) and newdirlist[i] == 'Up':
                            passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Up'])
                        else:
                            if int(caveWithGold[0][2]) > int(curcave['cNum'][2]) and newdirlist[i] == 'Right':
                                passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Right'])
                            elif int(caveWithGold[0][2]) < int(curcave['cNum'][2]) and newdirlist[i] == 'Left':
                                passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Left'])
                else:
                    if int(caveWithGold[0][0]) > int(curcave['cNum'][0]) and dirlist[i] == 'Down':
                        passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Down'])
                    elif int(caveWithGold[0][0]) < int(curcave['cNum'][0]) and dirlist[i] == 'Up':
                        passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Up'])
                    else:
                        if int(caveWithGold[0][2]) > int(curcave['cNum'][2]) and dirlist[i] == 'Right':
                            passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Right'])
                        elif int(caveWithGold[0][2]) < int(curcave['cNum'][2]) and dirlist[i] == 'Left':
                            passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Left'])

        activAct = 'Go'
    print("-- lastAct=", lastMove, " curPos:", curcave['cNum'])
    print(" choosenAct:", passivAct, activAct)
    return ([passivAct, activAct])


def makeAllCavesList(allCaves):
    for i in range(0, 4):
        for j in range(0, 4):
            allCaves.append(str(i) + '_' + str(j))


# делаем игру - организуем взаимодействие с сервером
def chooseAndAct(case_id, user_id, mapnum):
    # запуск игры:
    passivAct = 'noAct'
    activAct = 'noAct'
    request = connect(case_id, user_id, mapnum, passivAct=passivAct, activAct=activAct)
    allCaves = []
    makeAllCavesList(allCaves)
    # проверка успешности установки связи с сервером
    if (request == None):
        print("Связь с сервером", url, "не установлена")
    else:
        # играем - выбираем ходы и передаем, пока игра не завершится
        perceptTemp = request['text']
        AgentState = perceptTemp['iagent']
        caveWithGold = []
        for currCave in allCaves:
            if AgentState['knowCaves'][currCave]['isGold'] == 1:
                caveWithGold.append(currCave)
        caveWithMonster = []
        for currCave in allCaves:
            if AgentState['knowCaves'][currCave]['isMonster'] == 1:
                caveWithMonster.append(currCave)
        cavesWithHoles = []
        for currCave in allCaves:
            if AgentState['knowCaves'][currCave]['isHole'] == 1:
                cavesWithHoles.append(currCave)
        print(caveWithGold)
        print(cavesWithHoles)
        print(caveWithMonster)
        while (request['error'] == None):
            percept = request['text']
            act = chooseAct(percept, caveWithGold, caveWithMonster, cavesWithHoles)
            request = connect(case_id, user_id, mapnum, passivAct=act[0], activAct=act[1])
    print("Код завершения: ", request['error'])
    return (request['error'])


# Запуск работы агента. Если все хорошо, то будет выдано сообщение "GAME IS REACHED"
chooseAndAct(case_id, user_id, mapnum)
