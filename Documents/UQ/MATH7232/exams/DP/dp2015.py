

OperatorsRequired = [155, 120, 140, 100, 155]


# n: number
# i: season
def seasonCost(n, i): return 2000 * (n - OperatorsRequired[i])


# delta: change in empoyment
def hiringCost(delta): return 200 * delta**2

# Dynamic State
# D_[Stage, State] = (Action, UltimateCost)
dynamicState = {}
r = range(-55, 55)

# Dynamic Program
# return (Action, UltimateCost)
def solve(seasonsRemaining, employees):

    #i = 5 - seasonsRemaining
    i = seasonsRemaining
       
    # Memo
    if (i, employees) in dynamicState:
        return dynamicState[i, employees]
    
    # End of sim
    if seasonsRemaining == 5:
        dynamicState[i, employees] = (0, 'outoftime')
        return dynamicState[i, employees]
    
    # Otherwise do the calc
    # blah[]: (UltimateCost, Action)
    blah = []
    for j in r:
        
        # Hiring/Firing
        action = j
    
        newEmployment = employees + action
        cost = seasonCost(newEmployment, i) + hiringCost(action)

        # constraint
        #if (newEmployment < OperatorsRequired[i]): continue
        if (employees < OperatorsRequired[i]): continue

        # recursion
        s = solve(seasonsRemaining + 1, newEmployment)
        if isinstance(s[1], (int, long)):
            blah.append((cost + s[1], action))

        elif (s[1] == 'outoftime'):
            blah.append((cost, action))

    # ?
    if len(blah) == 0:
        dynamicState[i, employees] = (0, 'nosolution')
        return dynamicState[i, employees]


    x = min(blah)
    dynamicState[i, employees] = (x[1], x[0])
    return dynamicState[i, employees]



# Do it
solve(0, 155)


# Output
R0 = 155
for year in range(5):
    #i = 5 - year
    i = year
    Y = dynamicState[i, R0]
    A = Y[0]
    print i+1, R0, A

    #if (A == 'outoftime'): break
    if isinstance(A, (int, long)):
        R0 += A

