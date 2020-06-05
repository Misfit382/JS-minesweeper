"""Testy modułu main."""
import main
import unittest


class CellTest(unittest.TestCase):
    """Testy klasy cell."""

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
        self.assertFalse(self.cell.find_mines(0))


class TestAssets(unittest.TestCase):
    """Testy klasy Assets."""

    def setUp(self):
        self.assets = main.Assets()

    def test_load_file(self):
        path = "./Cells/cell1.gif"
        distance = 500 // 10
        self.assertTrue(self.assets.loadfile(path, distance))


class TestColors(unittest.TestCase):
    """Testy klasy od kolorów."""

    def setUp(self):
        self.color = main.Colors()

    def test_green(self):
        self.assertEqual(self.color.GREEN, (0, 128, 0))

    def test_WHITE(self):
        self.assertEqual(self.color.WHITE, (255, 255, 255))


if __name__ == '__main__':
    unittest.main()
