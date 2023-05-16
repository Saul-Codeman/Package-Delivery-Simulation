class Snapshot:
    def __init__(self):
        self.snapshots = {}

        def take_snapshot(self, time, truck, packages):
            # Creating a dictionary to hold snapshot information
            snapshot = {
                'time': time, #time provided by user
                'truck': truck.__str__(), #truck information to be checked
                'packages': packages # Packages to search
            }

            # Store the snapshot indexed by the time
            self.snapshots[time] = snapshot

        def get_snapshot(self, time):
            # Get the snapshot information at the requested time
            if time in self.snapshots:
                return self.snapshots[time]
            else:
                return "No snapshot available at this time."
