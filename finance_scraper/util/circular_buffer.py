import time


class CircularBuffer:
    def __init__(self, size, holding_time):
        self.dictionary = {}
        self.key_list = []
        self.timestamps = {}
        self.max_size = size
        self.max_holding_time = holding_time

    def set_size(self, size):
        self.max_size = size

    def set_holding_time(self, holding_time):
        self.max_holding_time = holding_time

    def add(self, key, value):
        if len(self.key_list) >= self.max_size:
            self.delete(self.key_list[0])
        self.key_list.append(key)
        self.dictionary[key] = value
        self.timestamps[key] = time.time()

    def get(self, key):
        load_time = self.timestamps.get(key)
        if load_time:
            if (time.time() - load_time) > self.max_holding_time:
                self.delete(key)
        return self.dictionary.get(key)

    def delete(self, key):
        self.key_list.remove(key)
        del self.timestamps[key]
        del self.dictionary[key]

    def clear(self):
        self.dictionary.clear()
        self.key_list.clear()

    def refresh(self, key):
        self.key_list.remove(key)
        self.key_list.append(key)
