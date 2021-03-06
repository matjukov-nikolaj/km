# -*- coding: utf-8 -*-
"""
Created on Fri May  5 12:26:57 2017

@author: nehaevin
"""

import requests; import random

url	= 'https://mooped.net/local/its/index.php?module=game&action=agentaction'
url = 'https://mooped.net/local/its/game/agentaction/?gameid=GAMEID&userid=USERID&act=ACT'
url = 'https://mooped.net/local/its/game/agentaction/?id=2&userid=2&act=noAct noAct'
url = 'https://mooped.net/local/its/game/agentaction/'
http_proxy  = "http://10.0.0.4:3128"
https_proxy  = "https://10.0.0.4:3128"
proxyDict = {
             "http" : http_proxy,
             "https" : https_proxy
             }

passivMoves	 = ['noAct', 'onLeft', 'upSideDn', 'onRight']
activMoves	 = ['Go', 'Shoot', 'Take', 'noAct']
alldirsN = {'Up':0, 'Right':1, 'Down':2, 'Left':3}
alldirs = ['Up', 'Right', 'Down', 'Left']

allkeys = alldirsN.keys()
type(alldirsN.values())

# заменить на свой user_id
user_id = 2845

# Выбор кейса
#case_id = 1 #L-1 (Поиск клада. Известный Лабиринт. 2 обвала. 1 монстр.)
#case_id = 6  #L-2 (Поиск клада. Неизвестный Лабиринт. Без обвалов. Без монстра.)
#case_id = 7 #L-3 (Поиск клада. Неизвестный Лабиринт. 1 обвал. Без монстра)
case_id = 4 #L-4 (Поиск клада. Неизвестный Лабиринт. 2 обвала. Без монстра. )
#case_id = 2 #L-5 (Поиск клада. Неизвестный Лабиринт. 2 обвала. 1 монстр.)

# Выбор карты
mapnum = 20

def connect(case_id, user_id, mapnum=1, passivAct = 'noAct', activAct = 'noAct'):
  #url1 = url + "?gameid=129&userid=7&act=noAct+noAct"
  resp = requests.get(url, params= {'hash': '5931b6c02a3662f04259fe4434319842', 'passive': passivAct, 'active': activAct}, verify=False) #proxies = proxyDict, verify=False)
  # проверка успешности установки связи с сервером
  if resp.status_code == 200:
    # Print the status code of the response.
    print("----- соединение установлено -----")
    print("Выбран ход:", " ".join([passivAct, activAct]))
    json1 = resp.json()
    #print(json1['error'])
    #str(json2)
  else:
    json1 = None
  return(json1)


# определение противоположного направления движения
def backdir(curdir="Up"):
  # type: (object) -> object
  newdirN = (alldirsN[curdir] + 2) % 4
  #if(newdir > 3) newdir = newdir - 4
  newdir = alldirs[newdirN]
  return(newdir)

#print(backdir("Left"))
#print(backdir("Right"))

# определение номера противоположного направления движения
def backdirN(curdirN= 0) :
  newdirN = (curdirN + 2) % 4
  return(newdirN)

#backdirN(3)

# определение того, куда надо повернуться от текущего направления движения Агента к новому направлению
def chooseRotation(IAdirN=2, newdirN=0) :
  dirdiff = (IAdirN - newdirN + 4) % 4
  return(passivMoves[dirdiff])

