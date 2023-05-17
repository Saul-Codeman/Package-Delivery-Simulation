import csv
from hash_map import HashMap
from package import Package
from truck import Truck
from travel_time import Time

# Read from addresses
with open('Data/addresses.csv') as addresses:
    CSV_addresses = csv.reader(addresses)
    CSV_addresses = list(CSV_addresses)

# Read from distances
with open('Data/distances.csv') as distances:
    CSV_distances = csv.reader(distances)
    CSV_distances = list(CSV_distances)

# Read from packages
with open('Data/packages.csv') as packages:
    next(packages)
    CSV_packages = csv.reader(packages)
    CSV_packages = list(CSV_packages)

# Create hashmap for packages
packages_hash = HashMap()
# Create hashmap for time and packages or truck
snapshot_hash = HashMap()

# Add packages to hash table
for row in CSV_packages:
    id = row[0]
    address = row[1]
    city = row[2]
    state = row[3]
    zip = row[4]
    deadline = row[5]
    weight = row[6]
    note = row[7]
    # Create package object
    package = Package(id, address, city, state, zip, deadline, weight, note)
    # Insert package into hash table
    packages_hash.add(id, package)

# Create trucks
truck1 = Truck()
truck2 = Truck()
truck3 = Truck()

# Fill trucks
truck1.packages = ["1", "13", "14", "15", "16", "20", "29", "30", "31", "34", "37", "40"]
truck2.packages = ["3", "6", "12", "17", "18", "19", "21", "22", "23", "24", "26", "27", "35", "36", "38", "39"]
truck3.packages = ["2", "4", "5", "6", "7", "8", "9", "10", "11", "25", "28", "32", "33"]

# Instantiate time objects to keep track of truck delivery times
time1 = Time()
time2 = Time()

# Get the ID of the address in the addresses.csv file
def get_addressID(address):
    for row in CSV_addresses:
        if address in row[2]:
            return int(row[0])
    # Detects an error in the packages CSV where 3575 W Valley Central Station bus Loop was 3575 W Valley Central Sta bus Loop
    print(f"Warning: Address '{address}' not found in CSV_addresses")
    return None

# Get distance between two addresses. Will likely use truck.location and package.address
def get_distance(sourceID, destinationID):
    distance = CSV_distances[sourceID][destinationID]
    if distance == '':
        distance = CSV_distances[destinationID][sourceID]
    return float(distance)

# Sorts the packages on the truck using the nearest neighbor algorithm
def sort_packages(truck):
    # Create a copy of trucks.packages to use to sort the order for delivery
    remaining_packages = truck.packages[:]
    # Create an empty list to hold the packages being sorted
    sorted_packages = []
    # Truck's current location at WGU
    current_location = get_addressID(truck.location)

    while remaining_packages:
        nearest_package = None
        shortest_distance = float('inf')

        # Find the nearest package using nearest neighbor
        for ID in remaining_packages:
            package = packages_hash.get(ID)
            package_address = get_addressID(package.address)
            distance = get_distance(current_location, package_address)
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_package = ID
        remaining_packages.remove(nearest_package)
        sorted_packages.append(nearest_package)
        current_location = get_addressID(packages_hash.get(nearest_package).address)

    # Replace truck.packages with the sorted packages list
    truck.packages = sorted_packages

# Package delivery
def deliver_packages(truck, time):
    # Sort the trucks packages
    sort_packages(truck)
    # Create a copy of trucks.packages to deliver the packages
    remaining_packages = truck.packages[:]
    # Truck starting location at WGU
    truck_location = get_addressID(truck.location)
    # Set start time of truck departure
    truck.departure_time = time.time
    # Change all package status' to En Route
    for id in remaining_packages:
        package = packages_hash.get(id)
        package.place_on_truck()

    # Go through all packages in truck
    while remaining_packages:
        # Next package to be delivered
        package = packages_hash.get(remaining_packages[0])
        package_location = get_addressID(package.address)
        # Distance to package location
        distance = get_distance(truck_location, package_location)
        # Add distance to miles traveled
        truck.miles_traveled += distance
        #
        # print(f"{truck_location} + {distance} + {package_location}")
        # Update the time
        time.update_time(distance, truck.speed)
        truck.travel_time = time.time - 8
        # Move the truck location to the package location
        truck_location = package_location
        # Change package status to Delivered
        package.deliver()
        # Remove package from truck
        remaining_packages.remove(remaining_packages[0])

    # Return to WGU
    distance = get_distance(truck_location, get_addressID("4001 South 700 East"))
    truck.miles_traveled += distance
    time.update_time(distance, truck.speed)
    truck.return_time = time.time
    truck.travel_time = time.time - truck.departure_time
    truck_location = "4001 South 700 East"
    truck.location = truck_location



truck1.print_metrics(1)
truck2.print_metrics(2)
truck3.print_metrics(3)
# Deliver packages for trucks 1 and 2
deliver_packages(truck1, time1)
deliver_packages(truck2, time2)
truck1.print_metrics(1)
truck2.print_metrics(2)
# Determine which truck arrived first to begin truck 3 delivery
if time1.time > time2.time:
    # Have truck wait until 10:15 to deliver next package
    deliver_packages(truck3, time2)
else:
    # Have truck wait until 10:15 to deliver next package
    deliver_packages(truck3, time1)
truck3.print_metrics(3)