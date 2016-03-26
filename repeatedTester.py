import KHAlgorithm as kh
import randomGenerator as rg
import time

def testForRange(startPlayers,endPlayers,startItems,endItems,numTrials):
    #tests for termination for a range of players,items
    #tests numTrials times
    #start <= n <= end
    #tests with randomly generated preferences
    if startPlayers == 0: startPlayers = 1
    for numPlayers in range(startPlayers,endPlayers+1):
        for numItems in range(startItems,endItems+1):
            for k in range(numTrials):
                preferences = rg.generatePrefs(numPlayers,numItems)
                t1 = time.time()
                thisAlg = kh.KHSystem(preferences)
                print("Time: start", ", Active:",thisAlg.active,
                      ", Withdrawn:",thisAlg.withdrawn)
                thisAlg.algorithm()
                t2 = time.time()
                print("Time: end", ", Active:",thisAlg.active,
                      ", Withdrawn:",thisAlg.withdrawn, ", Time elapsed:",t2-t1)

testForRange(2,5,3,7,3)
