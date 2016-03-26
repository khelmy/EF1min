##Generates an allocation that is envy-free to the smallest good, as well as providing a random-preference generator and a repeated random-preference tester. Allocations are generated according to the following algorithm:

###First, define 3 sets of inequalities:

Inequality 1:  |V_i(A_a)|/p >= |V_i(A_i)| >= |V_i(A_a)|/p - min(V_i(A_a - A_i))
     Where A_a is the set of currently allocatable items, including the ones being considered for A_i, and p is the number of active players.
  
Inequality 2: |V_i(A_i)| >= |V_i(A_a)|/p
     Where A_i consists of a single item.
     
Inequality 3: |V_i(A_i)| >= |V_i(A_j)| - min(V_i(A_j)) and |V_i(A_i)| >= |V_i(A_a - A_j)|/(p-1) - min(V_i(A_a - A_j))

###Then, define the following terms:
1. Sub-proportional (SP) bundle: a bundle of items satisfying inequality 1 for any given player.

2. Greater-than-proportional (GP) item: an item satisfying inequality 2 for any given player.

3. Withdrawn: a withdrawn player has been given an allocation, will be given no more items as a result of having received either an SP bundle or a GP item in a previous round.

4. Active: a player that is not withdrawn.

5. Acceptable (with regards to one's own allocation): an active player finds any GP or SP allocation acceptable for itself to receive.

6. Acceptable (with regards to another player's allocation): a withdrawn player finds any allocation satisfying inequality 3 to be acceptable for another player to receive; an active player finds any single item, SP allocation or subset thereof for another player to receive.

###Next, allocate items to players according to the following system:
1. Check if any players have any GP items. Iterate through the players who do, and within each player the items that are acceptable: choose the highest precedence (most valuable) GP item for any player that is considered acceptable by all withdrawn players, allocate it to said player, and withdraw the player.

2. If another GP allocation is possible, return to (1).

3. Formulate SP bundles for each player, checking if they are acceptable for all withdrawn and active players. Grant the highest-possible precedence SP bundle to whichever player is possible. When such an allocation is found, allocate it to the relevant player and withdraw the player.

4. If another GP allocation is possible, return to (1). Otherwise, if items remain, return to (3).
