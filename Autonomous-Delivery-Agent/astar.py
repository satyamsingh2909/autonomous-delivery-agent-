"""astar.py - A* search with admissible Manhattan heuristic.
Returns path and statistics (nodes expanded).
"""
import heapq

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(env):
    start, goal = env.start, env.goal
    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    nodes_expanded = 0
    visited = set()
    while frontier:
        _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        nodes_expanded += 1
        if current == goal:
            break
        for n in env.neighbors(current):
            new_cost = cost_so_far[current] + env.cost(n)
            if n not in cost_so_far or new_cost < cost_so_far[n]:
                cost_so_far[n] = new_cost
                priority = new_cost + heuristic(n, goal)
                heapq.heappush(frontier, (priority, n))
                came_from[n] = current
    path = reconstruct(came_from, start, goal)
    return {'path': path, 'nodes': nodes_expanded}

def reconstruct(came_from, start, goal):
    if goal not in came_from:
        return []
    path = []
    cur = goal
    while cur != start:
        path.append(cur)
        cur = came_from[cur]
    path.append(start)
    path.reverse()
    return path
