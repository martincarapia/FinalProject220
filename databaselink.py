import sqlite3

def get_db_connection():
    """
    Establish a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database.
    """
    conn = sqlite3.connect('time_tracking.db')
    return conn

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
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def add_clock_record(user_id, clock_in_time, clock_out_time):
    """
    Add a new clock record to the clock_records table.

    Args:
        user_id (int): The ID of the user.
        clock_in_time (str): The clock-in time.
        clock_out_time (str): The clock-out time.
    """
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO clock_records (user_id, clock_in_time, clock_out_time) VALUES (?, ?, ?)', 
                (user_id, clock_in_time, clock_out_time))
    conn.commit()
    conn.close()