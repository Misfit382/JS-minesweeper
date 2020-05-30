import tkinter as tk
import random
from dataclasses import dataclass
import pygame as py
import sys

WINDOW_SIZE = 500

def init():
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
        GRID = grid_size.get()
        TOTALMINECOUNT = minesCount.get()
        DISTANCE = WINDOW_SIZE // GRID
        if GRID > 30 or TOTALMINECOUNT > GRID * GRID - 1:
            print("give smaller num \n grid < 30 must be and mines must be < GRID * GRID -1")
        else:
            mainSweeper(DISTANCE, GRID,TOTALMINECOUNT, window)

    button_calc = tk.Button(window, text="confirm", command=update)
    button_calc.grid(row=3, column=0)
    window.mainloop()

Matrix = []
Uncovered = []
adjFields = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                (0, 1), (1, -1), (1, 0), (1, 1)]

def check_grid(y, x, GRID_SIZE):
    return -1 < y < GRID_SIZE and -1 < x < GRID_SIZE

def loadfile(filename, DISTANCE):
        return py.transform.scale(py.image.load(filename), (DISTANCE, DISTANCE))

@dataclass
class Cell:
    Row: int
    Column: int
    Mine: bool = False
    UncoveredMine: bool = False
    Marked: bool = False
    Mine_Count_Neighbourhood: int = 0

    def show(self, DISTANCE,screen, cell_normal,cell_marked,cell_mine):
        pos = (self.Column * DISTANCE, self.Row * DISTANCE)
        if self.UncoveredMine:
            if self.Mine:
                screen.blit(cell_mine, pos)
            else:
                screen.blit(Uncovered[self.Mine_Count_Neighbourhood], pos)
        else:
            if self.Marked:
                screen.blit(cell_marked, pos)
            else:
                screen.blit(cell_normal, pos)

    def find_mines(self,GRID_SIZE):
        for pos in adjFields:
            new_line, new_column = self.Row + pos[0], self.Column + pos[1]
            if check_grid(new_line, new_column, GRID_SIZE) and Matrix[new_line * GRID_SIZE + new_column].Mine:
                self.Mine_Count_Neighbourhood += 1

def fill_func(row, col, GRID_SIZE):
        for pos in adjFields:
            new_line = row + pos[0]
            new_column = col + pos[1]
            if check_grid(new_line, new_column, GRID_SIZE):
                celle = Matrix[new_line * GRID_SIZE + new_column]
                if celle.Mine_Count_Neighbourhood == 0 and not celle.UncoveredMine:
                    celle.UncoveredMine = True
                    fill_func(new_line, new_column,GRID_SIZE)
                else:
                    celle.UncoveredMine = True

def first_click(selected_cell, mines_left,GRID_SIZE):
    selected_cell.UncoveredMine = True
    while mines_left > 0:
        cell = Matrix[random.randrange(GRID_SIZE * GRID_SIZE)]
        if not cell.Mine and cell != selected_cell:
            cell.Mine = True
            mines_left -= 1
    for obj in Matrix:
        if not obj.Mine:
            obj.find_mines(GRID_SIZE)


def test(winorloose, screen):
    font = py.font.SysFont("comicsansms", 50)
    if winorloose == True:
        text = font.render("U win", True, (0, 128, 0))
    else:
        text = font.render("U loose", True, (0, 128, 0))

    screen.fill((255, 255, 255))
    screen.blit(text,
        (250 - text.get_width() // 2, 240 - text.get_height() // 2))
    
    py.display.flip()

def mainSweeper(DISTANCE, GRID_SIZE,TOTALMINECOUNT, window):
    py.init()
    mines_left = TOTALMINECOUNT 
    flags_on_mines = 0
    screen = py.display.set_mode([WINDOW_SIZE, WINDOW_SIZE])
    py.display.set_caption('Minesweeper By Krzysztof Greś')

    cell_normal = loadfile('./Cells/cellnormal.gif', DISTANCE)
    cell_marked = loadfile('./Cells/cellmarked.gif', DISTANCE)
    cell_mine = loadfile('./Cells/cellmine.gif', DISTANCE)

    for n in range(9):
        Uncovered.append(loadfile(f'./Cells/cell{n}.gif', DISTANCE))


    for n in range(GRID_SIZE * GRID_SIZE):
        Matrix.append(Cell(n // GRID_SIZE, n % GRID_SIZE))
    
    flag = True
    ongoing = True
    while ongoing:
        for event in py.event.get():
            if event.type == py.QUIT:
                ongoing = False
            if event.type == py.MOUSEBUTTONDOWN:
                mouseX, mouseY = py.mouse.get_pos()
                cell = Matrix[mouseY // DISTANCE * GRID_SIZE + mouseX // DISTANCE]
                if flag == True:
                    first_click(cell, mines_left, GRID_SIZE)
                if flag == False:
                    if py.mouse.get_pressed()[2]:
                        cell.Marked = not cell.Marked
                        if cell.Mine:
                            flags_on_mines += 1
                            print(1)
                        if flags_on_mines == TOTALMINECOUNT:
                            test(True,screen)
                            ongoing = False
                            py.time.wait(5000)

                    if py.mouse.get_pressed()[0]:
                        cell.UncoveredMine = True
                        if cell.Mine_Count_Neighbourhood == 0 and not cell.Mine:
                            fill_func(mouseY // DISTANCE, mouseX // DISTANCE, GRID_SIZE)
                        if cell.Mine:
                            for obj in Matrix:
                                obj.UncoveredMine = True
                            test(False,screen)
                            ongoing = False
                            py.time.wait(5000)
                flag = False
        for obj in Matrix:
            obj.show(DISTANCE,screen,cell_normal,cell_marked,cell_mine)
        py.display.flip()

    py.display.quit()
    window.destroy()

init()
