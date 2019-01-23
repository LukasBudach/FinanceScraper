class CircularBuffer:
    def __init__(self, size):
        self.dictionary = {}
        self.key_list = []
        self.max_size = size

    def set_size(self, size):
        self.max_size = size

    def add(self, key, value):
        if len(self.key_list) >= self.max_size:
            print('Removed ' + self.key_list[0] + ' from buffer')
            del self.dictionary[self.key_list.pop(0)]
        self.key_list.append(key)
        self.dictionary[key] = value

    def get(self, key):
        return self.dictionary.get(key)

    def clear(self):
        self.dictionary.clear()
        self.key_list.clear()

    def refresh(self, key):
        self.key_list.remove(key)
        self.key_list.append(key)
