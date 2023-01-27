import common_functions

import math
import numpy as np

from typing import List
from ortools.sat.python import cp_model

# Input data. Relevant parameters chosen from 'testPriorityMessByCodeSharing.json'.
time_to_clean = [1, 1, 1, 1, 1, 1, 1, 1, 1]
n_cleaning_areas = len(time_to_clean)

priority = [n for n in range(1, n_cleaning_areas + 1)]
floor_id = [1, 1, 1, 1, 1, 2, 2, 2, 2]
floor_sort = [0, 0, 0, 0, 0, 1, 1, 1, 1]
building_id = n_cleaning_areas * [1]

tour_max_duration = [14, 14]

n_tours = len(tour_max_duration)

assert(n_cleaning_areas == len(priority))
assert(n_cleaning_areas == len(floor_id))
assert(n_cleaning_areas == len(floor_sort))
assert(n_cleaning_areas == len(building_id))

# Build the constraints.
model = cp_model.CpModel()
# Decision variables
x = {}
for t in range(n_tours):
    for c in range(n_cleaning_areas):
        x[(t, c)] = model.NewBoolVar(f'x[{t}, {c}]')

## Add constraints.
# Constraint 1: For any tour, time to clean <= tour max duration.
for t in range(n_tours):
    time = [x[(t, c)] * time_to_clean[c] for c in range(n_cleaning_areas)]
    model.AddLinearConstraint(sum(time), 0, tour_max_duration[t])

# Constraint 2: A cleaning area should be allocated to at most one tour.
for c in range(n_cleaning_areas):
    model.AddAtMostOne([x[(t, c)] for t in range(n_tours)])

# Constraint 3: Fair distribution across tours.
tour_allocs = []
for t in range(n_tours):
    tour_allocs.append(sum([x[t, c] for c in range(n_cleaning_areas)]))

lbound = math.floor(n_cleaning_areas/2)
ubound = n_cleaning_areas
for i in range(len(tour_allocs)):
    model.AddLinearConstraint(tour_allocs[i], lbound, ubound)
        

## Build objective function.
obj_list = []
    
uniq_buildings = set()
for b in building_id:
    uniq_buildings.add(b)

# Objective 1: For each tour, within a building, minimise floor change.
terms = []
floor_penalty = 0 # This will be a negative number.
for t in range(n_tours):        
    for ub in uniq_buildings:
        i = -1
        # Get indices of all floors in this building
        cleaning_areas_in_bldg = []
        for b_id in building_id:
            i += 1            
            if ub == b_id:
                cleaning_areas_in_bldg.append(i)

        for b_id in building_id:
            if ub == b_id:                
                for j in range(len(cleaning_areas_in_bldg)):
                    for k in range(j + 1, len(cleaning_areas_in_bldg)):
                        p = -np.abs(floor_id[j] - floor_id[k])
                        terms.append(p*x[(t, j)])
                        terms.append(p*x[(t, k)])
                        if floor_penalty > (j - k):
                            floor_penalty = j - k                
                        
obj_list.append(sum(terms))

# Objective 2: For each tour, minimise building changes.
bldg_penalty = 0
if len(uniq_buildings) > 0:
    terms = []
    bldg_penalty = floor_penalty - 2 # This will be an even more negative number.
    for t in range(n_tours):
        for j in range(n_cleaning_areas):
            for k in range(j + 1, n_cleaning_areas):
                if building_id[j] != building_id[k]:
                    terms.append(bldg_penalty * x[(t, j)])
                    terms.append(bldg_penalty * x[(t, k)])

    obj_list.append(sum(terms))

# Objective 3: maximise priorities.
max_priority = np.max(priority)
if np.min(priority) < max_priority:
    normalised_priority = common_functions.normalise(priority)
    terms = []
    for t in range(n_tours):
        for c in range(n_cleaning_areas):
            terms.append(x[(t, c)] * normalised_priority[c])

    obj_list.append(sum(terms))
    max_priority = np.max(normalised_priority)

# Objective 4: maximise allocations
factor = 1
amplify = (n_tours + len(uniq_buildings) + 2)
if max_priority > -2 * bldg_penalty:
    factor = max_priority
else:
    factor = -amplify * (bldg_penalty + floor_penalty)

terms = []    
for t in range(n_tours):
    for c in range(n_cleaning_areas):
        terms.append(factor * x[(t, c)])

obj_list.append(sum(terms))

model.AddHint(x[(0, 0)], 1)
model.AddHint(x[(1, 5)], 1)
## Final objective function.
model.Maximize(sum(obj_list))
model.ExportToFile('testPriorityMessByCodeSharing.txt')

solver = cp_model.CpSolver()
status = solver.Solve(model)

found = common_functions.report_status(status)

if found:
    print(f'Total time = {solver.ObjectiveValue()}')
    for t in range(n_tours):
        print(f'Cleaning tour {t} will clean:')
        for c in range(n_cleaning_areas):
            if solver.BooleanValue(x[(t, c)]):
                print(f'Area {c}, floor {floor_id[c]}, building {building_id[c]}.')
else:
    print('No solution found.')
        
