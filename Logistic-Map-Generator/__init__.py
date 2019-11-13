
import string
import numpy as np


class LogisticMapGenerator:
    def __init__(self, x, r, alphabet, depth, ret_type='alpha'):
        self.alphabet = alphabet
        self.depth = depth
        self.r = r
        self.ret_type = ret_type if ret_type == 'alpha' else 'decimal'
        
        self.brackets = len(self.alphabet)+1

        self.last_x = None
        self.last_label = None
        
        self.current_x = x
        self.current_label = self.__get_label(self.current_x)



    def __get_label(self, x):
    	# set initial search brackets
        search_brackets = np.linspace(0.0,1.0, num=self.brackets, endpoint=True)

        # squence representation of decimal value
        sequence=''

        for _ in range(self.depth):
        	# find first index larger than input value -> new search brackets = [value_index-1: value_index]
            value_index = np.argmax(search_brackets > x)
            value_index -= 1

            # update sequence
            sequence += self.alphabet[value_index]

            # set new recursive search brackets
            min_lim, max_lim = search_brackets[value_index], search_brackets[value_index+1]
            search_brackets = np.linspace(min_lim, max_lim, num=self.brackets, endpoint=True)

        return sequence

    def __evaluate_map(self):
    	return self.last_x * (1 - self.last_x) * self.r
    
    def __next__(self):
        self.last_x = self.current_x
        self.last_label = self.current_label
        
        self.current_x = self.__evaluate_map()
        self.current_label = self.__get_label(self.current_x)
        
        return (self.last_label, self.current_label) if self.ret_type == 'alpha' else (self.last_x, self.current_x)
    
    def set_x(self, x):
        self.current_x = x
        self.current_label = self.__get_label(self.current_x)
        
    def set_r(self, r):
        self.r = r

if __name__ == '__main__':
    # Init Test Class
    decimal_test_gen = LogisticMapGenerator(x=np.random.rand(), r=3.2, alphabet='ABCD', depth=6, ret_type='decimal')

    for _ in range(10):
    	print(next(decimal_test_gen))
    del decimal_test_gen

    alpha_test_gen = LogisticMapGenerator(x=np.random.rand(), r=3.2, alphabet='ABCD', depth=6, ret_type='alpha')
    for _ in range(10):
    	print(next(alpha_test_gen))
    del alpha_test_gen