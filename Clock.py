from datetime import datetime

class Clock:
    """A class that will allow the user to punch in and out and record the time spent."""
    def __init__(self):
        self.punch_in_time = None
        self.punch_out_time = None

    def punch_in(self):
        if self.punch_in_time != None:
            print("Already punched in at:", self.punch_in_time)
        else:
            self.punch_in_time = datetime.now().replace(microsecond=0)
            print("Punched in at:", self.punch_in_time)

    def punch_out(self):
        if self.punch_in_time == None:
            print("You need to punch in first!")
        elif self.punch_out_time != None:
            print("Already punched out at:", self.punch_out_time)
        else:
            self.punch_out_time = datetime.now().replace(microsecond=0)
            session_time = self.punch_out_time - self.punch_in_time
            return session_time
    