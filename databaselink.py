import sqlite3
import re
from datetime import datetime

def get_db_connection():
    """
    Establish a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database.
    """
    conn = sqlite3.connect('time_tracking.db')
    return conn

def sanitize_input(input_string):
    """
    Sanitize the input string by removing any potentially harmful characters.

    Args:
        input_string (str): The input string to sanitize.

    Returns:
        str: The sanitized input string.
    """
    return re.sub(r'[^\w\s]', '', input_string)

def setup_database():
    """
    Set up the database by creating the necessary tables if they do not exist.
    """
    conn = get_db_connection()
    c = conn.cursor()
    
    # Create the users table
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    
    # Create the clock_records table
    c.execute('''
    CREATE TABLE IF NOT EXISTS clock_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        clock_in_time TEXT,
        clock_out_time TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')
    
    conn.commit()
    conn.close()

def add_user(username, password):
    """
    Add a new user to the users table.

    Args:
        username (str): The username of the new user.
        password (str): The password of the new user.
    """
    username = sanitize_input(username).strip()
    password = sanitize_input(password).strip()
    
    if not username or not password:
        raise ValueError("Username and password cannot be blank or contain only whitespace/newline characters.")
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def get_user(username):
    """
    Retrieve a user from the users table by username.

    Args:
        username (str): The username of the user to retrieve.

    Returns:
        tuple: A tuple containing the user's information, or None if the user does not exist.
    """
    username = sanitize_input(username)
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def add_clock_record(user_id, clock_in_time, clock_out_time=None):
    """
    Add a new clock record to the clock_records table.

    Args:
        user_id (int): The ID of the user.
        clock_in_time (str): The clock-in time.
        clock_out_time (str, optional): The clock-out time. Defaults to None.
    """
    clock_in_time = datetime.strptime(clock_in_time, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    if clock_out_time:
        clock_out_time = datetime.strptime(clock_out_time, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO clock_records (user_id, clock_in_time, clock_out_time) VALUES (?, ?, ?)', 
              (user_id, clock_in_time, clock_out_time))
    conn.commit()
    conn.close()

def update_clock_out(user_id, clock_out_time):
    """
    Update the clock-out time for the most recent clock-in record of the user.

    Args:
        user_id (int): The ID of the user.
        clock_out_time (str): The clock-out time.
    """
    clock_out_time = datetime.strptime(clock_out_time, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE clock_records SET clock_out_time = ? WHERE user_id = ? AND clock_out_time IS NULL', 
              (clock_out_time, user_id))
    conn.commit()
    conn.close()

def get_clock_records(user_id):
    """
    Retrieve all clock records for a user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of tuples containing the clock records.
    """
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT clock_in_time, clock_out_time FROM clock_records WHERE user_id = ?', (user_id,))
    records = c.fetchall()
    conn.close()
    return records

def has_active_clock_in(user_id):
    """
    Check if the user has an active clock-in record without a clock-out time.

    Args:
        user_id (int): The ID of the user.

    Returns:
        bool: True if there is an active clock-in record, False otherwise.
    """
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id FROM clock_records WHERE user_id = ? AND clock_out_time IS NULL', (user_id,))
    active = c.fetchone() is not None
    conn.close()
    return active