"""Testy modułu spam."""
import main
import unittest


class CellTest(unittest.TestCase):
    def setUp(self):
        self.cell = main.Cell(cell_row=1, cell_column=1, cell_mine=False, cell_uncovered_mine=False, cell_marked=False,
                              cell_mine_count_neighbourhood=0, cheat_mine=False)

    def test_marked(self):
        self.assertFalse(self.cell.cell_marked)

    def test_mine(self):
        self.assertFalse(self.cell.cell_mine)

    def test_cheat(self):
        self.assertFalse(self.cell.cheat_mine)

    def test_uncovered(self):
        self.assertFalse(self.cell.cell_uncovered_mine)

    def test_find_mines(self):
        matrix = []
        self.assertFalse(self.cell.find_mines(0, matrix))

    def test_fill_func(self):
        grid_size = 3
        matrix = main.init_matrix(grid_size)
        matrix[0].set_mine()

        main.fill_func(2, 2, 3, matrix)
        bool_matrix = [True, False, False,
                       False, False, False,
                       False, False, False]
        for i in range(grid_size * grid_size):
            self.assertEqual(
                matrix[i].cell_mine, bool_matrix[i])

    def test_fill_func_2(self):
        grid_size = 3
        matrix = main.init_matrix(grid_size)
        matrix[0].set_mine()
        matrix[4].set_mine()
        matrix[8].set_mine()
        mines_found = 0

        main.fill_func(2, 2, 3, matrix)
        bool_matrix = [True, False, False,
                       False, True, False,
                       False, False, True]
        for i in range(grid_size*grid_size):
            if bool_matrix[i]:
                mines_found += 1
        self.assertEqual(mines_found, 3)


class TestAssets(unittest.TestCase):
    def setUp(self):
        self.assets = main.Assets()

    def test_load_file(self):
        path = "./Cells/cell1.gif"
        distance = 500 // 10
        self.assertTrue(self.assets.loadfile(path, distance))


class TestColors(unittest.TestCase):
    def setUp(self):
        self.color = main.Colors()

    def test_green(self):
        self.assertEqual(self.color.GREEN, (0, 128, 0))

    def test_WHITE(self):
        self.assertEqual(self.color.WHITE, (255, 255, 255))


if __name__ == '__main__':
    unittest.main()
