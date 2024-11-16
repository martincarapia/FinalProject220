import pytest
from User import User
from Clock import Clock

def test_user_initialization():
    user = User(id=1, username="testuser", password="password123")
    
    assert user.id == 1
    assert user.username == "testuser"
    assert user.password == "password123"
    assert isinstance(user.clock, Clock)

def test_user_str():
    user = User(id=1, username="testuser", password="password123")
    
    user_str = str(user)
    expected_str = "ID: 1, Username: testuser, Password: password123"
    assert user_str == expected_str