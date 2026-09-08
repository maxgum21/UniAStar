import tkinter as tk
from astar import *

w, h = 5, 5

l = [
    1.0, 1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0, 1.0,
    0.1, 0.1, 0.1, 0.1, 0.1,
    0.1, 0.1, 0.1, 0.1, 0.1,
    0.1, 0.1, 0.1, 0.1, 0.1
]


l_disp = [str(elem) for elem in l]


x0, y0 = 0, 2
x1, y1 = 4, 2

path = astar(l, w, h, (x0, y0), (x1, y1))
print(path)

if path == None:
    print("No path found")
    exit()

for cell in path:
    l_disp[cell[0] + cell[1] * w] = "[X]"

l_disp[x0 + y0 * w] = "STA"
l_disp[x1 + y1 * w] = "END"

for j in range(h):
    for i in range(w):
        print(l_disp[i + j * w], end=" ")
    print()