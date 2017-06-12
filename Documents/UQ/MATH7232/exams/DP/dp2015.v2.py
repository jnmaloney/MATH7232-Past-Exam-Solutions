

operators = [155, 120, 140, 100, 155]
overCost = 2000

r = range(-50, 60)

dynamicSolution = {}

def cost(stage, state, delta):
    a = 0 if state <= operators[stage] else overCost * (state - operators[stage])
    b = 200 * delta**2
    return a + b

def solve(stage, state):
    
    if (stage, state) not in dynamicSolution:
        
        # Stopping condition
        if (stage == -1):
            dynamicSolution[stage, state] = (0, 0)
    
        # Prepare the next stage solution
        else:
            actionCosts = []
            newStage = stage - 1
            for i in r:
                newState = state + i
                
                if newState < operators[stage]: continue
                
                actionCost = cost(stage, newState, i) + solve(newStage, newState)[0]
                actionCosts.append((actionCost, newState))
            
            dynamicSolution[stage, state] = min(actionCosts)

    return dynamicSolution[stage, state]





state0 = 4
stage0 = 155

solve(state0, stage0)

# Output
stage = stage0
for i in range(state0, -1, -1):
    Y = dynamicSolution[i, stage]
    stage = Y[1]
    print i+1, Y
