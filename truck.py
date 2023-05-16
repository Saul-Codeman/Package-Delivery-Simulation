class Truck:
    def __init__(self):
        self.carrying_capacity = 16
        self.speed = 18
        self.driver = False
        self.miles_traveled = 0
        self.packages = []
        # Initial WGU address
        self.location = "4001 South 700 East"

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


    #def __str__(self):

