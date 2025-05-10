#!/usr/bin/env python

"""Tests for `focusedme` package."""

import pytest

from focusedme import util
from focusedme.__main__ import Config


@pytest.fixture(scope="function")
def call_in_app_path() -> str:
    return util.in_app_path("test.txt")


def test_in_app_path(call_in_app_path: str) -> None:
    import pathlib

    assert call_in_app_path == str(pathlib.Path().absolute()) + "/focusedme/test.txt"


@pytest.fixture(scope="function")
def call_from_resource() -> str:
    return util._from_resource("test.txt")


def test_from_resource(call_from_resource: str) -> None:
    import pathlib

    assert call_from_resource == str(pathlib.Path().absolute()) + "/focusedme/test.txt"


@pytest.fixture(scope="function")
def call_load_init() -> tuple[dict[str, int], dict[str, str]]:
    return Config.load_init()


def test_load_init(call_load_init: tuple[dict[str, int], dict[str, str]]) -> None:
    time_args, sound_args = call_load_init
    assert time_args["focus_time"] == 25
    assert time_args["short_break"] == 5
    assert time_args["long_break"] == 25
    assert time_args["num_rounds"] == 3
    assert sound_args["sound"]
