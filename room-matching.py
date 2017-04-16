#!/usr/bin/env python

'''
Script to optimize room matching for n people.

Inputs: A table of how each person ranks each room. Rows correspond to people, 
    and columns correspond to rooms.
Outputs: Optimal room assignments for person i getting room j.
'''

import numpy as np
from pulp import *
import sys

# load in data from file: each row is a person, each column is a room
if (len(sys.argv) == 2):
    filename = sys.argv[1] # filename with the data
else:
    filename = "rankings.csv" # default file
# how would you rank each room from 1 to n?
data = np.genfromtxt(filename, delimiter=',', dtype=None)
people = data[1:,0]
rooms = data[0,1:]
rankings = data[1:,1:].astype(np.int)

# number of rooms/people
n = len(rooms)

# set up the problem
prob = LpProblem("Room Matching",LpMinimize)

# initialize table of variables
xs = [[0 for i in range(n)] for i in range(n)]

# initialize objective
objective = 0

# define variables: indicator variable for person i being assigned room j
for i in range(n):
    for j in range(n):
        xs[i][j]=LpVariable(people[i]+' '+rooms[j],0,1,LpInteger)
        objective += rankings[i][j]*xs[i][j]

# objective function
prob += objective

# constraints for each person getting 1 room, each room getting 1 person
for j in range(n):
    prob+=lpSum([xs[i][j] for i in range(n)])==1,"1 person per room "+str(i)+str(j)

for i in range(n):
    prob+=lpSum([xs[i][j] for j in range(n)])==1,"1 room per person "+str(i)+str(j)

# The problem data is written to an .lp file
prob.writeLP("room-matching.lp")

# solve the problem
prob.solve()

# The status of the solution is printed to the screen
print "Status: " + LpStatus[prob.status]

# print optimal room assignment
for v in prob.variables():
    if (v.varValue == 1):
        print v.name

# print average ranking
print "Average ranking = " + str(value(prob.objective) / n)
