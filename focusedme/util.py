"""
This file was copied from
https://github.com/JaDogg/pydoro
to solve in app path references
"""

import os
import time
from typing import Callable


def every(delay: float, task: Callable[[], None]) -> None:
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        task()
        next_time += (time.time() - next_time) // delay * delay + delay


def in_app_path(path: str) -> str:
    import sys

    try:
        # Handle PyInstaller's special _MEIPASS attribute
        wd = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        return os.path.abspath(os.path.join(wd, path))
    except AttributeError:
        return _from_resource(path)


def _from_resource(path: str) -> str:
    from pkg_resources import resource_filename

    res_path = resource_filename(__name__, path)
    if not os.path.exists(res_path):
        res_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), path
        )  # noqa: E501
    return res_path
