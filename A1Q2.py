#################################################
#@title:     Pairwise Calculator                #
#            COMPSCI 320                        #
#            A1Q2                               #
#@author     Samuel Powell                      #
#            mgu011                             #
#            4364426                            #
#################################################
import math
import copy
import random

input_string = "10 20 50 51 52 53 54 12 15 16 "
data_set = input_string.split()
data_set = [random.randint(0,20000) for i in range(20000)]

for i in range(len(data_set)):
	data_set[i] = int(data_set[i])

def add_to_dict(a_dict, value):
	try:
		a_dict[value] += 1
	except:
		a_dict[value] = 1

def pairwise_min(data_set):
	data_length = len(data_set)
	current_min = {}
	row_min = []
	pair_data = []
	
	for i in range(data_length):
		for j in range(data_length - (i)):
			j = j + i
			if (i != j):
				#print("{0}: {2}\n{1}: {3}\n".format(i, j, data_set[i], data_set[j]))
				temp_min = data_set[i] + data_set[j]
				row_min += [temp_min]
				
	for value in row_min:
		add_to_dict(current_min, value)
		
	for key, value in current_min.items():
		if (value > 1):
			# print("{0}: {1}".format(key, value))
			pair_data += [key]
	try:
		return min(pair_data)
	except:
		return None
		
def sample_min(in_data):
	data_copy = copy.deepcopy(in_data)
	data_size = len(in_data)
	
	while (data_size > 10000):
		data_size = int(data_size / 5)
	data_copy = data_copy[:data_size]
	local_min = pairwise_min(data_copy)
	
	return local_min
		
def input(in_data):
	in_data = list(set(in_data))
	local_min = sample_min(in_data)
	
	filtered_list = [x for x in in_data if x <= local_min]
	pair_min = pairwise_min(filtered_list)
	
	if (not(pair_min)):
		print("None")
	else:
		print("Yes: {0}".format(pair_min))
		
def main(in_data):
	input(in_data)
	
main(data_set)