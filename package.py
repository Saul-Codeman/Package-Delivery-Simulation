class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight, note=None):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        # Check if the package has a note
        if note is None:
            self.note = 'No note'
        else:
            self.note = note
        self.status = "At Hub"
        self.on_truck = False
        self.delivered = False
        self.time_delivered = None

    # Give the status value a string
    def status(self):
        if self.on_truck:
            self.status = "En Route"
        elif self.delivered:
            self.status = "Delivered"
        else:
            self.status = "At Hub"

    # Changes the package status to en route
    def place_on_truck(self):
        self.on_truck = True
        self.status = "En Route"

    # Changes the package status to delivered and gives a time
    def deliver(self, time):
        self.on_truck = False
        self.delivered = True
        self.status = "Delivered"
        self.time_delivered = time

    # Formats time
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

    # String value to print packages
    def __str__(self):
        # ANSI color codes
        RED = '\033[91m'
        YELLOW = '\033[93m'
        GREEN = '\033[92m'
        END = '\033[0m'

        if self.status == 'At Hub':
            status = f'{RED}{self.status}{END}'
        elif self.status == 'En Route':
            status = f'{YELLOW}{self.status}{END}'
        elif self.status == 'Delivered':
            status = f'{GREEN}{self.status} at {self.format_time_am_pm(self.time_delivered)}{END}'
        else:
            status = self.status

        return f"Package ID: {self.id}, Status: {status}, Address: {self.address}, City: {self.city}, State: {self.state}, Zip: {self.zip}, Deadline: {self.deadline}, Weight: {self.weight}, Note: {self.note}"

