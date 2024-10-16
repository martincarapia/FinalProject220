class User:
    def __init__(self, id: int, username: str, password: str, timecard: object, last_action: str, is_admin: bool):
        """Initiate info for user with also a timecard object"""
        self.id = id
        self.username = username
        self.password = password
        # Will hold the timecard class to get total hours and when clocked
        self.timecard = timecard
        # Last two attributes may not be needed
        self.last_action = last_action
        self.is_admin = is_admin
    
    def __str__(self):
        return f"ID: {self.id}, Username: {self.username}, Password: {self.password}, Total hours: {self.timecard.total_hours}"