"""utils.py
Helper utilities: path reconstruction, cost calculation, simple timing.
"""
import time

def reconstruct_path(came_from, start, goal):
    if goal not in came_from:
        return []
    path = []
    curr = goal
    while curr != start:
        path.append(curr)
        curr = came_from[curr]
    path.append(start)
    path.reverse()
    return path

def path_cost(path, env):
    if not path:
        return float('inf')
    c = 0
    for p in path[1:]:  # cost for entering the cell
        c += env.cost(p)
    return c

def timed(func, *args, **kwargs):
    t0 = time.perf_counter()
    res = func(*args, **kwargs)
    t1 = time.perf_counter()
    return res, (t1-t0)*1000.0  # ms
