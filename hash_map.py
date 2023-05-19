# Hashmap developed using the video by Joe James "Python: Creating a HASHMAP using Lists"
# Link: https://www.youtube.com/watch?v=9HFbhPscPU0
class HashMap:
    def __init__(self):
        self.size = 64
        self.map = [None] * self.size

    # Gets the hash number given a key
    def get_hash(self, key):
        hash = 0
        for char in str(key):
            hash += ord(char)
        return hash % self.size

    # Adds the key value pair to the hashmap
    def add(self, key, value):
        key_hash = self.get_hash(key)
        key_value = [key, value]
        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.map[key_hash].append(key_value)
            return True

    # Gets the value from the hashmap given a key
    def get(self, key):
        key_hash = self.get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    # Deletes the key value pair given the key
    def delete(self, key):
        key_hash = self.get_hash(self, key)
        if self.map[key_hash] is None:
            return False
        for i in range(0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True

    # Prints the str of the item in the hashmap
    def print(self):
        for item in self.map:
            if item is not None:
                print(str(item))

    # Prints all of the packages in the hashmap
    def print_all_packages(self):
        IDs = [str(i) for i in range(1, 41)]
        for id in IDs:
            package = self.get(id)
            if package is not None:
                print(package)
            else:
                print(f"No package with ID: {id}")
