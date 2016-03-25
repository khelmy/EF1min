import KHAlgorithm as kh
import random
import time

def generatePrefs(numPlayers,numItems):
    #generates random preferences when specified #players, #items
    playerPrefs = dict()
    for i in range(numPlayers):
        myPrefs = list()
        for j in range(numItems):
            myPrefs += [random.randint(1,100)]
        #rescales preferences according to 100 point scale
        mySum = sum(myPrefs)
        scaledPrefs = [x*(100/mySum) for x in myPrefs]
        #adjusts to dict data type
        playerPrefs[i] = dict()
        for k in range(len(scaledPrefs)):
            playerPrefs[i][k] = scaledPrefs[k]
        playerPrefs = roundPrefs(numItems,playerPrefs)
    return playerPrefs

def roundPrefs(numItems,playerPrefs):
    #rounds preferences to ints, randomly makes up for error
    for player in playerPrefs:
        for item in playerPrefs[player]:
            playerPrefs[player][item] = int(round(playerPrefs[player][item]))
        while kh.dictSum(playerPrefs[player]) > 100:
            decreaseThis = random.randint(0,numItems-1)
            if playerPrefs[player][decreaseThis] > 1: playerPrefs[player][decreaseThis] -= 1
        while kh.dictSum(playerPrefs[player]) < 100:
            increaseThis = random.randint(0,numItems-1)
            playerPrefs[player][increaseThis] += 1
    return playerPrefs

preferences = generatePrefs(4,7)
t1 = time.time()
thisAlg = kh.KHSystem(preferences)
print("Time: start", ", Active:",thisAlg.active,", Withdrawn:",thisAlg.withdrawn)
thisAlg.algorithm()
t2 = time.time()
print("Time: end", ", Active:",thisAlg.active,", Withdrawn:",thisAlg.withdrawn, ", Time elapsed:",t2-t1)

##INTERESTING CASES
#preferences = {1:{1:50,2:40,3:10}, 2:{1:40,2:10,3:50}}
#preferences = {1:{1:10,2:30,3:40,4:20},2:{1:50,2:10,3:30,4:10},3:{1:20,2:30,3:40,4:10}}
#preferences = {0: {0: 25, 1: 39, 2: 16, 3: 20}, 1: {0: 13, 1: 18, 2: 39, 3: 30}, 2: {0: 32, 1: 17, 2: 23, 3: 28}}
#preferences = {0: {0: 1, 1: 37, 2: 9, 3: 20, 4: 33},1: {0: 25, 1: 24, 2: 23, 3: 25, 4: 3},2: {0: 23, 1: 18, 2: 2, 3: 43, 4: 14}}