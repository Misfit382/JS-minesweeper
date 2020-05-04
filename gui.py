from main import *

GRID = 20
TOTALMINECOUNT = 50


def init():
    import tkinter as tk

    window = tk.Tk()
    window.title("Settings")
    window.resizable(False, False)
    window.geometry("200x100")

    minesCount = tk.IntVar()
    grid_size = tk.IntVar()

    minelabel = tk.Label(window, text="Mine Count: ")
    minelabel.grid(row=0, column=0)

    mineEntry = tk.Entry(window, textvariable=minesCount)
    mineEntry.grid(row=0, column=1)

    gridlabel = tk.Label(window, text="Grid Size: ")
    gridlabel.grid(row=1, column=0)

    gridEntry = tk.Entry(window, textvariable=grid_size)
    gridEntry.grid(row=1, column=1)

    def update():
        WINDOW = 500
        GRID = grid_size.get()
        TOTALMINECOUNT = minesCount.get()
        DIST = WINDOW // GRID
        if GRID > 30 or TOTALMINECOUNT > GRID * GRID - 1:
            print("give smaller num \n grid < 30 must be and mines must be < GRID * GRID -1")
        else:
            mainSweeper(WINDOW, GRID, TOTALMINECOUNT, DIST)

    button_calc = tk.Button(window, text="confirm", command=update)
    button_calc.grid(row=3, column=0)
    window.mainloop()


init()
