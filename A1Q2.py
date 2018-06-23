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
		
def main(in_data):
	data_set = in_data
	data_length = len(data_set)
	
	if (length <= 20):
		for i in range(data_length):
			for j in range(data_length):
				if (j != i):
					gcd(data_set[i], data_set[j])
	
	