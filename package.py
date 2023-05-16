class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight, note=None):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        if note is None:
            self.note = 'No note'
        else:
            self.note = note
        self.status = "At Hub"
        self.on_truck = False
        self.delivered = False

    def status(self):
        if self.on_truck:
            self.status = "En Route"
        elif self.delivered:
            self.status = "Delivered"
        else:
            self.status = "At Hub"

    def place_on_truck(self):
        self.on_truck = True
        self.status = "En Route"

    def deliver(self):
        self.on_truck = False
        self.delivered = True
        self.status = "Delivered"

    def __str__(self):
        return f"Package ID: {self.id}, Address: {self.address}, City: {self.city}, State: {self.state}, Zip: {self.zip}, Deadline: {self.deadline}, Weight: {self.weight}, Note: {self.note}, Status: {self.status}"

