#################################################
#@title:     GCD Calculator                     #
#            COMPSCI 320                        #
#            A1Q1                               #
#@author     Samuel Powell                      #
#            mgu011                             #
#            4364426                            #
#################################################

# Calculates the greatest common denominator of two 
# or more numbers and outputs the value of their gcd
# 0 to terminate

# Global Variables
OUT_TEXT = 'The gcd of the integer(s) is'

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
                

def main():
    inputs = input()
    # Function terminate clause
    while inputs != '0':
        # Line variables
        current = 0
        useList = []
        inputs = inputs.split()
        
        # Convert array from string to integers
        for x in range(len(inputs)):
            if inputs[x] != '0' and inputs[x] != '-0':
                useList.append(int(inputs[x]))
                
        if len(useList) == 1:
            gcdVal = useList[0]
        elif len(useList) == 0:
            gcdVal = 0
        # Calls gcd on pairs on numbers until the highest gcd
        # is calculated
        else:
            gcdVal = gcd(useList[current], useList[current + 1])
            # Shifts the current index along
            current += 2
            while current != len(useList):
                gcdVal = gcd(int(gcdVal), useList[current])
                current += 1
                
        print(OUT_TEXT, str(gcdVal) + '.')
        
        # Next input
        inputs = input()
        
main()