""" Text utilities

Any function that manipulates strings and isn't specific to an object or class
goes here.
"""

def strip_trailing_newline(string):
    """ Removes last character recursively while it's a new line | str -> str """
    try:
        if string[-1] in ['\n','\r']:
            return strip_trailing_newline(string[:-1])
        return string
    except IndexError:
        return string
