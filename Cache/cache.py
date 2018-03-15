from .cache_set import CacheSet
from threading import Lock

class Cache:
    """
    Implements the top level cache interface
    """
    def __init__(self, associativity, number_sets, key_type, value_type, replacement_policy):
        
        self.number_sets = number_sets
        self.associativity = associativity
        self.key_type = key_type
        self.value_type = value_type
        self.replacement_policy = replacement_policy

        self.locks = [
            Lock() for i in range(self.number_sets)
        ]

        self.__setup_cache()

    def __setup_cache(self):

        self.sets = [
            CacheSet(maxsize=self.associativity)
            for i in range(self.number_sets)
        ]

        self.replacement_policies = [
            self.replacement_policy()
            for i in range(self.number_sets)
        ]

    def __setitem__(self, key, value):
        """
        Implements the c[key] = value interface
        """
        key_check = self.is_valid_arg_type(key)
        value_check = self.is_valid_ret_type(value)

        if not key_check:
            raise KeyError('Key \'{}\' is of wrong type, is: {}, expected: {}'
                                .format(key, self.get_types(key, self.key_type), self.key_type))

        elif not value_check:
            raise ValueError('Value \'{}\' is of wrong type, is: {}, expected: {}'
                                    .format(value, self.get_types(value, self.value_type), self.value_type))

        else:
            h = hash(key) % self.number_sets

            with self.locks[h]:
                if self.sets[h].is_full():
                    pop_key = self.replacement_policies[h].select_pop_item()
                    self.sets[h].pop(pop_key)

                self.sets[h][key] = value
                self.replacement_policies[h].update_on_write(key, value)


    def __getitem__(self, key):
        """
        Implements the value = c[key] interface
        """
        key_check = self.is_valid_arg_type(key)

        if not key_check:
            raise KeyError('Key \'{}\' is of wrong type, is: {}, expected: {}'
                                .format(key, self.get_types(key, self.key_type), self.key_type))

        else:
            h = hash(key) % self.number_sets

            with self.locks[h]:
                value = self.sets[h][key]
                self.replacement_policies[h].update_on_read(key, value)
                return value


    def get_types(self, arg, ref):
        """
        Used to get the type of 'arg' in a convenient manner
        This is used in the key and value runtime type-checking
        """
        if type(ref) is tuple: #multiple arguments
            if type(arg) is tuple:
                return tuple(type(v) for v in arg)
            else:
                return type(arg)
        else:
            if type(arg) is tuple and len(arg) == 1:
                return type(arg[0])
            else:
                return type(arg)

    def is_valid_arg_type(self, args):
        """
        Used to check that wrapped function input is of correct type
        Input: Any object
        Output: Boolean
        """
        return self.get_types(args, self.key_type) == self.key_type

    def is_valid_ret_type(self, function_result):
        """
        Used to check that wrapped function output is of correct type
        Input: Any object
        Output: Boolean
        """
        return self.get_types(function_result, self.value_type) == self.value_type

    def __repr__(self):
        return 'Cache contents\n' +  \
            ''.join([
                '   Set {} - {}\n'.format(str(i), repr(s))
                for i, s in enumerate(self.sets)
            ])

    def clear(self):
        self.__setup_cache()