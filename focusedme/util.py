"""
This file was copied from
https://github.com/JaDogg/pydoro
to solve in app path references
"""

import os
import time


# Python program to print
# colored text and background
class Colors:
    """ Class proposed in https://www.geeksforgeeks.org/
    print-colors-python-terminal/
    Reset all colors with colors.reset;
    Two sub classes fg for foreground and bg for background;
    use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.greenalso, the generic bold, disable,
    underline, reverse, strike through,
    and invisible work with the main class i.e. colors.bold
    """

    reset = "\033[0m"
    bold = "\033[01m"
    disable = "\033[02m"
    underline = "\033[04m"
    reverse = "\033[07m"
    strikethrough = "\033[09m"
    invisible = "\033[08m"

    class fg:
        black = "\033[30m"
        red = "\033[31m"
        green = "\033[32m"
        orange = "\033[33m"
        blue = "\033[34m"
        purple = "\033[35m"
        cyan = "\033[36m"
        lightgrey = "\033[37m"
        darkgrey = "\033[90m"
        lightred = "\033[91m"
        lightgreen = "\033[92m"
        yellow = "\033[93m"
        lightblue = "\033[94m"
        pink = "\033[95m"
        lightcyan = "\033[96m"

    class bg:
        black = "\033[40m"
        red = "\033[41m"
        green = "\033[42m"
        orange = "\033[43m"
        blue = "\033[44m"
        purple = "\033[45m"
        cyan = "\033[46m"
        lightgrey = "\033[47m"


def every(delay, task):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        task()
        next_time += (time.time() - next_time) // delay * delay + delay


def in_app_path(path):
    import sys

    try:
        wd = sys._MEIPASS
        return os.path.abspath(os.path.join(wd, path))
    except AttributeError:
        return _from_resource(path)


def _from_resource(path):
    from pkg_resources import resource_filename

    res_path = resource_filename(__name__, path)
    if not os.path.exists(res_path):
        res_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), path
        )  # noqa: E501
    return res_path
