from struct import *



chance = [0.80, 0.60, 0.90, 0.50]
points = [6, 4, 10, 7]
r = range(4)
dynamicState = {}


def solve1(stage, state):
    
    if (stage, state) in dynamicState: return dynamicState[stage, state]
    
    if (stage == 0):
        dynamicState[stage, state] = (0, 0)#'end of time')
        return dynamicState[stage, state]

        
    # Shoot an arrow
    newStage = stage - 1

    # Chance to hit
    cth0 = chance[state] * points[state] + solve(newStage, state)[1]

    cth1 = 0 if state == 0 else chance[state-1] * points[state-1] + solve(newStage, state - 1)[1]

    # move on or nah
    listOfActionCosts = [(cth0, state), (cth1, state-1)]
    #listOfActionCosts.append((s+c+solve(stage-1,newState)[1], i))
    
    m = max(listOfActionCosts)

    dynamicState[stage, state] = (m[1], m[0])
    return dynamicState[stage, state]


# score from shots
def costOf(shots):
    score = 0.0
    for i in r:
        hit = 1.0 - chance[i] ** shots[i]
        score += hit * points[i]

    return score


def hsh(l):
    return pack('iiii', l[0], l[1], l[2], l[3])

# stage - number of arrows
# state - shots per target
def solve(stage, state):


    if (stage, hsh(state)) in dynamicState: return dynamicState[stage, hsh(state)]
    
    if (stage == -1):
        dynamicState[stage, hsh(state)] = (costOf(state), 0)#'end of time')
        return dynamicState[stage, hsh(state)]

    listOfActionCosts = []
    for i in r:
        newStage = stage - 1
        newState = [(state[j] if j != i else state[j] + 1) for j in r]
        #actionCost = costOf(newState) + solve(newStage, newState)[0]
        actionCost = solve(newStage, newState)[0]
        listOfActionCosts.append((actionCost, newState))

    m = max(listOfActionCosts)

    dynamicState[stage, hsh(state)] = m
    return dynamicState[stage, hsh(state)]


# Do it
R0 = 3
R0 = [0, 0, 0, 0]

X = solve(9, R0)

print X

# Output
for year in range(9, -1, -1):
    #i = 5 - year
    i = year
    Y = dynamicState[i, hsh(R0)]
    A = Y[1]
    R0 = A
    print i+1, Y


