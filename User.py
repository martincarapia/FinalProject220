from Clock import Clock

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
        # Will hold the Clock class instance to get total hours and when clocked
        self.clock = Clock()

    def __str__(self):
        """
        Return a string representation of the User instance.

        Returns:
            str: A string containing the user's ID, username, and password.
        """
        return f"ID: {self.id}, Username: {self.username}, Password: {self.password}"