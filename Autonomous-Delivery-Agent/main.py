"""main.py - CLI entry point to run planners on map files.
Usage examples:
    python main.py --algorithm astar --map maps/small.txt
"""
import argparse, json
from pathlib import Path
from environment import GridEnvironment
import utils
import bfs, ucs, astar, simulated_annealing as sa

def load_map(path):
    with open(path,'r') as f:
        grid = [list(map(int, line.split())) for line in f if line.strip()]
    return grid

def parse_dynamic(path):
    # optional: dynamic obstacles file format (json) next to map with same name + .dyn.json
    dynfile = Path(path).with_suffix(Path(path).suffix + '.dyn.json')
    if dynfile.exists():
        with open(dynfile,'r') as f:
            return json.load(f)
    return {}

def pretty_print(path):
    if not path:
        print("No path found.")
        return
    print(" -> ".join(str(p) for p in path))
    print("Length (steps):", len(path)-1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--algorithm", choices=["bfs","ucs","astar","sa"], required=True)
    parser.add_argument("--map", required=True, help="Path to map txt file")
    parser.add_argument("--start", nargs=2, type=int, help="Start x y", required=False)
    parser.add_argument("--goal", nargs=2, type=int, help="Goal x y", required=False)
    args = parser.parse_args()

    grid = load_map(args.map)
    start = tuple(args.start) if args.start else (0,0)
    goal = tuple(args.goal) if args.goal else (len(grid)-1, len(grid[0])-1)
    dyn = parse_dynamic(args.map)
    env = GridEnvironment(grid, start, goal, dynamic_obstacles=dyn)

    if args.algorithm == "bfs":
        res, t = utils.timed(bfs.bfs, env)
    elif args.algorithm == "ucs":
        res, t = utils.timed(ucs.uniform_cost, env)
    elif args.algorithm == "astar":
        res, t = utils.timed(astar.astar, env)
    else:
        res, t = utils.timed(sa.simulated_annealing, env)

    path = res.get('path') if isinstance(res, dict) else (res if isinstance(res, list) else [])
    nodes = res.get('nodes') if isinstance(res, dict) else '-'
    cost = utils.path_cost(path, env)
    print(f"Algorithm: {args.algorithm.upper()}")
    print(f"Nodes expanded: {nodes}")
    print(f"Time (ms): {t:.3f}")
    print(f"Path cost: {cost if cost!=float('inf') else 'N/A'}")
    pretty_print(path)
