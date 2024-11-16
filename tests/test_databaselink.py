import pytest
import sqlite3
import os
from databaselink import get_db_connection, setup_database, add_user, get_user

# Define a test database file
TEST_DB = 'test_time_tracking.db'

@pytest.fixture(scope='module')
def db_connection():
    # Setup: Create a test database
    conn = sqlite3.connect(TEST_DB)
    yield conn
    # Teardown: Close the connection and remove the test database
    conn.close()
    os.remove(TEST_DB)

@pytest.fixture(scope='module')
def setup_db(db_connection):
    # Setup the database schema
    setup_database()
    yield
    # Teardown: No specific teardown needed as the database file will be removed

def test_add_user(db_connection, setup_db):
    # Test adding a user
    add_user('testuser', 'password123')
    user = get_user('testuser')
    assert user is not None
    assert user[1] == 'testuser'
    assert user[2] == 'password123'

def test_add_duplicate_user(db_connection, setup_db):
    # Test adding a duplicate user
    add_user('duplicateuser', 'password123')
    with pytest.raises(sqlite3.IntegrityError):
        add_user('duplicateuser', 'password123')

def test_get_nonexistent_user(db_connection, setup_db):
    # Test retrieving a non-existent user
    user = get_user('nonexistentuser')
    assert user is None