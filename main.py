# Name: Sean Roberts
# Student ID: 010802895

import csv
from hash_map import HashMap
from package import Package
from truck import Truck
from travel_time import Time

# Read from addresses
with open('Data/addresses.csv') as addresses:
    CSV_addresses = csv.reader(addresses)
    # Hold to read later in program
    CSV_addresses = list(CSV_addresses)

# Read from distances
with open('Data/distances.csv') as distances:
    CSV_distances = csv.reader(distances)
    # Hold to read later in program
    CSV_distances = list(CSV_distances)

# Read from packages
with open('Data/packages.csv') as packages:
    next(packages)
    CSV_packages = csv.reader(packages)
    # Hold to read later in program
    CSV_packages = list(CSV_packages)

# Create hashmap for packages
packages_hash = HashMap()

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

# Get the ID of the address in the addresses.csv file
def get_addressID(address):
    for row in CSV_addresses:
        if address in row[2]:
            return int(row[0])
    # Detects an error in the packages CSV where 3575 W Valley Central Station bus Loop was 3575 W Valley Central Sta bus Loop
    print(f"Warning: Address '{address}' not found in CSV_addresses")
    return None

# Get the address of the ID in the addresses.csv file
def get_address(addressID):
    for row in CSV_addresses:
        if str(addressID) in row[0]:
            return row[2]

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

        # Find the nearest package using nearest neighbor algorithm
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
def deliver_packages(truck, time, stop_time):
    # Check if truck can begin
    if time.time <= stop_time:
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
        while remaining_packages and time.time <= stop_time:
            # Next package to be delivered
            package = packages_hash.get(remaining_packages[0])
            package_location = get_addressID(package.address)
            # Distance to package location
            distance = get_distance(truck_location, package_location)
            # Estimated time to deliver the next package
            estimated_delivery_time = time.time + distance / truck.speed
            # Check if estimated_delivery_time is greater than stop_time
            if estimated_delivery_time > stop_time:
                break
            # Add distance to miles traveled
            truck.miles_traveled += distance
            # Update the time
            time.update_time(distance, truck.speed)
            truck.travel_time = time.time - truck.departure_time
            # Move the truck location to the package location
            truck_location = package_location
            # Update truck.location parameter
            truck.location = get_address(truck_location)
            # Change package status to Delivered
            package.deliver(time.time)
            # Remove package from truck
            remaining_packages.remove(remaining_packages[0])

        # Return to WGU
        if not remaining_packages:
            distance = get_distance(truck_location, get_addressID("4001 South 700 East"))
            truck.miles_traveled += distance
            time.update_time(distance, truck.speed)
            truck.return_time = time.time
            truck.travel_time = time.time - truck.departure_time
            truck_location = "4001 South 700 East"
            truck.location = truck_location

