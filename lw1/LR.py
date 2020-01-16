counterFives = 0
counter = 0
for i in range(1000000):
    currNum = i
    strNum = str(currNum)
    lenStr = len(strNum)
    for j in range(lenStr):
        if strNum[j] == '5':
            counterFives += 1
        if counterFives > 2:
            counterFives = 0
    if counterFives == 2:
        print(currNum)
        counter += 1
    counterFives = 0
print('--98415-- ',counter)
#
# import math
#
# M0 = 4 * math.pi * 10**-7
# N1 = 450
# N2 = 75
# R1 = 533
# R2 = 42.9
# C  = 0.38 * 10**-6
# Lmid = 115.55 * 10**-3
# S = 82.85 * 10**-6
# Freq = 650
#
# # input!!!
# listI = [0, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 32, 36, 40]
# listU = [0, 1, 4, 7, 11, 16, 20, 32, 41, 53, 63, 72, 79, 85, 108, 123, 132, 138, 139, 143, 146]
# # --------
#
# H0mid = N1 * math.sqrt(2) / Lmid
# listH0 = []
# for i in range(21):
#     listH0.append(H0mid * listI[i])
#
#
# Bmid = R2 * C * math.sqrt(2) / (N2 * S)
# listB = []
# for i in range(21):
#     listB.append(Bmid * listU[i])
#
#
# listM = []
# listM.append(-1) #infinity
#
# for i in range(1, 21):
#     listM.append(listB[i] / (M0 * listH0[i]))
#
#
# for i in range(21):
#     print(round( listI[i], 2 ), end = '  ', )
#
# print('\n')
#
# for i in range(21):
#     print(round( listU[i], 2 ), end = '  ', )
#
# print('\n')
#
# for i in range(21):
#     print(round( listH0[i], 2 ), end = '  ', )
#
# print('\n')
#
# for i in range(21):
#     print(round( listB[i], 2 ), end = '  ', )
#
# print('\n')
#
# for i in range(21):
#     print(round( listM[i], 2 ), end = '  ', )