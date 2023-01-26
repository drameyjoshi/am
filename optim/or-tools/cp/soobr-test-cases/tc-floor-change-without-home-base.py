from typing import List

from ortools.sat.python import cp_model

# Input data. Relevant parameters chosen from 'testFloorChangeWithoutHomeBase.json'.
time_to_clean = [1, 1, 1, 1, 1]
priority = [80, 80, 80, 80, 80]
floor_id = [1, 2, 3, 4, 5]
floor_sort = [0, 1, 2, 1, 2]
building_id = [1, 1, 1, 2, 2]

tour_max_duration = [2, 2, 2]

n_tours = len(tour_max_duration)
n_cleaning_areas = len(time_to_clean)
assert(n_cleaning_areas == len(priority))

# Build the constraints.
model = cp_model.CpModel()
# Decision variables
x = {}
for t in range(n_tours):
    for c in range(n_cleaning_areas):
        x[(t, c)] = model.NewBoolVar(f'x[{t}, {c}]')

# Constraint 1: For any tour, time to clean <= tour max duration.
for t in range(n_tours):
    time = [x[(t, c)] * time_to_clean[c] for c in range(n_cleaning_areas)]
    model.AddLinearConstraint(sum(time), 0, tour_max_duration[t])

# Constraint 2: A cleaning area should be allocated to at most one tour.
for c in range(n_cleaning_areas):
    model.AddAtMostOne([x[(t, c)] for t in range(n_tours)])

# Objective: For each tour, within a building, minimise floor change.
terms = []
uniq_buildings = (b for b in building_id)
floor_penalty = 0 # This will be a negative number.
for t in range(n_tours):        
    for ub in uniq_buildings:
        i = -1
        # Get indices of all floors in this building
        floor_idx = []
        for b_id in building_id:
            i += 1            
            if ub == b_id:
                floor_idx.append(i)

        for b_id in building_id:
            if ub == b_id:                
                for j in range(len(floor_idx)):
                    for k in range(j + 1, len(floor_idx)):
                        terms.append((j - k)*x[(t, j)])
                        terms.append((j - k)*x[(t, k)])
                        if floor_penalty > (j - k):
                            floor_penalty = j - k
                        
obj_1 = sum(terms)

# Objective: For each tour, minimise building changes.
terms = []
bldg_penalty = floor_penalty - 1 # This will be an even more negative number.
for t in range(n_tours):
    for j in range(n_cleaning_areas):
        for k in range(j + 1, n_cleaning_areas):
            if building_id[j] != building_id[k]:
                terms.append(bldg_penalty * x[(t, j)])
                terms.append(bldg_penalty * x[(t, k)])

obj_2 = sum(terms)

# Objective: maximise priorities.
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
terms = []
for t in range(n_tours):
    for c in range(n_cleaning_areas):
        terms.append(x[(t, c)] * normalised_priority[c])

obj_3 = sum(terms)

# Objective: maximise allocations
terms = []
for t in range(n_tours):
    for c in range(n_cleaning_areas):
        terms.append(x[(t, c)])

obj_4 = sum(terms)

model.Maximize(sum([obj_1, obj_2, obj_3, obj_4]))

solver = cp_model.CpSolver()
status = solver.Solve(model)

found = False
if status == cp_model.FEASIBLE:
    print('Found a feasible solution.')
    found = True
elif status == cp_model.OPTIMAL:
    print('Found an optimal solution.')
    found = True

if found:
    print(f'Total time = {solver.ObjectiveValue()}')
    for t in range(n_tours):
        print(f'Cleaning tour {t} will clean:')
        for c in range(n_cleaning_areas):
            if solver.BooleanValue(x[(t, c)]):
                print(f'Area {c}, floor {floor_id[c]}, building {building_id[c]}.')
else:
    print('No solution found.')
        
