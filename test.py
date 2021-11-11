#!/usr/bin/env python
# @(#) $Jeannot: test2.py,v 1.16 2004/03/20 17:06:54 js Exp $

# This example is a PuLP rendition of the todd.mod problem included in the GLPK
# 4.4 distribution. It's a hard knapsack problem.
import pulp
# import pulp as pl
# solver_list = pl.listSolvers(onlyAvailable=True)
# print(solver_list)

# Import PuLP modeler functions
# from pulp import *

# Import math functions
from math import *

# A new LP problem
prob = pulp.LpProblem("test", pulp.LpMaximize)

# s1 = pulp.LpVariable("s1", 0, 1)
# s2 = LpVariable("s2", 0, 1)
# s3 = LpVariable("s3", 0, 1)
# z1 = LpVariable("z1", 0, 1)
# z2 = LpVariable("z2", 0, 1)

s = pulp.LpVariable.dicts(name="s", indexs=[i for i in range(1, 4)], lowBound=0, upBound=1, cat=pulp.LpContinuous)
z = pulp.LpVariable.dicts(name="z", indexs=[i for i in range(1, 3)], lowBound=0, upBound=1, cat=pulp.LpInteger)

formula = [[1, 2, 3], [1, -2, -3]]

# Objective
# prob += z[1] + z[2], "obj"
prob += pulp.lpSum(z)
# Constraint
for i, clause in enumerate(formula):
    prob += (pulp.lpSum([(1 - s[abs(lit)]) if lit > 0 else s[abs(lit)] for lit in clause]) <= 1+3*(1-z[i + 1]), f"clause_{i}")

# prob += 1-s[1]+1-s[2] <= 1+3*(1-z[1]), "c1"
# prob += s[1]+1-s[2]+s[3] <= 1+3*(1-z[2]), "c2"

# s[1].setInitialValue(0)
# s[1].fixValue()
# s[1].unfixValue()

# prob.writeLP("test1.lp")

# Resolution
solver = pulp.PULP_CBC_CMD(msg=False, threads=1)
# solver.tmpDir = "temp"

prob.solve(solver)

# Print the status of the solved LP
print("Status:", pulp.LpStatus[prob.status])

if prob.status == pulp.LpSolutionOptimal:
    # Print the value of the variables at the optimum
    for v in prob.variables():
        print(v.name, "=", v.varValue)

    # Print the value of the objective
    print("objective=", pulp.value(prob.objective))

    for i in z:
        print(z[i].name, "=", pulp.value(z[i]))