#chooseRotation(3,1)

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
def chooseAct(percept, allCaves, visitedCaves, act, windCaves) :
  #* currentcave	- информация о текущей пещере
  #* worldinfo		- информация о мире
  #* iagent			- информация об агенте
  #* userid			- идентификатор пользователя
  curcave = percept['currentcave']
  worldinfo = percept['worldinfo']
  AgentState = percept['iagent']
  dirs = curcave['dirList']
  IAdir = AgentState['dir']
  lastMove = AgentState['choosenact']
  if(curcave['isGold']) : # берем золото
    passivAct = 'noAct'
    activAct = 'Take'
  elif(curcave['isWind']):
      passivAct = 'noAct'
      if len(allCaves) - len(visitedCaves) == 1 or len(allCaves) - len(visitedCaves)  == 2:
          lastCave = list(set(allCaves) - set(visitedCaves))
          if len(lastCave) == 4:
              for i in range(len(lastCave)):
                  if lastCave[i] not in visitedCaves:
                      lastCave.remove(lastCave[i])
          for i in range(len(lastCave)):
              if int(lastCave[i][0]) > int(curcave['cNum'][0]):
                  passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Down'])
              elif int(lastCave[i][0]) < int(curcave['cNum'][0]):
                  passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Up'])
              else:
                  if int(lastCave[i][2]) > int(curcave['cNum'][2]):
                      passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Right'])
                  elif int(lastCave[i][2]) < int(curcave['cNum'][2]):
                      passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Left'])
      else:
          if curcave['cNum'] not in windCaves:
              passivAct = 'upSideDn'
              activAct = 'Go'
      activAct = 'Go'
      if curcave['cNum'] not in visitedCaves:
          visitedCaves.append(curcave['cNum'])
      if curcave['cNum'] not in windCaves:
          windCaves.append(curcave['cNum'])
  else :  # остальные случаи
  #elif(not curcave['isBones'] or worldinfo['ismonsteralive']=='0' or not worldinfo['ismonsteralive']) :
         # рядом нет живого монстра - случайный ход в новом направлении
         passivAct = 'noAct'
         if len(allCaves) - len(visitedCaves)  == 1 or len(allCaves) - len(visitedCaves)  == 2:
             lastCave = list(set(allCaves) - set(visitedCaves))
             if len(lastCave) == 4:
                 for i in range(len(lastCave)):
                     if lastCave[i] not in visitedCaves:
                         lastCave.remove(lastCave[i])
             for i in range(len(lastCave)):
                 if int(lastCave[i][0]) > int(curcave['cNum'][0]):
                     passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Down'])
                 elif int(lastCave[i][0]) < int(curcave['cNum'][0]):
                     passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Up'])
                 else:
                     if int(lastCave[i][2]) > int(curcave['cNum'][2]):
                         passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Right'])
                     elif int(lastCave[i][2]) < int(curcave['cNum'][2]):
                         passivAct = chooseRotation(alldirsN[IAdir], alldirsN['Left'])
         else:
             if curcave['cNum'] not in visitedCaves:
                 visitedCaves.append(curcave['cNum'])
             dirlist = list(dirs.keys())
             if backdir(IAdir) in dirlist:
                 dirlist.remove(backdir(IAdir))
             nextCave = ''
             for i in range(len(dirlist)):
                 nextCave = getNextCave(curcave['cNum'], dirlist[i])
                 if (nextCave not in visitedCaves):
                     print('Получили не посещенную пещеру', nextCave)
                     passivAct = chooseRotation(alldirsN[IAdir], alldirsN[dirlist[i]])
                     break
             if passivAct == 'noAct':
                 dirlist = list(dirs.keys())
                 if backdir(IAdir) in dirlist:
                     dirlist.remove(backdir(IAdir))
                 for i in range(len(dirlist)):
                     nextCave = getNextCave(curcave['cNum'], dirlist[i])
                     if (nextCave not in windCaves):
                         passivAct = chooseRotation(alldirsN[IAdir], alldirsN[dirlist[i]])
         if passivAct == 'noAct':
             dirlist = list(dirs.keys())
             if backdir(IAdir) in dirlist:
                 dirlist.remove(backdir(IAdir))
             randdir = random.randint(0, len(dirlist) - 1)
             passivAct = chooseRotation(alldirsN[IAdir], alldirsN[dirlist[randdir]])
         activAct = 'Go'
  print("-- lastAct=", lastMove, " curPos:", curcave['cNum'])
  print(" choosenAct:", passivAct, activAct)
  return([passivAct, activAct])

def makeAllCavesList(allCaves):
    for i in range(0, 4):
        for j in range(0, 4):
            allCaves.append(str(i) + '_' + str(j))
# делаем игру - организуем взаимодействие с сервером
def chooseAndAct(case_id, user_id, mapnum) :
  # запуск игры:
  passivAct = 'noAct'
  activAct = 'noAct'
  request = connect(case_id, user_id, mapnum, passivAct = passivAct, activAct = activAct)
  allCaves = []
  windCaves = []
  makeAllCavesList(allCaves)
  visitedCaves = []
  # проверка успешности установки связи с сервером
  if(request == None) :
    print("Связь с сервером", url, "не установлена")
  else:
      # играем - выбираем ходы и передаем, пока игра не завершится
      lastAct = [passivAct, activAct]
      weKnowAboutWind = False
      windCaves = []
      while(request['error'] == None) :
        percept = request['text']
        act = chooseAct(percept, allCaves, visitedCaves, lastAct, windCaves)
        lastAct = act
        request = connect(case_id, user_id, mapnum, passivAct = act[0], activAct = act[1])
  print("Код завершения: ", request['error'])
  for i in range(len(visitedCaves)):
      print(visitedCaves[i])
  print('len = ', len(visitedCaves))
  return(request['error'])


# Запуск работы агента. Если все хорошо, то будет выдано сообщение "GAME IS REACHED"
chooseAndAct(case_id, user_id, mapnum)
