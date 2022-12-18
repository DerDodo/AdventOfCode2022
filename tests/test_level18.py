from file_util import read_input_file, read_input_file_id
from level18 import level18


def test_level18():
    _surface_area, _outer_surface_area = level18(read_input_file(18))
    assert _surface_area == 64
    assert _outer_surface_area == 58


def test_level18():
    _surface_area, _outer_surface_area = level18(read_input_file_id(18, 2))
    assert _surface_area == 108
    assert _outer_surface_area == 90
