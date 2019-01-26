import time


class CircularBuffer:
    def __init__(self, size, holding_time):
        self.dictionary = {}
        self.key_list = []
        self.timestamps = {}
        self.max_size = size
        self.max_holding_time = holding_time

    # sets the amount of key - value pairs that can be held by the buffer
    def set_size(self, size):
        self.max_size = size

    # sets the maximum duration in seconds for which tuples are allowed to be held in the buffer
    def set_holding_time(self, holding_time):
        self.max_holding_time = holding_time

    # adds a key - value pair to the buffer, if the buffer is full the least recently used key is removed
    def add(self, key, value):
        if len(self.key_list) >= self.max_size:
            self.delete(self.key_list[0])
        self.key_list.append(key)
        self.dictionary[key] = value
        self.timestamps[key] = time.time()

    # checks if requested key is still current enough, if not returns None else returns the value saved for that key
    def get(self, key):
        load_time = self.timestamps.get(key)
        if load_time:
            if (time.time() - load_time) > self.max_holding_time:
                self.delete(key)
        return self.dictionary.get(key)

    # removes the key - value pair from the buffer
    def delete(self, key):
        self.key_list.remove(key)
        del self.timestamps[key]
        del self.dictionary[key]

    # removes all data from the buffer
    def clear(self):
        self.dictionary.clear()
        self.key_list.clear()
        self.timestamps.clear()

    # sets the passed key to be the most recently used, relevant for the data removal if buffer is full
    def refresh(self, key):
        self.key_list.remove(key)
        self.key_list.append(key)
