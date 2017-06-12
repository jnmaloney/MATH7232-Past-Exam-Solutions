
# ---------------------
# Data
# ---------------------


products = range(4)
profit = [10, 15, 22, 17]
max_demand = [50, 60, 85, 70]

stages = range(3)
stage_name = 'ABC'
stage_cost = [[2, 2, 1, 1],
              [2, 4, 1, 2],
              [3, 6, 1, 5]]

stage_pool = [160, 200, 80]

max_days = 5;

# ---------------------
# Model
# ---------------------
from gurobipy import *
model = Model()


# ---------------------
# Variables
# ---------------------

# Products to make
X = [model.addVar(vtype = GRB.INTEGER) for i in products]

# Days to shift
Y = [model.addVar(vtype = GRB.INTEGER) for j in stages]


# ---------------------
# Objective
# ---------------------

weekly_profit = quicksum(X[i] * profit[i] for i in products)
model.setObjective(weekly_profit, GRB.MAXIMIZE)


# ---------------------
# Constraints
# ---------------------

# Less than max demand
for i in products:
    model.addConstr(X[i] <= max_demand[i])

# Hours are used up
#for j in stages:
#    model.addConstr(quicksum(X[i] * stage_cost[j][i] for i in products) <= stage_pool[j] + 8 * Y[j])

model.addConstr(quicksum(X[i] * stage_cost[0][i] for i in products) <= stage_pool[0] + 8 * Y[0])
model.addConstr(quicksum(X[i] * stage_cost[1][i] for i in products) <= stage_pool[1] - 8 * Y[1])
model.addConstr(quicksum(X[i] * stage_cost[2][i] for i in products) <= stage_pool[2] + 8 * Y[2])

# Days moved conservation
#model.addConstr(quicksum(Y[j] for j in stages) == 0)
model.addConstr(Y[0] - Y[1] + Y[2] == 0)

# Days moved limits
model.addConstr(Y[0] >= 0)
model.addConstr(Y[0] <= max_days)

model.addConstr(Y[1] >= 0)
model.addConstr(Y[1] <= max_days)

model.addConstr(Y[2] >= 0)
model.addConstr(Y[2] <= max_days)


# ---------------------

model.optimize()

print "$", model.ObjVal

for i in products:
    print X[i].x,
print '\n'

for j in stages:
    print stage_name[j], Y[j].x
