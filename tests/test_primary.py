import pytest
from calculator import *
from unittest.mock import patch
from app import main


def test_multiply_zero():
    assert multiply(10, 0) == 0

def test_health(capsys):
    with patch(
        "sys.argv",
        ["app.py", "health"]
    ):
        exit_code = main()

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "ok" in captured.out

def test_invalid_function(capsys):
    with patch(
        "sys.argv",
        ["app.py", "power", "2", "3"]
    ):
        exit_code = main()

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "not found" in captured.out

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
