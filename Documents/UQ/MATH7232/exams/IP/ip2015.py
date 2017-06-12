

# ---------------------
# Question1.py
# ---------------------


from gurobipy import *
import random

# 100 candidate sites
S = range(100)
G = range(30)
random.seed(20)

# Drill cost at each site
DrillCost = [random.randint(15000,60000) for s in S]

# 30 groups with between 5 and 10 elements in every group
Group = [sorted(random.sample(S, random.randint(5,10))) for i in G]
print Group


# ---------------------
# Data
# ---------------------
n = 20
pen = 10000


# ---------------------
# Model
# ---------------------
model = Model()


# ---------------------
# Variables
# ---------------------

# Drill sites
X = [model.addVar(vtype = GRB.INTEGER) for i in S]

# Groups with two sites
Y = [model.addVar(vtype = GRB.INTEGER) for j in G]



# ---------------------
# Objective
# ---------------------

site_cost = quicksum(X[i] * DrillCost[i] for i in S)
penalty_cost = quicksum(pen * Y[j] for j in G)
total_cost = site_cost + penalty_cost
model.setObjective(total_cost, GRB.MINIMIZE)


# ---------------------
# Constraints
# ---------------------
for j in G:
    # Max dupes
    model.addConstr(Y[j] <= 1)
    
    # Force dupes
    model.addConstr(Y[j] >= quicksum(X[i] for i in Group[j]) - 1)

# Must have 20 drill sites
model.addConstr(quicksum(X[i] for i in S) == n)

for i in S: model.addConstr(X[i] <= 1)

# ---------------------

model.optimize()

print "Cost: ${:,d}".format(int(model.ObjVal))

for i in S:
    if X[i].x:
        print i,

print

for j in G:
    if Y[j].x:
        print 'group', [i for i in Group[j]]

print '\n'

