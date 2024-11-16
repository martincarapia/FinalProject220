from datetime import datetime

class Clock:
    """A class that allows the user to punch in and out and record the time spent."""

    def __init__(self):
        """
        Initialize the Clock instance with clock_in_time and clock_out_time set to None.
        """
        self.clock_in_time = None
        self.clock_out_time = None

    def clock_in(self):
        """
        Record the current time as the clock-in time.
        
        Raises:
            ValueError: If the user has already clocked in and not clocked out yet.
        
        Returns:
            datetime: The clock-in time.
        """
        if self.clock_in_time:
            raise ValueError("Operation not allowed. Please clock out first.")
        else:
            self.clock_in_time = datetime.now().replace(microsecond=0)
            return self.clock_in_time

    def clock_out(self):
        """
        Record the current time as the clock-out time and calculate the session time.
        
        Raises:
            ValueError: If the user has not clocked in yet or has already clocked out.
        
        Returns:
            timedelta: The duration of the session.
        """
        if not self.clock_in_time:
            raise ValueError("Operation not allowed. Please clock in first.")
        elif self.clock_out_time:
            raise ValueError("Operation not allowed. Please clock in first.")
        else:
            self.clock_out_time = datetime.now().replace(microsecond=0)
            session_time = self.clock_out_time - self.clock_in_time
            return session_time