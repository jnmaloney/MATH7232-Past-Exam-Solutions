


demand = [20, 20, 30, 30, 20, 10]
r = range(0, 60, 10)
dynamicState = {}



def orderCost(n): return 0 if n == 0 else 20 + 2 * n


def storageCost(n): return 0.1 * n


def solve(stage, state):

    if (stage, state) in dynamicState: return dynamicState[stage, state]

    if (stage == 0):
        dynamicState[stage, state] = (20, 0)#'end of time')
        return dynamicState[stage, state]

    listOfActionCosts = []
    for i in r:
        c = orderCost(i)
        newState = state + i - demand[stage]
        if newState < 0: continue
        if newState > 40: newState = 40
        s = storageCost(newState)
        listOfActionCosts.append((s+c+solve(stage-1,newState)[1], i))

    m = min(listOfActionCosts)

    dynamicState[stage, state] = (m[1], m[0])
    return dynamicState[stage, state]


# Do it
R0 = 0

solve(5, R0)


# Output
for year in range(5, -1, -1):
    #i = 5 - year
    i = year
    Y = dynamicState[i, R0]
    A = Y[0]
    R0 += A - demand[year]
    print i+1, R0, A
    

