from datetime import datetime

class Clock:
    """A class that will allow the user to punch in and out and record the time spent."""
    def __init__(self):
        self.clock_in_time = None
        self.clock_out_time = None

    def clock_in(self):
        if self.clock_in_time != None:
            print("Already punched in at:", self.clock_in_time)
        else:
            self.clock_in_time = datetime.now().replace(microsecond=0)
            return self.clock_in_time

    def clock_out(self):
        if self.clock_in_time == None:
            print("You need to punch in first!")
        elif self.clock_out_time != None:
            print("Already punched out at:", self.clock_out_time)
        else:
            self.clock_out_time = datetime.now().replace(microsecond=0)
            session_time = self.clock_out_time - self.clock_in_time
            return session_time
    
