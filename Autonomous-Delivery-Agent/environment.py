"""environment.py
Grid environment with terrain costs, static and dynamic obstacles.
"""
from typing import List, Tuple, Dict

class GridEnvironment:
    def __init__(self, grid: List[List[int]], start: Tuple[int,int], goal: Tuple[int,int],
                 dynamic_obstacles: Dict[int, list]=None):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows>0 else 0
        # dynamic_obstacles is a dict mapping time step -> list of (x,y) cells occupied
        self.dynamic_obstacles = dynamic_obstacles or {}

    def in_bounds(self, pos: Tuple[int,int]) -> bool:
        x,y = pos
        return 0 <= x < self.rows and 0 <= y < self.cols

    def passable(self, pos: Tuple[int,int], t: int = 0) -> bool:
        x,y = pos
        if not self.in_bounds(pos):
            return False
        if self.grid[x][y] == -1:
            return False
        # check dynamic obstacles at time t (if provided)
        if t in self.dynamic_obstacles and pos in self.dynamic_obstacles[t]:
            return False
        return True

    def cost(self, pos: Tuple[int,int]) -> int:
        x,y = pos
        return self.grid[x][y]

    def neighbors(self, pos: Tuple[int,int], t: int = 0):
        x,y = pos
        cand = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        result = []
        for n in cand:
            if self.in_bounds(n) and self.passable(n, t):
                result.append(n)
        return result
