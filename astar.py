from typing import Callable

class Cell:
    def __init__(self, x : int, y : int, cost : float = 1.0, g : float = float('inf'), f : float = float('inf')):
        self.x = x
        self.y = y
        self.cost = cost # if cost is 0, can't enter; if more than 1, less likely to enter
        self.g = g
        self.f = f
        self.came_from : Cell = None
    
    def __str__(self):
        return f"Cell: (x:{self.x}, y:{self.y}) cost:{self.cost}, g:{self.g:.2f}, f:{self.f:.2f}"

class MinHeap:
    def __init__(self):
        self._list : list[Cell] = []
    
    def __bool__(self):
        return len(self._list) != 0
    
    def insert(self, ncell : Cell) -> int:
        if len(self._list) == 0:
            self._list.append(ncell)
            return 0

        for i, cell in enumerate(self._list):
            if ncell.f <= cell.f:
                self._list.insert(i, ncell)
                return i
        
        self._list.append(cell)
        return len(self._list) - 1
    
    def pop(self) -> Cell:
        if len(self._list) == 0:
            return None
        return self._list.pop(0)


class Map:
    def __init__(self, row : int, col : int, cmap : list[int] = []):
        self.row = row
        self.col = col
        if cmap:
            self._list = [Cell(i, j, cmap[i + j * col]) for j in range(self.row) for i in range(self.col)]
        else:
            self._list = [Cell(i, j) for j in range(self.row) for i in range(self.col)]

    
    def __getitem__(self, index):
        return self._list[index[0] + index[1] * self.col]

    def get_neighbors(self, x : int, y : int) -> list[tuple[Cell, float]]:
        res = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i < 0 or i >= self.col or j < 0 or j >= self.row or (i == x and j == y):
                    continue
                res.append((self[i, j], (((x - i) ** 2 + (y - j) ** 2) ** 0.5) * self[i, j].cost))
        return res

def reconstruct_path(dest : Cell) -> list[Cell]:
    res = []
    while dest != None:
        res.insert(0, dest)
        dest = dest.came_from
    return res


def astar(cmap : Map, heuristic : Callable[[int, int, int, int], float], x0 : int, y0 : int, x1 : int, y1 : int) -> list[Cell]:
    if x0 == x1 and y0 == y1: return [Map[x0, y0]]

    cmap[x0, y0].g = 0.0
    cmap[x0, y0].f = 0.0

    heap = MinHeap()
    heap.insert(cmap[x0, y0])

    while heap:
        cur = heap.pop()
        
        if cur.x == x1 and cur.y == y1:
            return reconstruct_path(cur)
        
        for neighbor, cost in cmap.get_neighbors(cur.x, cur.y):
            if neighbor.cost == 0.0: continue
            ng = cur.g + cost
            if ng < neighbor.g:
                neighbor.came_from = cur
                neighbor.g = ng
                neighbor.f = ng + heuristic(neighbor.x, neighbor.y, x1, y1)
                heap.insert(neighbor)

    return None

def manhattan_heuristic(x0, y0, x1, y1) -> float:
    return abs(x1 - x0) + abs(y1 - y0)

def euclidian_heuristic(x0, y0, x1, y1) -> float:
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5