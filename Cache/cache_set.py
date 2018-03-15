class CacheSet:
    def __init__(self, maxsize):
        self.__data = {}
        self.__maxsize = maxsize

    def __getitem__(self, key):
        """
        Implements the indexing syntax for reading, e.g. res = cache[key]
        Returns value if key in self.__data
        else defaults to None
        """
        return self.__data.get(key, None)

    def __setitem__(self, key, value):
        """
        Implements the indexing syntax for writing, e.g. cache[key] = value
        """
        self.__data[key] = value

    def pop(self, key):
        self.__data.pop(key)

    def is_full(self):
        return len(self.__data.keys()) == self.__maxsize

    def __repr__(self):
        return 'Contents: {}, current size: {}, max size: {}'.format(
            self.__data, len(self.__data), self.__maxsize
        )
