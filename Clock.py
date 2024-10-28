from datetime import datetime
class Clock:
    """A class that will allow the user to punch in and out and record the time spent."""
    def punch_in():
        start_time = datetime.now()
        return start_time

    def punch_out():
        end_time = datetime.now()
        return None
