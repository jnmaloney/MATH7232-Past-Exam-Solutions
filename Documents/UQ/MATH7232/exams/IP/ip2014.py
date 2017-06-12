

# ---------------------
# Words.py
# ---------------------


from gurobipy import *
import random
import math

L = range(26)
alphabet = "abcdefghijklmnopqrstuvwxyz"

# Calculates the number of time each letter appears in a word
# and returns it as a list
def wordletters (w):
    letters = [0 for j in L]
    for c in w:
        k = alphabet.index(c)
        if (k >= 0) and (k < 26):
            letters[k] += 1
    return letters

# word frequencies from http://www.wordfrequency.info
# Read in the file and store in in words
# words[w][0] is the word and words[w][1] is the frequency
wordsfile = open('freqs.txt', 'r')
words = [w.strip().split(',') for w in wordsfile]

# Letter data stores the number of times each letter appears in each word
letterdata = [wordletters(w[0]) for w in words]
# V stores the score of each word, based on a scaled frequency
v = [int(math.log(int(w[1]))+1) for w in words]

W = range(len(letterdata))

random.seed(3)
# N is randomly generated data for letter distributions
N = [random.randint(20,50) for l in L]

# Number of blanks
NBlanks = 50



# ---------------------
# Data
# ---------------------


# ---------------------
# Model
# ---------------------
model = Model()


# ---------------------
# Variables
# ---------------------

# Products to make
X = [model.addVar(vtype = GRB.INTEGER) for i in L]
Y = [model.addVar(vtype = GRB.INTEGER) for j in W]



# ---------------------
# Objective
# ---------------------

total_points = quicksum(Y[j] * v[j] for j in W)
model.setObjective(total_points, GRB.MAXIMIZE)


# ---------------------
# Constraints
# ---------------------

# for each letter
# (Y) words used * letters in word = (X) number of tiles available
for i in L:
    model.addConstr(quicksum(Y[j] * letterdata[j][i] for j in W) <= X[i] + N[i])


for j in W: model.addConstr(Y[j] <= 1)

# (X) Only 50 blanks
model.addConstr(quicksum(X[i] for i in L) <= 50)


# ---------------------

model.optimize()

print "Score: {:,d}".format(int(model.ObjVal))

for i in L:
    print int(X[i].x)

for j in W:
    if Y[j].x:
        print j, words[j][0]

print '\n'

