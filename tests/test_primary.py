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


def test_invalid_args(capsys):
    with patch(
        "sys.argv",
        ["app.py", "add", "k", "p"]
    ):
        exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Arguments must be numeric" in captured.out


def test_invalid_function(capsys):
    with patch(
        "sys.argv",
        ["app.py", "power", "2", "3"]
    ):
        exit_code = main()

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "not found" in captured.out

    
def test_invalid_arg_count(capsys):
    with patch(
        "sys.argv",
        ["app.py", "add", "2"]
    ):
        exit_code = main()

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Usage: python main.py <function> <num1> <num2>" in captured.out


def test_divide_by_zero(capsys):
    with patch("sys.argv", ["app.py", "div", "10", "0"]):
        exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Cannot divide by zero" in captured.out


def test_invalid_health_args(capsys):
    with patch(
        "sys.argv",
        ["app.py", "health", "2", "3"]
    ):
        exit_code = main()

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Usage: python main.py <function> <num1> <num2>" in captured.out