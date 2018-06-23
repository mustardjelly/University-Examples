#################################################
#@title:     Pairwise Calculator                #
#            COMPSCI 320                        #
#            A1Q2                               #
#@author     Samuel Powell                      #
#            mgu011                             #
#            4364426                            #
#################################################
import math

# Calculates and returns the GCD of two numbers
def gcd(number1, number2):
    remainder = ''
    quotient = 0
    
    # Sets number1 to be the larger number
    if number2 > number1:
        tempNumber = number1
        number1 = number2
        number2 = tempNumber
        
    while (True):#remainder != 0):
        remainder = number1 % number2
        if remainder != 0:
            number1 = number2
            number2 = remainder
        else:
            if number2 > 0:
                return number2
            else:
                return -number2
				
data_set = [10, 16, 8, 3, 4, 2, 1, 60, 33, 12, 18, 13]

# Sets processing boundaries to speed up large calculations by setting a limit on
# the number of elements to look at.
# Input: a data set
# Output: (int) a number of elements to process
def process_data(aDataSet):
	length = len(aDataSet)
	if (length > 1000000):
		return 100000
	if length > 100000):
		return length / 2
		
