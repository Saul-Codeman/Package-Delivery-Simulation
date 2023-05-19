# Time class used to keep track of time while delivering packages
class Time:
    def __init__(self):
        # Time starts at 8am
        self.time = 8
    # Updates the time given miles traveled and speed of the truck
    def update_time(self, miles, speed):
        # Calculate the travel time in hours
        travel_time = miles/speed
        self.time += travel_time
        # Check if time is over 24 hours and adjust it
        if self.time > 24:
            self.time -= 24

    # Gives the string to print time
    def __str__(self):
        # Calculate hour and minutes
        hour = int(self.time)
        minutes = int((self.time - hour) * 60)
        # Calculate am or pm
        am_pm = "am" if self.time < 12 else "pm"
        # Adjust hour for 12-hour format
        hour %= 12
        if hour == 0:
            hour = 12
        return "{:02d}:{:02d} {}".format(hour, minutes, am_pm)