# Converts time given by user to a float
def time_to_float(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours + minutes / 60.0


# Deliver packages for the trucks with the time provided by the user
def run_with_stop_time(stop_time):
    # Create trucks
    truck1 = Truck()
    truck2 = Truck()
    truck3 = Truck()

    # Fill trucks
    truck1.packages = ["1", "2", "13", "14", "15", "16", "19", "20", "21", "29", "30", "34", "37", "40"]
    truck2.packages = ["3", "6", "18", "25", "26", "28", "31", "32", "36", "38"]
    truck3.packages = ["4", "5", "7", "8", "9", "10", "11", "12", "17", "22", "23", "24", "27", "33", "35", "39"]

    # Reset package status
    for i in range(1, 41):
        packages_hash.get(str(i)).status = "At Hub"
    # Instantiate time objects to keep track of truck delivery times
    time1 = Time()
    time2 = Time()

    # Truck 1 leaves at 8:00
    deliver_packages(truck1, time1, stop_time)
    # Truck 2 leaves at 9:05
    time2.time = 9.084
    deliver_packages(truck2, time2, stop_time)

    # Prevent truck 3 from going out if time stops before going out for delivery
    if stop_time >= time1.time or stop_time >= time2.time:
        # Determine which truck arrived first to begin truck 3 delivery
        if time1.time > time2.time:
            # Have truck wait until 10:30 to deliver next package
            if time2.time <= 10.34:
                time2.time = 10.34
                packages_hash.get("9").address = "410 S State St"
                deliver_packages(truck3, time2, stop_time)
            else:
                packages_hash.get("9").address = "410 S State St"
                deliver_packages(truck3, time2, stop_time)
        else:
            # Have truck wait until 10:15 to deliver next package
            if time1.time <= 10.34:
                packages_hash.get("9").address = "410 S State St"
                time1.time = 10.34
                deliver_packages(truck3, time1, stop_time)
            else:
                packages_hash.get("9").address = "410 S State St"
                deliver_packages(truck3, time1, stop_time)

    # Print Truck metrics
    truck1.print_metrics(1)
    truck2.print_metrics(2)
    truck3.print_metrics(3)
    print("-------------------------------")
    print(f"Combined Mileage: {truck1.miles_traveled + truck2.miles_traveled + truck3.miles_traveled} miles")
    print(f"Total time traveled: {truck1.format_time(truck3.travel_time + truck2.travel_time + truck1.travel_time)} hours")


# Beginning of user interface
# Got inspiration for user interface from Josh Madakor on Youtube
print("Western Governors University Parcel Service")
print("Delivery complete for all trucks!")
# Stop time used and packages delivered
stop_time = Time()
stop_time.time = 18
run_with_stop_time(stop_time.time)
# Allows the user to interact with the program and perform lookups and check times
while True:
    print()
    user_choice = input("What would you like to check?\n"
                        "t - Package and truck status at given time\n"
                        "p - Lookup package by ID\n"
                        "a - Lookup package by address\n"
                        "d - Lookup package by deadline\n"
                        "c - Lookup package by city\n"
                        "z - Lookup package by zip code\n"
                        "w - Lookup package by weight\n"
                        "s - Lookup package by status\n"
                        "e - exit\n"
                        "> ")
    if user_choice.lower() == "t":
        print()
        # Stop time provided by user to get a snapshot of the trucks and packages at the time
        stop = time_to_float(input("What time would you like to check (HH:mm, Example: 14:00)? "))
        stop_time.time = stop
        run_with_stop_time(stop_time.time)
        packages_hash.print_all_packages()
    elif user_choice.lower() == "p":
        print()
        package_id = input("Please pick a package ID (1-40) to lookup. ")
        print(packages_hash.get(package_id))
    elif user_choice.lower() == "a":
        package_address = input("Please enter a package address to lookup. ")
        packages_with_address = []
        for i in range(1, 41):
            if packages_hash.get(str(i)).address == package_address:
                packages_with_address.append(packages_hash.get(str(i)))
        for package in packages_with_address:
            print(str(package))
    elif user_choice.lower() == "d":
        package_deadline = input("Please enter a package deadline to lookup. ")
        packages_with_deadline = []
        for i in range(1, 41):
            if packages_hash.get(str(i)).deadline == package_deadline:
                packages_with_deadline.append(packages_hash.get(str(i)))
        for package in packages_with_deadline:
            print(str(package))
    elif user_choice.lower() == "c":
        package_city = input("Please enter a city to lookup. ")
        packages_with_city = []
        for i in range(1, 41):
            if packages_hash.get(str(i)).city == package_city:
                packages_with_city.append(packages_hash.get(str(i)))
        for package in packages_with_city:
            print(str(package))
    elif user_choice.lower() == "z":
        package_zip = input("Please enter a zip code to lookup. ")
        packages_with_zip = []
        for i in range(1, 41):
            if packages_hash.get(str(i)).zip == package_zip:
                packages_with_zip.append(packages_hash.get(str(i)))
        for package in packages_with_zip:
            print(str(package))
    elif user_choice.lower() == "w":
        package_weight = input("Please enter a package weight (in Kilos) to lookup. ")
        packages_with_weight = []
        for i in range(1, 41):
            if packages_hash.get(str(i)).weight == package_weight:
                packages_with_weight.append(packages_hash.get(str(i)))
        for package in packages_with_weight:
            print(str(package))
    elif user_choice.lower() == "s":
        package_status = input("Please enter a package status to lookup (En Route, At Hub, Delivered). ")
        packages_with_status = []
        for i in range(1, 41):
            if packages_hash.get(str(i)).status.lower() == package_status.lower():
                packages_with_status.append(packages_hash.get(str(i)))
        for package in packages_with_status:
            print(str(package))
    elif user_choice.lower() == "e":
        break
    else:
        print("Invalid choice. Please try again.")
        print()