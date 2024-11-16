import pytest
from User import User

def test_user_initialization():
    user = User(id=1, username="testuser", password="password123")
    
    assert user.id == 1
    assert user.username == "testuser"
    assert user.password == "password123"

def test_user_str():
    user = User(id=1, username="testuser", password="password123")
    
    user_str = str(user)
    expected_str = "User(id=1, username=testuser)"
    assert user_str == expected_str