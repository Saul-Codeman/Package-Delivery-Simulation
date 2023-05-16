import csv
from hash_map import HashMap
from package import Package
from truck import Truck

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

print(packages_hash.get("1"))

# Create trucks
truck1 = Truck()
truck2 = Truck()
truck3 = Truck()

