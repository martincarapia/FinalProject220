import pytest
from datetime import datetime, timedelta
from Clock import Clock

def test_clock_in():
    clock = Clock()
    clock_in_time = clock.clock_in()
    assert isinstance(clock_in_time, datetime)

def test_clock_out_without_clock_in():
    clock = Clock()
    with pytest.raises(ValueError, match="Operation not allowed. Please clock in first."):
        clock.clock_out()

def test_clock_out():
    clock = Clock()
    clock.clock_in()
    session_time = clock.clock_out()
    assert isinstance(session_time, timedelta)

def test_clock_in_twice():
    clock = Clock()
    clock.clock_in()
    with pytest.raises(ValueError, match="Operation not allowed. Please clock out first."):
        clock.clock_in()

def test_clock_out_twice():
    clock = Clock()
    clock.clock_in()
    clock.clock_out()
    with pytest.raises(ValueError, match="Operation not allowed. Please clock in first."):
        clock.clock_out()