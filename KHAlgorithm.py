import itertools
import copy

class KHSystem(object):
    def __init__(self,playerPrefs):
        #initializes self.active to dict with playerPrefs and the sum of players' prefs
        self.active = dict()
        for player in playerPrefs: self.active[player] = [playerPrefs[player],dictSum(playerPrefs[player])]
        self.withdrawn = dict()

    def algorithm(self):
        #loops thisRound
        while not self.allAllocated():
            while self.thisRound(0):
                if not self.allAllocated(): self.thisRound(0)
            if not self.allAllocated(): self.thisRound(1)

    def allAllocated(self):
        #checks if all items and players have been allocated
        if self.active == dict(): return True
        firstPlayer = [x for x in self.active][0]
        if self.active[firstPlayer][0] == dict(): return True
        return False

    def thisRound(self,type):
        #one round of allocation
        #type is 0 for GP, 1 for SP
        possibleAllocations = dict()
        for player in self.active: possibleAllocations[player] = self.getAllocations(type,player)
        for i in range(dictLenMax(possibleAllocations)):
            for player in self.active:
                if len(possibleAllocations[player]) > i:
                    if self.isPluriacceptable(player,possibleAllocations[player][i],type):
                        self.withdraw(player,possibleAllocations[player][i])
                        return True
        return False

    def getAllocations(self,type,player):
        #gets allocations for player, GP or SP
        if type == 0: return self.getGP(player)
        if type == 1: return self.getSP(player)

    def getGP(self,player):
        #returns GP items for oen player
        #|V_i(A_i)| >= |V_i(A_a)|/p
        targetVal = self.active[player][1]/len(self.active)
        #all items, all values sorted in descending order
        itemsWithVals = self.allocationBasics(player)
        (allGP,i) = ([],0)
        while i < len(itemsWithVals) and itemsWithVals[i][1] >= targetVal:
            allGP += [{itemsWithVals[i][0]}]
            i += 1
        return allGP


    def getSP(self,player):
        #returns SP bundles for a player
        #|V_i(A_a)|/p >= |V_i(A_i)| >= |V_i(A_a)|/p - min(V_i(A_a - A_i))
        targetVal = self.active[player][1]/len(self.active)
        #all items, all values sorted in descending order
        itemsWithVals = self.allocationBasics(player)
        #Generates all possible combinations
        myCombos = []
        for i in range(1,len(itemsWithVals)+1):
            myCombos += list(itertools.combinations(itemsWithVals,i))
        #trims combinations
        j = 0
        while j < len(myCombos):
            mySum = sum([item[1] for item in myCombos[j]])
            outVals = [item[1] for item in itemsWithVals if item not in myCombos[j]]
            if outVals == []: smallestVal = 0
            else: smallestVal = min(outVals)
            if mySum > targetVal or (mySum <= (targetVal - smallestVal) and smallestVal != 0):
                myCombos.pop(j)
            else: j+= 1
        #converts format of combos to final format
        finalCombos = []
        for combo in myCombos:
            finalCombos += [set()]
            for item in combo: finalCombos[-1] |= {item[0]}
        return finalCombos

    def allocationBasics(self,player):
        #common vals to SP and GP allocations (items with vals)
        allItems = sorted([x for x in self.active[player][0]],key=lambda y:self.active[player][0][y])
        allValues = sorted([self.active[player][0][x] for x in self.active[player][0]])
        itemsWithVals = [(allItems[x],allValues[x]) for x in range(len(allItems))]
        itemsWithVals.reverse()
        return itemsWithVals

    def meetsConditions(self,player,bundle):
        #checks if meets conditions for SP acceptability
        targetVal = self.active[player][1]/(len(self.active)-1)
        values = [self.active[player][0][item] for item in bundle]
        if targetVal >= sum(actualVal) > targetVal - min(actualVal): return True
        return False

    def isPluriacceptable(self,player,bundle,type):
        #checks if SP/GP allocation acceptable forall players
        #only needs to check active players if SP
        # (if only one item, guaranteed acceptable for active players
        if type == 1:
            for other in self.active:
                if player != other:
                    if not self.isAA(other,bundle): return False
        for other in self.withdrawn:
            if player != other:
                if not self.isAW(other,bundle): return False
        return True

    def isAcceptable(self,concerned,target,bundle):
        #sorts into active and withdrawn acceptabilities
        if concerned in self.active: return isAA(target,bundle)
        else: return isAW(target,bundle)

    def isAA(self,player,bundle):
        #returns if is acceptable for an active player
        if len(bundle) == 1: return True
        targetVal = self.active[player][1]/(len(self.active)-1)
        actualVal = sum([self.active[player][0][item] for item in bundle])
        if targetVal >= actualVal: return True
        return False

    def isAW(self,player,bundle):
        #returns if is acceptable for a withdrawn player
        #|V_i(A_i)| >= |V_i(A_j)| - min(V_i(A_j)) and |V_i(A_i)| >= |V_i(A_a - A_j)|/(p-1) - min(V_i(A_a - A_j))
        inVals = [self.withdrawn[player][0][item] for item in bundle]
        outVals = [self.withdrawn[player][0][item] for item in self.withdrawn[player][0] if item not in bundle]
        myVal = self.withdrawn[player][2]
        if inVals == []: smallestInVal = 0
        else: smallestInVal = min(inVals)
        if outVals == []: smallestOutVal = 0
        else: smallestOutVal = min(outVals)
        #shortcuts to avoid /0 error
        if len(self.active) == 1:
            if outVals == []: return True
            else: return False
        if myVal >= sum(inVals)-smallestInVal and myVal >= (sum(outVals)/(len(self.active)-1))-smallestOutVal:
            return True
        return False

    def withdraw(self,player,bundle):
        #withdraws player and allocates bundle
        #takes both player and items in bundle out of game
        myVal = 0
        for pDict in [self.active,self.withdrawn]:
            for thisPlayer in pDict:
                if thisPlayer == player:
                    for item in bundle:
                        myVal += pDict[thisPlayer][0][item]
                        pDict[thisPlayer][1] -= pDict[thisPlayer][0][item]
                        pDict[thisPlayer][0].pop(item)
                else:
                    for item in bundle:
                        pDict[thisPlayer][1] -= pDict[thisPlayer][0][item]
                        pDict[thisPlayer][0].pop(item)
        self.withdrawn[player] = self.active[player]+[myVal]+[bundle]
        self.active.pop(player)

def dictSum(thisDict):
    #sums vals in a dict
    return sum([thisDict[x] for x in thisDict])

def dictLenMax(thisDict):
    #returns max len of a subdictionary in a dict of dicts
    dictLens = [len(thisDict[x]) for x in thisDict]
    if dictLens == []: return 0
    else: return max(dictLens)