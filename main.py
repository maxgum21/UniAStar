import tkinter as tk
from astar import *

r, c = 5, 5

l = [
    1, 1, 1, 1, 1,
    1, 1, 0, 1, 1,
    1, 1, 0, 1, 1,
    1, 1, 0, 1, 1,
    1, 1, 0, 1, 1
]

l_disp = [str(elem) for elem in l]


x0, y0 = 0, 2
x1, y1 = 3, 4

map = Map(r, c, l)
path = astar(map, euclidian_heuristic, x0, y0, x1, y1)

if path == None:
    print("No path found")
    exit()

for cell in path:
    l_disp[cell.x + cell.y * c] = "X"

l_disp[x0 + y0 * c] = "S"
l_disp[x1 + y1 * c] = "E"

for j in range(c):
    for i in range(r):
        print(l_disp[i + j * c], end=" ")
    print()