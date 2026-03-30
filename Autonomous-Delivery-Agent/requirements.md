# Requirements and Run Instructions

- Python 3.8+ (3.10 recommended)
- No external packages required.
- To run a planner:
    python main.py --algorithm astar --map maps/small.txt
- To specify start and goal:
    python main.py --algorithm ucs --map maps/medium.txt --start 0 0 --goal 9 9
- Optional dynamic obstacles: add a JSON file next to map named <mapfile>.dyn.json
  Example content: {"0": [[2,2]], "1": [[2,3]], "2": [[2,4]]} where keys are integer time steps.
