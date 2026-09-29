import pygame
from pygame import Rect
from typing import List, Tuple
from astar import *

class Cell:
    def __init__(self, value : float):
        self.val = value
        self.is_path = False
        self.is_tried = False
        self.is_walked = False
        self.is_start = False
        self.is_end = False

WIDTH, HEIGHT = 1200, 800

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
tickrate = 20
dt = 0

is_mouse_held = False
has_cell_changed = False
prev_cell = (-1, -1)

flag_just_pressed = False
is_setting_points = 0
cellb, celle = (-1, -1), (-1, -1)

start_just_pressed = False
was_path_created = False

mapw, maph = 50, 20
board = [[Cell(1) for _ in range(mapw)] for _ in range(maph)]
board_x, board_y, cell_size = 0, 0, 0


def draw_cells(board : List[List[Cell]], padding : int):
    global board_x, board_y, cell_size

    if len(board) == 0:
        return

    w, h = len(board[0]), len(board) 
    csize = min(WIDTH // w, (HEIGHT * 0.9) // h)
    mx = (WIDTH - csize * w) // 2
    my = (int(HEIGHT * 0.9) - csize * h) // 2
    board_x, board_y, cell_size = mx, my, csize

    for x in range(w):
        for y in range(h):
            r = Rect(mx + x * csize + padding, my + y * csize + padding, csize - padding, csize - padding)
            cell = board[y][x]

            MINCOL, MAXCOL = 50, 255
            col = (0, 0, 0)
            if cell.is_end:
                col = (200, 50, 50)
            elif cell.is_start:
                col = (50, 200, 50)
            elif cell.is_path:
                col = (200, 200, 50)
            elif cell.is_walked:
                col = (160, 160, 50)
            elif cell.is_tried:
                col = (120, 120, 50)
            else:
                cval = MINCOL + cell.val * (MAXCOL - MINCOL)
                col = (cval, cval, cval)

            pygame.draw.rect(screen, col, r)

def get_cell_by_pos(pos : Tuple[int, int]) -> Tuple[int, int]:
    board_w = cell_size * mapw
    board_h = cell_size * maph
    bx, by = 0, 0

    minx, maxx = board_x, board_x + board_w
    miny, maxy = board_y, board_y + board_h
    if pos[0] >= minx and pos[0] < maxx and pos[1] >= miny and pos[1] < maxy:
        bx = (pos[0] - board_x) // cell_size
        by = (pos[1] - board_y) // cell_size
        return (bx, by)
    return (-1, -1)

def astarize_board(board : List[List[Cell]]) -> List[float]:
    if not len(board): return None
    w, h = len(board[0]), len(board)
    res = []
    for y in range(h):
        for x in range(w):
            res.append(board[y][x].val)
    return res


while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            is_mouse_held = True
        elif event.type == pygame.MOUSEBUTTONUP:
            is_mouse_held = False
            has_cell_changed = False
            prev_cell = (-1, -1)
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                if not flag_just_pressed:
                    flag_just_pressed = True

                    if was_path_created:
                        was_path_created = False
                        for celll in board:
                            for cell in celll:
                                cell.is_path = False

                    if celle != (-1, -1):
                        board[celle[1]][celle[0]].is_end = False
                    if cellb != (-1, -1):
                        board[cellb[1]][cellb[0]].is_start = False
                    if is_setting_points == 1:
                        is_setting_points = 0
                    else:
                        is_setting_points = 1
                    
            if event.key == pygame.K_RETURN:
                if not start_just_pressed:
                    start_just_pressed = True
                    was_path_created = False
                    for celll in board:
                        for cell in celll:
                            cell.is_path = False
                    if cellb == (-1, -1) or celle == (-1, -1):
                        print("Please select start and end cells!")
                    else:
                        blist = astarize_board(board)
                        path = astar(blist, mapw, maph, cellb, celle)
                        if path:
                            was_path_created = True
                            for cell in path:
                                if cell != celle and cell != cellb:
                                    board[cell[1]][cell[0]].is_path = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                flag_just_pressed = False
            if event.key == pygame.K_RETURN:
                start_just_pressed = False
    
    if is_mouse_held:
        pos = pygame.mouse.get_pos()
        bx, by = get_cell_by_pos(pos)
        if bx != -1:
            if prev_cell != (bx, by):
                prev_cell = (bx, by)
                if is_setting_points == 1:
                    if board[by][bx].val != 0:
                        board[by][bx].is_start = True
                        cellb = (bx, by)
                        is_setting_points = 2
                elif is_setting_points == 2:
                    if (bx, by) == cellb:
                        is_setting_points = 0
                        board[by][bx].is_start = False
                    else:
                        board[by][bx].is_end = True
                        celle = (bx, by)
                        is_setting_points = 0
                else:
                    board[by][bx].val = 1 - board[by][bx].val


    # RENDER #

    pygame.draw.rect(screen, (100, 100, 100), Rect(0, (HEIGHT * 0.9), WIDTH, HEIGHT * 0.1))

    draw_cells(board, 1)

    pygame.display.flip()

    # ------ #

    dt = clock.tick(tickrate) / 1000   

pygame.quit()