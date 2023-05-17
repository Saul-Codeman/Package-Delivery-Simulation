class Truck:
    def __init__(self):
        self.carrying_capacity = 16
        self.speed = 18
        self.driver = False
        self.packages = []
        # Initial WGU address
        self.location = "4001 South 700 East"
        # Information for metrics
        self.departure_time = 8
        self.return_time = None
        self.miles_traveled = 0
        self.travel_time = 0

    def add_package(self, package):
        self.carrying_capacity -= 1
        self.packages.append(package)

    def deliver_package(self, package):
        self.carrying_capacity += 1
        self.packages.remove(package)

    def assign_driver(self):
        self.driver = True

    def remove_driver(self):
        self.driver = False

    def print_metrics(self, truck_number):
        print("-------------------------------")
        print(f"Truck {truck_number} Metrics")
        print(f"Departure Time: {self.format_time_am_pm(self.departure_time)}")
        if self.return_time == None:
            print("Return Time: Has not arrived")
        else:
            print(f"Return Time: {self.format_time_am_pm(self.return_time)}")
        print(f"Travel Time: {self.format_time(self.travel_time)} hours")
        print(f"Miles Traveled: {self.miles_traveled} miles")
        print(f"Truck Location: {self.location}")

    def format_time_am_pm(self, hours_float):
        # Calculate hour and minutes
        hours = int(hours_float)
        minutes = int((hours_float - hours) * 60)

        # Calculate am or pm
        am_pm = "AM" if hours < 12 else "PM"

        # Adjust hour for 12-hour format
        hours %= 12
        if hours == 0:
            hours = 12

        return f"{hours:02d}:{minutes:02d} {am_pm}"
    def format_time(self, hours_float):
        # Calculate hour and minutes
        hours = int(hours_float)
        minutes = int((hours_float - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"
    #def __str__(self):

