import warnings
from collections import namedtuple, deque

import numpy as np


class LogisticMapGenerator:

    ValueRange = namedtuple('ValueRange', 'min max')

    # Global Params
    depth_range = ValueRange(1, 32)
    r_range = ValueRange(0.0, 4.0)
    map_range = ValueRange(0.0, 1.0)

    valid_ret_types = ('alpha', 'decimal', 'ternary')

    def __init__(self,
                 x: np.float,
                 r: np.float,
                 alphabet: str,
                 depth: int,
                 ret_type: str,
                 ret_history: int = 2,
                 throwaway_itts: int = 10000
                 ):

        self.alphabet = alphabet
        self.depth = depth
        self.r = r

        self.ret_type = ret_type
        self.ret_history = ret_history

        self.brackets = len(self.alphabet) + 1

        self.x_vals = np.array([x], dtype=np.float64)
        if self.ret_type == 'alpha':
            self.labels = np.array([self.__get_label(x)], dtype=str)

        self.return_lookups = {'alpha': lambda: self.labels,
                               'decimal': lambda: np.array(self.x_vals),
                               'ternary': lambda: self.__evaluate_ternary()
                               }

        for _ in range(throwaway_itts):
            _ = next(self)

    @property
    def ret_type(self):
        return self.__ret_type

    @ret_type.setter
    def ret_type(self, ret_type):
        if ret_type not in self.valid_ret_types:
            warn = f'Valid Return Types are: {self.valid_ret_types}.\
            Default return type used. ret_type set to "alpha".'
            warnings.warn(warn, UserWarning)
            self.__ret_type = 'alpha'
        else:
            self.__ret_type = ret_type

    @property
    def ret_history(self):
        return self.__ret_history

    @ret_history.setter
    def ret_history(self, ret_history):
        if ret_history <= 0:
            warn = f'ret_history must be > 0.\
            ret_hist set to 2.'
            warnings.warn(warn, UserWarning)
            self.__ret_history = 2

        elif (self.ret_type == 'ternary') and (ret_history != 3):
            warn = f'ret_history must be = 3 for ret_type = "ternary".\
            ret_hist set to 3.'
            warnings.warn(warn, UserWarning)
            self.__ret_history = 3

        else:
            self.__ret_history = ret_history

    @property
    def r(self):
        return self.__r

    @r.setter
    def r(self, r):
        if self.r_range.min < r < self.r_range.max:
            self.__r = r
        else:
            error = f'r-value must be in the range \
            ({self.r_range.min} - f{self.r_range.max}).'
            raise ValueError(error)

    @property
    def depth(self):
        return self.__depth

    @depth.setter
    def depth(self, depth):
        if self.depth_range.min <= depth <= self.depth_range.max:
            self.__depth = int(depth)
        else:
            error = f'depth must be in the range \
            [{self.depth_range.min} - {self.depth_range.max}].'
            raise ValueError(error)

    def __get_label(self, x):

        # Helper function -> get brackets w/ endpoints
        # & appropriate brackets count
        def get_brackets(start, stop):
            return np.linspace(start=start,
                               stop=stop,
                               num=self.brackets,
                               endpoint=True)

        # set initial search brackets
        search_brackets = get_brackets(start=self.map_range.min,
                                       stop=self.map_range.max)

        # squence representation of decimal value
        sequence = ''
        for _ in range(self.depth):
            # find first index larger than input value
            # -> new search brackets = [value_index: value_index+1]
            value_index = np.argmax(search_brackets > x) - 1

            # Update sequence w/ new state
            sequence += self.alphabet[value_index]

            min_lim = search_brackets[value_index]
            max_lim = search_brackets[value_index + 1]
            search_brackets = get_brackets(start=min_lim,
                                           stop=max_lim)

        return sequence

    def __evaluate_ternary(self):
        return np.array(self.x_vals) / np.sum(self.x_vals)

    def __evaluate_map(self):
        last_x = self.x_vals[-1]
        return last_x * (1 - last_x) * self.r

    def __next__(self):

        while len(self.x_vals) <= self.ret_history:
            next_x = self.__evaluate_map()
            self.x_vals = np.append(self.x_vals, next_x)

            if self.ret_type == 'alpha':
                next_label = self.__get_label(next_x)
                self.labels = np.append(self.labels, next_label)

        if len(self.x_vals) >= self.ret_history:
            self.x_vals = self.x_vals[1:]
            if self.ret_type == 'alpha':
                self.labels = self.labels[1:]

        return self.return_lookups[self.ret_type]()


if __name__ == '__main__':
    # Init Test Class
    decimal_test_gen = LogisticMapGenerator(x=np.random.rand(),
                                            r=3.2,
                                            alphabet='ABCD',
                                            depth=6,
                                            ret_type='decimal'
                                            )

    for _ in range(10):
        print(next(decimal_test_gen))
    del decimal_test_gen

    alpha_test_gen = LogisticMapGenerator(x=np.random.rand(),
                                          r=3.2,
                                          alphabet='ABCD',
                                          depth=6,
                                          ret_type='alpha'
                                          )
    for _ in range(10):
        print(next(alpha_test_gen))
    del alpha_test_gen

    alpha_test_gen_2 = LogisticMapGenerator(x=np.random.rand(),
                                            r=3.2,
                                            alphabet='ABCD',
                                            depth=6,
                                            ret_type='alpha',
                                            ret_history=4
                                            )
    for _ in range(10):
        print(next(alpha_test_gen_2))
    del alpha_test_gen_2
