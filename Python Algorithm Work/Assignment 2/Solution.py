#############################################################
# Title:  COMPSCI 320 A3                                    #
# Date:   31 AUG 2017                                       #
# Author: Sam Powell                                        #
#         mgu011                                            #
# Desc:   Calculates the i<10**10                           #
#         number of the sequence                            #
#         1121231234.... to 10*10                           #
#############################################################

# Used for testing by brute forcing the string up to inputInt
# Test no more than 6000
def testFunc(inputInt):
    tempString = ""
    outString = ""
    for i in range(1,inputInt):
        tempString += str(i)
        outString += tempString
    return outString

# Creates a string equal to the longest max number in the 
# sequence required for a string of length 10**10.
# If you know how many digits are used on full strings to this
# point you can subtract that from the the search length and
# use the index of this string to find the number at a given
# index.
masterString = ""
for i in range(1,343463):
    masterString += str(i)

# This function calculates the length of the complete sequence
# up until the search length.
# e.g If we search for 6, the longest complete sequence before
# length 6 is "112" or length 3. Then the remainder (6 - 3) is 
# used on the masterString as an index to find the value at that 
# point.
# Returns the length of the complete sequence under our searchLength
def searchFunction(searchLength):
    length = 0; # Keeps track of how long the string is
    # adding ints of length one 9 times (1, 2, ..., 9)
    for i in range(1, 10):
        prev = length   # keeps track of the last length
        length += i # increases the length by 1, 2, ..., 9
        # if the new length is longer than the searchLength
        # then we have found the lower bound of our length
        if length >= searchLength:  
            return prev 
            # returns the complete sequence length 
            # under our searchLength
            
    # adding ints of length two 89 =((189 - 11) / 2) times
    for i in range(11, 189, 2):
        prev = length
        length += i
        if length >= searchLength:
            return prev
    
    # adding ints of length three 899 times
    for i in range(189, 2889, 3):
        prev = length
        length += i
        if length >= searchLength:
            return prev
            
    # adding ints of length 4 8,999 times
    for i in range(2889, 38889, 4):
        prev = length
        length += i
        if length >= searchLength:
            return prev
            
    # adding ints of length 5 89,999 times
    for i in range(38889, 488889, 5):
        prev = length
        length += i
        if length >= searchLength:
            return prev
            
    # adding ints of length 6 899,999 times
    for i in range(488889, 5888889, 6):
        prev = length
        length += i
        if length >= searchLength:
            return prev
            
# Testing Functions            
# testString = testFunc(6000)
# lengthOfTest = len(testString)

# Finds the shortest complete sequence below the index
# we are trying to find. Subtract the shortest complete 
# sequence from our initial value. Now we can use the 
# masterString[index - 1] to calculate the value from the
# index given.
howMany = int(input())
for questions in range(howMany):
    searchLength = int(input())
    output = searchFunction(searchLength)   
    print(masterString[searchLength - output - 1])

#print("real: " + testString[searchLength-1])