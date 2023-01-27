from typing import List
from ortools.sat.python import cp_model

def normalise(priority: List[int]) -> List[int]:
    freq = {}
    M = len(priority)
    for p in priority:
        if p in freq:
            freq[p] += 1
        else:
            freq[p] = 1

    normalised_priority = []
    for i in range(len(priority)):
        normalised_priority.append(int(M * priority[i]/freq[priority[i]]))

    return normalised_priority

def report_status(status: int) -> None:
    found = False
   
    match status:
        case cp_model.FEASIBLE:
            print('Found a feasible solution.')
            found = True
        case cp_model.OPTIMAL:
            print('Found an optimal solution.')
            found = True
        case cp_model.INFEASIBLE:
            print('The problem is infeasible.')
        case cp_model.MODEL_INVALID:
            print('The model is invalid.')
        case _:
            print('Unknown status')
            

    return found
