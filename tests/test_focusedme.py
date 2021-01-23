#!/usr/bin/env python

"""Tests for `focusedme` package."""

import pytest
import focusedme
from focusedme import util
from focusedme.__main__ import Config

@pytest.fixture
def call_in_app_path():
    return util.in_app_path('test.txt')

def test_in_app_path(call_in_app_path):
    import pathlib
    
    assert call_in_app_path == str(pathlib.Path().absolute()) + '/focusedme/test.txt'

@pytest.fixture
def call_from_resource():
    return util._from_resource('test.txt')

def test_from_resource(call_from_resource):
    import pathlib

    assert call_from_resource == str(pathlib.Path().absolute()) + '/focusedme/test.txt'

@pytest.fixture
def call_load_init():
    return Config.load_init()

def test_load_init(call_load_init):
    assert call_load_init["focus_time"] == 25
    assert call_load_init["short_break"] == 5
    assert call_load_init["long_break"] == 25
    assert call_load_init["num_rounds"] == 3
    assert call_load_init["sound"] == True