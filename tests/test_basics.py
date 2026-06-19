import pytest
from calculator import *
from unittest.mock import patch
from app import main

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(10, 3) == 7

def test_multiply():
    assert multiply(4, 5) == 20

def test_divide():
    assert divide(5, 2) == 2.5

def test_add_negative():
    assert add(-5, -3) == -8

def test_multiply_zero():
    assert multiply(10, 0) == 0
