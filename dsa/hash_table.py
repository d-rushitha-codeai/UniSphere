
class HashTable:
    """Custom hash table using separate chaining."""

    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]

    def _hash(self, key):
        hash_value = 0

        for character in str(key):
            hash_value = (
                hash_value * 31 + ord(character)
            ) % self.capacity

        return hash_value

    def insert(self, key, value):
        index = self._hash(key)

        for item in self.buckets[index]:
            if item[0] == key:
                item[1] = value
                return

        self.buckets[index].append([key, value])
        self.size += 1

        if self.size / self.capacity >= 0.75:
            self._resize()

    def search(self, key):
        index = self._hash(key)

        for item in self.buckets[index]:
            if item[0] == key:
                return item[1]

        return None

    def delete(self, key):
        index = self._hash(key)

        for item in self.buckets[index]:
            if item[0] == key:
                self.buckets[index].remove(item)
                self.size -= 1
                return True

        return False

    def _resize(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for key, value in bucket:
                self.insert(key, value)
