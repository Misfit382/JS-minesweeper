"""Testy modułu spam."""
import pytest
import main


def test_1():
    if main.check_grid(5, 7, 10):
        assert True


def test_2():
    if main.Assets.loadfile("./Cells/cell1.gif", 500 // 10):
        assert True


if __name__ == '__main__':
    pytest.main()
