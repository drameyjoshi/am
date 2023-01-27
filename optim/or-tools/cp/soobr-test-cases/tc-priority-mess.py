import common_functions

import numpy as np

from typing import List
from ortools.sat.python import cp_model

time_to_clean = [70, 70, 140]
priority = [50, 50, 80]

tour_max_duration = [140]
n_tour = 1
n_cleaning_areas = len(time_to_clean)

assert(n_cleaning_areas == len(priority))
model = cp_model.CpModel()
# Decision variables
x = []
for a in range(n_cleaning_areas):
    x.append(model.NewBoolVar(f'x[{a}]'))

# Total time to clean should not exceed tour max duration.
time = [x[a] * time_to_clean[a] for a in range(n_cleaning_areas)]
model.AddLinearConstraint(sum(time), 0, tour_max_duration[0])

normalised_priority = common_functions.normalise(priority)
total_priority = [x[a] * normalised_priority[a] for a in range(n_cleaning_areas)]
model.Maximize(sum(total_priority) + sum(x))
model.ExportToFile('testPriorityMess.txt')

solver = cp_model.CpSolver()
status = solver.Solve(model)

found = common_functions.report_status(status)

if found:
    print(f'Total time = {solver.ObjectiveValue()}')
    for a in range(n_cleaning_areas):
        if solver.BooleanValue(x[a]):
            print(f'Cleaning area {a} with priority {priority[a]} and time to clean {time_to_clean[a]} chosen.')
else:
    print('No solution found.')
    

