#!/usr/bin/env python

'''
Script to optimize room matching for n people.

Inputs: A table of how happy each person would be (on a scale of 1-10) to get
    each room. Rows correspond to people, and columns correspond to rooms.
Outputs: Optimal room assignments for person i getting room j.
'''

import numpy as np
from pulp import *

# load in data from csv: each row is a person, each column is a room
# on a scale from 1-10, how happy would you be if you got this room?
data = np.genfromtxt("happiness.csv", delimiter=',', dtype=None)
people = data[1:,0]
rooms = data[0,1:]
happiness = data[1:,1:].astype(np.int)

# number of rooms/people
n = len(rooms)

# set up the problem
prob = LpProblem("Room Matching",LpMaximize)

# initialize table of variables
xs = [[0 for i in range(n)] for i in range(n)]

# initialize objective
objective = 0

# define variables: indicator variable for person i being assigned room j
for i in range(n):
    for j in range(n):
        xs[i][j]=LpVariable(people[i]+' '+rooms[j],0,1,LpInteger)
        objective += happiness[i][j]*xs[i][j]

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

# print average happiness
print "Average happiness = " + str(value(prob.objective) / n)