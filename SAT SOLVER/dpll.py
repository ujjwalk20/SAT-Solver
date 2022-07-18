import sys
import random

#importing and storing cnf formula in an array called clauses
import csv
with open ('./test/uf20-02.cnf',"r") as cnf:
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
def bcp (formula, unit):
    modified=[]
    for clause in formula:
        if unit in clause:
            continue
        if -unit in clause:
            c=[x for x in clause if x!=-unit]
            if len(c)==0:
                return -1
            modified.append(c)
        else:
            modified.append(clause)
    return modified

#used to count the number of literals
def get_counter (formula):
    counter={}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return counter

#used to remove pure literals
def pure_literal (formula):
    counter=get_counter(formula)
    assignment=[]
    pures=[]
    for literal, times in counter.items():
        if -literal not in counter:
            pures.append(literal)
        for pure in pures:
            formula = bcp (formula,pure)
        assignment += pures
    return formula, assignment

#used for unit propagation
def unit_propagation(formula):
    assignment = []
    unit_clauses = [c for c in formula if len(c) == 1]
    while len(unit_clauses) > 0:
        unit = unit_clauses[0]
        formula = bcp(formula, unit[0])
        assignment += [unit[0]]
        if formula == -1:
            return -1, []
        if not formula:
            return formula, assignment
        unit_clauses = [c for c in formula if len(c) == 1]
    return formula, assignment

#selecting a random variable
def variable_selection(formula):
    counter = list(get_counter(formula))
    return random.choice(counter)

#backtracking
def backtracking(formula, assignment):
    formula, pure_assignment = pure_literal(formula)
    formula, unit_assignment = unit_propagation(formula)
    assignment = assignment + pure_assignment + unit_assignment
    if formula == - 1:
        return []
    if not formula:
        return assignment

    variable = variable_selection(formula)
    solution = backtracking(bcp(formula, variable), assignment + [variable])
    if not solution:
        solution = backtracking(bcp(formula, -variable), assignment + [-variable])
    return solution

#finding solution and printing
solution = backtracking(clauses, [])
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
