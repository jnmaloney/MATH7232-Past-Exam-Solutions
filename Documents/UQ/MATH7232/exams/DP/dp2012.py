

revenue = [[0, 7, 8, 9, 11],
           [0, 6, 10, 12, 14],
           [0, 7, 8, 13, 15],
           [0, 4, 9, 12, 16]]


r = range(4)

dynamicSolution = {}

def cost(state):
    profit = 0
    for i in r:
        j = state[i]
        profit += revenue[i][j]

    return profit

def hsh(state):
    return sum(state[i] * 10**i for i in r)

def solve(stage, state):

    fullState = state
    state = hsh(state)

    if (stage, state) not in dynamicSolution:
    
        # Stopping condition
        if (stage == -1):
            dynamicSolution[stage, state] = (cost(fullState), 0)
        
        # Prepare the next stage solution
        else:
            actionCosts = []
            newStage = stage - 1
            for i in r:
                newState = [fullState[j] + 1 if i == j else fullState[j] for j in r]
                
                if any(t > 4 for t in newState): continue
                
                actionCost = solve(newStage, newState)[0]
                actionCosts.append((actionCost, newState))

            dynamicSolution[stage, state] = max(actionCosts)
            
    return dynamicSolution[stage, state]





state0 = 5
stage0 = [0, 0, 0, 0]

solve(state0, stage0)

# Output
stage = stage0
for i in range(state0, -1, -1):
    Y = dynamicSolution[i, hsh(stage)]
    stage = Y[1]
    print i+1, Y
