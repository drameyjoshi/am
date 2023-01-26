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

def normalise(priority: List[int]) -> List[int]:
    freq = {}
    for p in priority:
        if p in freq:
            freq[p] += 1
        else:
            freq[p] = 1

    normalised_priority = []
    for i in range(len(priority)):
        normalised_priority.append(priority[i]/freq[priority[i]])

    return normalised_priority

normalised_priority = normalise(priority)
total_priority = [x[a] * normalised_priority[a] for a in range(n_cleaning_areas)]
model.Maximize(sum(total_priority) + sum(x))

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f'Total time = {solver.ObjectiveValue()}')
    for a in range(n_cleaning_areas):
        if solver.BooleanValue(x[a]):
            print(f'Cleaning area {a} with priority {priority[a]} and time to clean {time_to_clean[a]} chosen.')
else:
    print('No solution found.')
    

