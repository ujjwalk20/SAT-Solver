import sys
import random

#importing and storing cnf formula in an array called clauses
import csv
with open ('./test/uf150-02.cnf',"r") as cnf:
    cnf1=csv.reader(cnf)
    clauses=[]
    for line in cnf.readlines():
        if line[0]=='c':
            continue
        if line[0]=='p':
            nvars,nclauses=line.split()[2:4]
            continue
        clause=[int(x) for x in line[:-2].split()]
        clauses.append(clause)
    
#print (clauses)


#used to reduce the formula after assignment
def bcp(formula, unit):
    modified = []
    for clause in formula:
        if unit in clause:
            continue
        if -unit in clause:
            new_clause = [x for x in clause if x != -unit]
            if not new_clause:
                return -1
            modified.append(new_clause)
        else:
            modified.append(clause)
    return modified


#used to count the number of literals
def get_counter(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return counter


#used for unit propagation
def unit_propagation(formula):
    assignment = []
    unit_clauses = [c for c in formula if len(c) == 1]
    while unit_clauses:
        unit = unit_clauses[0]
        formula = bcp(formula, unit[0])
        assignment += [unit[0]]
        if formula == -1:
            return -1, []
        if not formula:
            return formula, assignment
        unit_clauses = [c for c in formula if len(c) == 1]
    return formula, assignment


#backtracking
def backtracking(formula, assignment, heuristic):
    formula, unit_assignment = unit_propagation(formula)
    assignment = assignment + unit_assignment
    if formula == - 1:
        return []
    if not formula:
        return assignment

    variable = heuristic(formula)
    solution = backtracking(bcp(formula, variable), assignment + [variable], heuristic)
    if not solution:
        solution = backtracking(bcp(formula, -variable), assignment + [-variable], heuristic)

    return solution


#returns max occuring literal
def most_often(formula):
    counter = get_counter(formula)
    return max(counter, key=counter.get)


#finding solution and printing
solution = backtracking(clauses, [], most_often)
#print(solution)
if solution:
    solution += [x for x in range(1, int(nvars) + 1) if x not in solution and -x not in solution]
    solution.sort(key=lambda x: abs(x))
    print ('SATISFIABLE')
#    print(solution)
    solution1=[]
    for literal in solution:
        if literal in solution1:
            continue
        solution1.append(literal)
    print(solution1)        
else:
    print ('UNSATISFIABLE')