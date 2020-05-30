"""minesweeper python game"""
import tkinter as tk
import random
from dataclasses import dataclass
import pygame as py

WINDOW_SIZE = 500


def init():
    """initialize gui"""
    window = tk.Tk()
    window.title("Settings")
    window.resizable(False, False)
    window.geometry("200x100")

    mines_count = tk.IntVar()
    grid_size = tk.IntVar()

    mine_label = tk.Label(window, text="Mine Count: ")
    mine_label.grid(row=0, column=0)

    mine_entry = tk.Entry(window, textvariable=mines_count)
    mine_entry.grid(row=0, column=1)

    grid_label = tk.Label(window, text="Grid Size: ")
    grid_label.grid(row=1, column=0)

    grid_entry = tk.Entry(window, textvariable=grid_size)
    grid_entry.grid(row=1, column=1)

    def update():
        """update vars"""
        get_grid = grid_size.get()
        get_mine_count = mines_count.get()
        distance = WINDOW_SIZE // get_grid
        if get_grid > 30 or get_mine_count > get_grid * get_grid - 1:
            print("give smaller num \n grid < 30 must be and mines must be < GRID * GRID -1")
        else:
            main_sweeper(distance, get_grid, get_mine_count, window)

    button_calc = tk.Button(window, text="confirm", command=update)
    button_calc.grid(row=3, column=0)
    window.mainloop()


Matrix = []
Uncovered = []
adjFields = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
             (0, 1), (1, -1), (1, 0), (1, 1)]


def check_grid(y_axis, x_axis, grid_size):
    """checking grid"""
    return -1 < y_axis < grid_size and -1 < x_axis < grid_size


def loadfile(filename, distance):
    """loading files from Cells folder"""
    return py.transform.scale(py.image.load(filename), (distance, distance))


@dataclass
class Cell:
    """cell object"""
    cell_row: int
    cell_column: int
    cell_mine: bool = False
    cell_uncovered_mine: bool = False
    cell_marked: bool = False
    cell_mine_count_neighbourhood: int = 0

    def show(self, distance, screen, cell_normal, cell_marked, cell_mine):
        """showing obj on boards"""
        pos = (self.cell_column * distance, self.cell_row * distance)
        if self.cell_uncovered_mine:
            if self.cell_mine:
                screen.blit(cell_mine, pos)
            else:
                screen.blit(Uncovered[self.cell_mine_count_neighbourhood], pos)
        else:
            if self.cell_marked:
                screen.blit(cell_marked, pos)
            else:
                screen.blit(cell_normal, pos)

    def find_mines(self, grid_size):
        """finding_mines"""
        for pos in adjFields:
            new_line, new_column = self.cell_row + pos[0], self.cell_column + pos[1]
            if check_grid(new_line, new_column, grid_size)\
                    and Matrix[new_line * grid_size + new_column].cell_mine:
                self.cell_mine_count_neighbourhood += 1


def fill_func(row, col, grid_size):
    """filling with proper gifs"""
    for pos in adjFields:
        new_line = row + pos[0]
        new_column = col + pos[1]
        if check_grid(new_line, new_column, grid_size):
            celle = Matrix[new_line * grid_size + new_column]
            if celle.cell_mine_count_neighbourhood == 0 and not celle.cell_uncovered_mine:
                celle.cell_uncovered_mine = True
                fill_func(new_line, new_column, grid_size)
            else:
                celle.cell_uncovered_mine = True


def first_click(selected_cell, mines_left, grid_size):
    """first click func"""
    selected_cell.cell_uncovered_mine = True
    while mines_left > 0:
        cell = Matrix[random.randrange(grid_size * grid_size)]
        if not cell.cell_mine and cell != selected_cell:
            cell.cell_mine = True
            mines_left -= 1
    for object_in_matrix in Matrix:
        if not object_in_matrix.cell_mine:
            object_in_matrix.find_mines(grid_size)


def end_screen(win_or_loose, screen):
    """end screen"""
    font = py.font.SysFont("comicsansms", 50)
    if win_or_loose:
        text = font.render("U win", True, (0, 128, 0))
    else:
        text = font.render("U loose", True, (0, 128, 0))

    screen.fill((255, 255, 255))
    screen.blit(text,
                (250 - text.get_width() // 2, 240 - text.get_height() // 2))

    py.display.flip()


def main_sweeper(distance, grid_size, total_mine_count, window):
    """main func that runs game"""
    py.init()
    mines_left = total_mine_count
    flags_on_mines = 0
    screen = py.display.set_mode([WINDOW_SIZE, WINDOW_SIZE])
    py.display.set_caption('Minesweeper By Krzysztof Greś')

    cell_normal = loadfile('./Cells/cellnormal.gif', distance)
    cell_marked = loadfile('./Cells/cellmarked.gif', distance)
    cell_mine = loadfile('./Cells/cellmine.gif', distance)

    for cell_in_grid in range(9):
        Uncovered.append(loadfile(f'./Cells/cell{cell_in_grid}.gif', distance))

    for cell_in_grid in range(grid_size * grid_size):
        Matrix.append(Cell(cell_in_grid // grid_size, cell_in_grid % grid_size))

    flag = True
    ongoing = True
    while ongoing:
        for event in py.event.get():
            if event.type == py.QUIT:
                ongoing = False
            if event.type == py.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = py.mouse.get_pos()
                cell = Matrix[mouse_y // distance * grid_size + mouse_x // distance]
                if flag:
                    first_click(cell, mines_left, grid_size)
                if not flag:
                    if py.mouse.get_pressed()[2]:
                        cell.cell_marked = not cell.cell_marked
                        if cell.cell_mine:
                            flags_on_mines += 1
                            print(1)
                        if flags_on_mines == total_mine_count:
                            end_screen(True, screen)
                            ongoing = False
                            py.time.wait(5000)

                    if py.mouse.get_pressed()[0]:
                        cell.cell_uncovered_mine = True
                        if cell.cell_mine_count_neighbourhood == 0 and not cell.cell_mine:
                            fill_func(mouse_y // distance, mouse_x // distance, grid_size)
                        if cell.cell_mine:
                            for obj in Matrix:
                                obj.cell_uncovered_mine = True
                            end_screen(False, screen)
                            ongoing = False
                            py.time.wait(5000)
                flag = False
        for obj in Matrix:
            obj.show(distance, screen, cell_normal, cell_marked, cell_mine)
        py.display.flip()

    py.display.quit()
    window.destroy()


init()
