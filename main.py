import random
from dataclasses import dataclass

import pygame


def mainSweeper(WINDOW, GRID, TOTALMINECOUNT, DIST):
    pygame.init()
    screen = pygame.display.set_mode([WINDOW, WINDOW])

    pygame.display.set_caption('Minesweeper By Krzysztof Greś')

    def loadfile(filename):
        return pygame.transform.scale(pygame.image.load(filename), (DIST, DIST))

    @dataclass
    class Cell:
        Row: int
        Col: int
        Mine: bool = False
        Unc: bool = False
        Marked: bool = False
        Mine_Count_Neighbourhood = int = 0

        def show(self):
            pos = (self.Col * DIST, self.Row * DIST)
            if self.Unc:
                if self.Mine:
                    screen.blit(CELL_MINE, pos)
                else:
                    screen.blit(Uncovered[self.Mine_Count_Neighbourhood], pos)
            else:
                if self.Marked:
                    screen.blit(CELL_MARKED, pos)
                else:
                    screen.blit(CELL_NORMAL, pos)

        def find_mines(self):
            for pos in adjFields:
                new_line, new_column = self.Row + pos[0], self.Col + pos[1]
                if check_grid(new_line, new_column) and Matrix[new_line * GRID + new_column].Mine:
                    self.Mine_Count_Neighbourhood += 1

    def check_grid(y, x):
        return -1 < y < GRID and -1 < x < GRID

    CELL_NORMAL = loadfile('cellnormal.gif')
    CELL_MARKED = loadfile('cellmarked.gif')
    CELL_MINE = loadfile('cellmine.gif')
    Uncovered = []

    for n in range(9):
        Uncovered.append(loadfile(f'cell{n}.gif'))

    Matrix = []
    adjFields = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                 (0, 1), (1, -1), (1, 0), (1, 1)]

    def fill_func(row, col):
        for pos in adjFields:
            new_line = row + pos[0]
            new_column = col + pos[1]
            if check_grid(new_line, new_column):
                celle = Matrix[new_line * GRID + new_column]
                if celle.Mine_Count_Neighbourhood == 0 and not celle.Unc:
                    celle.Unc = True
                    fill_func(new_line, new_column)
                else:
                    celle.Unc = True

    for n in range(GRID * GRID):
        Matrix.append(Cell(n // GRID, n % GRID))

    while TOTALMINECOUNT > 0:
        cell = Matrix[random.randrange(GRID * GRID)]
        if not cell.Mine:
            cell.Mine = True
            TOTALMINECOUNT -= 1

    for obj in Matrix:
        if not obj.Mine:
            obj.find_mines()

    Cont = True
    while Cont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Cont = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                cell = Matrix[mouseY // DIST * GRID + mouseX // DIST]
                if pygame.mouse.get_pressed()[2]:
                    cell.Marked = not cell.Marked
                if pygame.mouse.get_pressed()[0]:
                    cell.Unc = True
                    if cell.Mine_Count_Neighbourhood == 0 and not cell.Mine:
                        fill_func(mouseY // DIST, mouseX // DIST)
                    if cell.Mine:
                        for obj in Matrix:
                            obj.Unc = True

        for obj in Matrix:
            obj.show()
        pygame.display.flip()

    pygame.quit()
