import tkinter as tk

root = tk.Tk(className="astar")
root.title("A* Demo")
root.geometry("600x400")

# Main geometry

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=3)
root.columnconfigure(0, weight=1)

setframe = tk.Frame(root, background="red")
mapframe = tk.Frame(root, background="green")

setframe.grid(row=0, column=0, sticky="nsew")
mapframe.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

#

w, h = 20, 20

def set_map_size():
    w = int(xbox.get())
    if w > MAX_SIZE:
        w = MAX_SIZE
        xbox.invoke("buttonup")
    elif w < MIN_SIZE:
        w = MIN_SIZE
        xbox.invoke("buttondown")

    h = int(ybox.get())
    if h > MAX_SIZE:
        h = MAX_SIZE
        ybox.invoke("buttonup")
    elif h < MIN_SIZE:
        h = MIN_SIZE
        ybox.invoke("buttondown")
    print(w, h)

    set_map()


# Settings

MAX_SIZE = 50
MIN_SIZE = 10

is_start, is_end = False, False
value = 1.0

setframe.columnconfigure(0, weight=1)
setframe.columnconfigure(1, weight=1)
setframe.columnconfigure(2, weight=1)
setframe.columnconfigure(3, weight=10)
setframe.rowconfigure(0, weight=1)
setframe.rowconfigure(1, weight=1)
setframe.rowconfigure(2, weight=1)

xbox = tk.Spinbox(setframe, from_=MIN_SIZE, to=MAX_SIZE)
xlabel = tk.Label(setframe, text="x")
ybox = tk.Spinbox(setframe, from_=MIN_SIZE, to=MAX_SIZE)
ylabel = tk.Label(setframe, text="y")
setb = tk.Button(setframe, text="Set", command=set_map_size)

xlabel.grid(row=0, column=0, sticky="nwse")
xbox.grid(row=0, column=1, sticky="nwse")
ylabel.grid(row=1, column=0, sticky="nwse")
ybox.grid(row=1, column=1, sticky="nwse")
setb.grid(row=0, column=2, rowspan=2)


# Buttons


def click(x : int, y : int) -> callable:
    def curry():
        but : tk.Button = mapframe.grid_slaves(row=y, column=x)[0]
        but.config(bg="#00AA00", activebackground="#00CC00")
    return curry

def set_map():
    for child in mapframe.winfo_children():
        child.destroy()
    
    for i in range(w):
        mapframe.rowconfigure(i, weight=1)

    for i in range(h):
        mapframe.columnconfigure(i, weight=1)
    
    for x in range(w):
        for y in range(h):
            tk.Button(mapframe, text="0.0", command=click(x, y)).grid(row=y, column=x, sticky="nwse")



set_map()
root.mainloop()


#from astar import *
#
#w, h = 5, 5
#
#l = [
#    1.0, 1.0, 1.0, 1.0, 1.0,
#    1.0, 1.0, 1.0, 1.0, 1.0,
#    0.1, 0.1, 0.1, 0.1, 0.1,
#    0.1, 0.1, 0.1, 0.1, 0.1,
#    0.1, 0.1, 0.1, 0.1, 0.1
#]
#
#
#l_disp = [str(elem) for elem in l]
#
#
#x0, y0 = 0, 2
#x1, y1 = 4, 2
#
#path = astar(l, w, h, (x0, y0), (x1, y1))
#print(path)
#
#if path == None:
#    print("No path found")
#    exit()
#
#for cell in path:
#    l_disp[cell[0] + cell[1] * w] = "[X]"
#
#l_disp[x0 + y0 * w] = "STA"
#l_disp[x1 + y1 * w] = "END"
#
#for j in range(h):
#    for i in range(w):
#        print(l_disp[i + j * w], end=" ")
#    print()