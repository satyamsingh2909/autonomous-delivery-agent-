"""simulated_annealing.py - Local search (Simulated Annealing) for replanning.
This is a proof-of-concept local search; not guaranteed optimality.
"""
import random, math

def simulated_annealing(env, max_steps=500, T0=10.0, cooling=0.995):
    # initialize with a simple greedy path (random walk)
    current = random_path(env)
    best = current[:]
    def p_cost(path):
        return sum(env.cost(p) for p in path[1:]) if path else float('inf')

    T = T0
    nodes_expanded = 0
    for step in range(max_steps):
        neighbor = mutate_path(current, env)
        nodes_expanded += 1
        delta = p_cost(neighbor) - p_cost(current)
        if delta < 0 or random.random() < math.exp(-delta / max(1e-9, T)):
            current = neighbor
            if p_cost(current) < p_cost(best):
                best = current[:]
        T *= cooling
    return {'path': best, 'nodes': nodes_expanded}

def random_path(env, max_len=500):
    path = [env.start]
    cur = env.start
    visited = set([cur])
    while cur != env.goal and len(path) < max_len:
        nbrs = [n for n in env.neighbors(cur) if n not in visited]
        if not nbrs:
            break
        cur = random.choice(nbrs)
        visited.add(cur)
        path.append(cur)
    if path[-1] != env.goal:
        # try to append a best-effort direct sequence (may not reach goal)
        return path
    return path

def mutate_path(path, env):
    if not path:
        return path
    if len(path) < 3:
        return random_path(env)
    i = random.randrange(1, len(path)-1)
    new_path = path[:i]
    cur = new_path[-1]
    while cur != env.goal and len(new_path) < 500:
        nbrs = env.neighbors(cur)
        if not nbrs:
            break
        cur = random.choice(nbrs)
        new_path.append(cur)
    return new_path
