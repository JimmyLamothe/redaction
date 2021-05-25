""" Tests for text utilities """

from text_utilities import *

def test_strip_trailing_newline():
    """ Removes last character recursively while it's a new line | str -> str """
    t1 = '\n\rsfdgadfg adfgasfdg \n'
    t2 = ''
    t3 = '\n\rsfdgadfg adfgasfdg '
    t4 = '\r\n'
    t5 = 'ddd\nsdfgdf\n\n\n\n'
    assert strip_trailing_newline(t1) == '\n\rsfdgadfg adfgasfdg '
    assert strip_trailing_newline(t2) == ''
    assert strip_trailing_newline(t3) == '\n\rsfdgadfg adfgasfdg '
    assert strip_trailing_newline(t4) == ''
    assert strip_trailing_newline(t5) == 'ddd\nsdfgdf'
