#!/usr/bin/env python

"""Tests for `focusedme` package."""

import pytest
import focusedme
from focusedme import util

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