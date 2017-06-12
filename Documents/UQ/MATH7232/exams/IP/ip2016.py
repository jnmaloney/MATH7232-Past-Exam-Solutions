

# ---------------------
# Question1.py
# ---------------------


from gurobipy import *
import random

# Data and ranges
nHospitalSites = 30
nSuburbs = 55
MaxSuburbsPerHospital = 7
MaxPopulation = 500000

H = range(nHospitalSites)
S = range(nSuburbs)

random.seed(3)

FixedCost = [random.randint(5000000,10000000) for h in H]
Population = [random.randint(60000,90000) for s in S]

# Travel distance - multiply by population moved to get travel cost
Dist = [[random.randint(0,50) for s in S] for h in H]



# ---------------------
# Data
# ---------------------


# ---------------------
# Model
# ---------------------
model = Model()
model.setParam('MIPGap', 0)


# ---------------------
# Variables
# ---------------------


X = { (i, j): model.addVar(vtype = GRB.INTEGER, ub = 1) for i in H for j in S }



# ---------------------
# Objective
# ---------------------

total_cost = quicksum(X[i, j] * (FixedCost[i] + Population[j] * Dist[i][j]) for i in H for j in S)
model.setObjective(total_cost, GRB.MINIMIZE)


# ---------------------
# Constraints
# ---------------------

# Hospital capacities
for i in H:
    model.addConstr(quicksum(X[i, j] for j in S) <= MaxSuburbsPerHospital)
    model.addConstr(quicksum(X[i, j] * Population[j] for j in S) <= MaxPopulation)

# Every suburb serviced
for j in S:
    model.addConstr(quicksum(X[i, j] for i in H) == 1)

# ---------------------

model.optimize()

print
print "Cost: ${:,d}".format(int(model.ObjVal))

for i in H:
    if sum(X[i, j].x for j in S) == 0: continue
    print "Site", i, "services suburbs",
    for j in S:
        if X[i, j].x: print "{0},".format(j),
    print


