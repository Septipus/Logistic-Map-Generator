import numpy as np
from collections import namedtuple, deque


class LogisticMapGenerator:

    ValueRange = namedtuple('ValueRange', 'min max')

    # Global Params
    depth_range = ValueRange(1, 32)
    r_range = ValueRange(0.0, 4.0)
    map_range = ValueRange(0.0, 1.0)

    def __init__(self,
                 x: np.float,
                 r: np.float,
                 alphabet: str,
                 depth: int,
                 ret_type: str = 'alpha',
                 ret_history: int = 2
                 ):

        self.alphabet = alphabet
        self.depth = depth
        self.r = r
        self.ret_type = ret_type if ret_type == 'alpha' else 'decimal'
        self.ret_history = ret_history

        self.brackets = len(self.alphabet) + 1

        self.x_vals = deque([x])
        self.labels = deque([self.__get_label(x)])

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

    def __evaluate_map(self):
        last_x = self.x_vals[-1]
        return last_x * (1 - last_x) * self.r

    def __next__(self):
        if len(self.x_vals) == self.ret_history:
            _ = self.x_vals.popleft()
            _ = self.labels.popleft()

        while len(self.x_vals) < self.ret_history:
            next_x = self.__evaluate_map()
            next_label = self.__get_label(next_x)

            self.x_vals.append(next_x)
            self.labels.append(next_label)

        return self.labels \
            if self.ret_type == 'alpha' else self.x_vals

    @property
    def r(self):
        return self.__r

    @r.setter
    def r(self, r):
        if self.r_range.min < r < self.r_range.max:
            self.__r = r
        else:
            error = f'r-value must be in the range \
                    ({self.r_range.min} - f{self.r_range.min}).'
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
