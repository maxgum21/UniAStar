from typing import Tuple, List, Dict, Callable

PASSIVE_COST : float = 0.1

class MyHeap(List[Tuple[int, int, int]]):
    def stack(self, item : Tuple[int, int]):
        for i, elem in enumerate(self):
            if item[0] <= elem[0]:
                self.insert(i, item)
                return
        self.append(item)

    def pick(self) -> Tuple[int, int, int]:
        return self.pop(0)

def euclidean_heuristic(a : Tuple[int, int], b : Tuple[int, int]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def manhattan_heuristic(a : Tuple[int, int], b : Tuple[int, int]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(map : List[float], w : int, h : int, start : Tuple[int, int], end : Tuple[int, int],
          heuristic : Callable[[Tuple[int, int], Tuple[int, int]], float] = euclidean_heuristic) -> List[Tuple[int, int]]:

    def get_map(t : Tuple[int, int]) -> float:
        return map[t[0] + t[1] * w]

    def get_neighbors(t : Tuple[int, int]) -> List[Tuple[int, int]]:
        res = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0 and j == 0) or (t[0] + i) < 0 or (t[1] + j) < 0 or (t[0] + i) >= w or (t[1] + j) >= h:
                    continue
                res.append((t[0] + i, t[1] + j))
        return res

    came_from : Dict[Tuple[int, int], Tuple[int, int]] = {}

    def reconstruct_path(t : Tuple) -> List[Tuple[int, int]]:
        res = []
        cur = t
        while cur and cur != start:
            res.append(cur)
            cur = came_from[cur]
        res.append(start)
        return res[::-1]
                

    g_score : Dict[Tuple[int, int], float] = {}

    heap = MyHeap()
    heap.stack((0, *start))

    g_score[start] = 0

    while len(heap):
        f, *cur = heap.pick()
        cur = tuple(cur)

        if cur == end:
            return reconstruct_path(cur)
        
        for neigh in get_neighbors(cur):
            if get_map(neigh) == 0.0: continue

            g = g_score[cur] + (1 - get_map(neigh)) + PASSIVE_COST
            if g_score.get(neigh) is None or g_score[neigh] > g:
                g_score[neigh] = g
                came_from[neigh] = cur
                heap.stack([g + heuristic(neigh, end), *neigh])

    return None