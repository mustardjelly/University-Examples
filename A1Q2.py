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

# Adds values to a counting dictionary
def add_to_dict(a_dict, value):
	try:
		a_dict[value] += 1
	except:
		a_dict[value] = 1

# When given a set calculates the minimum of that set
# Returns an Integer or None
def pairwise_min(data_set):
	data_length = len(data_set)
	current_min = {}
	mins = []
	pair_data = []
	
	# Calculate the pairings for for all unique combinations
	for i in range(data_length):
		for j in range(data_length - (i)):
			j = j + i
			if (i != j):
				#print("{0}: {2}\n{1}: {3}\n".format(i, j, data_set[i], data_set[j]))
				temp_min = data_set[i] + data_set[j]
				mins += [temp_min]
				
	# Counts of all pair values
	for value in mins:
		add_to_dict(current_min, value)
		
	# Create a list of values with a count > 1
	for key, value in current_min.items():
		if (value > 1):
			# print("{0}: {1}".format(key, value))
			pair_data += [key]
			
	try:
		return min(pair_data)
	except:
		return None
		
# Takes a data set and samples a minimum. Uses this sample 
# to create a filtering mean to reduce the size of our data
# set		
def sample_min(in_data):
	data_copy = copy.deepcopy(in_data)
	data_size = len(in_data)
	
	while (data_size > 10000):
		data_size = int(data_size / 5)
	data_copy = data_copy[:data_size]
	local_min = pairwise_min(data_copy)
	
	return local_min
		
# Takes a data set and attempts to find the smallest pair wise
# sum defined in A1Q2
def input(in_data):
	# Sanitize the data for processing
	in_data = list(set(in_data))
	local_min = sample_min(in_data)
	
	# Creates a smaller filtered list
	filtered_list = [x for x in in_data if x <= local_min]
	# Creates a pairwise min for all elements in the original
	# data set smaller than or equal to the smallest sum found 
	# in the sample
	pair_min = pairwise_min(filtered_list)
	
	if (not(pair_min)):
		print("None")
	else:
		print("Yes: {0}".format(pair_min))
		

def main(in_data):
	input(in_data)

# Inputs
# input_string = "10 20 50 51 52 53 54 12 15 16 "
# data_set = input_string.split()
# Big Random Set
data_set = [int(random.randint(0,20000)) for i in range(20000)]
	
main(data_set)