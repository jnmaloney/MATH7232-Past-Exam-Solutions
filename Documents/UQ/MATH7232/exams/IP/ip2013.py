
# ---------------------
# Data
# ---------------------

products = range(6)
reach = [1000, 200, 300, 400, 450, 450]
cost = [500, 150, 300, 250, 250, 100]
des = [700, 250, 200, 200, 300, 400]
sales = [2, 1, 1, 1, 1, 10]

cost_available = 1400
des_available = 1500
sales_available = 12

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



# ---------------------
# Objective
# ---------------------

total_reach = quicksum(X[i] * reach[i] for i in products)
model.setObjective(total_reach, GRB.MAXIMIZE)


# ---------------------
# Constraints
# ---------------------

# Cost($)
model.addConstr(quicksum(X[i] * cost[i] for i in products) <= cost_available)

# Designer hours
model.addConstr(quicksum(X[i] * des[i] for i in products) <= des_available)

# Sales hours
model.addConstr(quicksum(X[i] * sales[i] for i in products) <= sales_available)

#
model.addConstr(X[5] <= X[3] + X[4])

#
model.addConstr(X[1] + X[4] <= 1)

for i in products: model.addConstr(X[i] <= 1)

# ---------------------

model.optimize()

print "Campaign audience: {:,d},000 reached.".format(int(model.ObjVal))

for i in products:
    print int(X[i].x),
print '\n'

