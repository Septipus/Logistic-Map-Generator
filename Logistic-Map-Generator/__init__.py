import string
import numpy as np
from collections import namedtuple

class LogisticMapGenerator:

	ValueRange = namedtuple('ValueRange', 'min max')

	# Global Params
	depth_range = ValueRange(1, 32)
	r_range = ValueRange(0.0, 4.0)
	map_range = ValueRange(0.0, 1.0)
	
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

		# Helper function -> get brackets w/ endpoints & appropriate brackets count
		get_brackets = lambda start, stop: np.linspace(start=start, stop=stop, num=self.brackets, endpoint=True)
		
		# set initial search brackets
		search_brackets = get_brackets(start=self.map_range.min, stop=self.map_range.max)

		# squence representation of decimal value
		sequence=''
		for _ in range(self.depth):
			# find first index larger than input value -> new search brackets = [value_index: value_index+1]
			value_index = np.argmax(search_brackets > x) - 1

			# Update sequence w/ new state
			sequence += self.alphabet[value_index]

			min_lim, max_lim = search_brackets[value_index], search_brackets[value_index+1]
			search_brackets = get_brackets(start=min_lim, stop=max_lim)

		return sequence

	def __evaluate_map(self):
		return self.last_x * (1 - self.last_x) * self.r
	
	def __next__(self):
		self.last_x = self.current_x
		self.last_label = self.current_label
		
		self.current_x = self.__evaluate_map()
		self.current_label = self.__get_label(self.current_x)
		
		return (self.last_label, self.current_label) if self.ret_type == 'alpha' else (self.last_x, self.current_x)
	
	@property
	def r(self):
		return self.__r
	
	@r.setter  
	def r(self, r):
		if self.r_range.min <= r <=self.r_range.max:
			self.__r=r
		else:
			raise ValueError('Value of r must be in the range [0.0 - 4.0].')
		
	@property
	def depth(self):
		return self.__depth
	
	@depth.setter  
	def depth(self, depth):
		if self.depth_range.min <= depth <=self.depth_range.max:
			self.__depth=int(depth)
		else:
			raise ValueError(f'Value of r must be in the range [0.0 - {self.max_depth}].')
		

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