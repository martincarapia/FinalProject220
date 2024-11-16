from datetime import datetime
import databaselink as database

class User:
    """
    A class to represent a user with an associated timecard object.
    """

    def __init__(self, id: int, username: str, password: str):
        """
        Initialize the User instance with an ID, username, password, and a timecard object.

        Args:
            id (int): The unique identifier for the user.
            username (str): The username of the user.
            password (str): The password of the user.
        """
        self.id = id
        self.username = username
        self.password = password

    def clock_in(self):
        """
        Handle the clock-in process by recording the current time in the database.
        """
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        database.add_clock_record(self.id, now)

    def clock_out(self):
        """
        Handle the clock-out process by recording the current time in the database.
        """
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        database.update_clock_out(self.id, now)

    def get_total_hours(self):
        """
        Calculate the total hours worked by the user.

        Returns:
            float: The total hours worked.
        """
        records = database.get_clock_records(self.id)
        total_hours = 0
        for record in records:
            if record[1]:
                clock_in = datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S')
                clock_out = datetime.strptime(record[1], '%Y-%m-%d %H:%M:%S')
                total_hours += (clock_out - clock_in).total_seconds() / 3600
        return total_hours
    
    def __str__(self):
        """
        Return a string representation of the User instance.
        """
        return f"User(id={self.id}, username={self.username})"
