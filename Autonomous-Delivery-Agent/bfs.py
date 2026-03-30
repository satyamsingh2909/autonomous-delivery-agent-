"""bfs.py - BFS for unweighted (or step-cost) grids.
Returns path and statistics (nodes expanded).
"""
from collections import deque
from typing import Tuple

def bfs(env):
    start, goal = env.start, env.goal
    frontier = deque([start])
    came_from = {start: None}
    nodes_expanded = 0
    while frontier:
        current = frontier.popleft()
        nodes_expanded += 1
        if current == goal:
            break
        for n in env.neighbors(current):
            if n not in came_from:
                came_from[n] = current
                frontier.append(n)
    path = __reconstruct(came_from, start, goal)
    return {'path': path, 'nodes': nodes_expanded}

def __reconstruct(came_from, start, goal):
    if goal not in came_from:
        return []
    path = []
    cur = goal
    while cur != start:
        path.append(cur)
        cur = came_from[cur]
    path.append(start)
    return list(reversed(path))
