
import argparse
import sys
from random import choice



myparser = argparse.OptionParser()
myparser.add_option("-r", "--runtot", action="store_true")

options = myparser.parse_args()[0]
args = myparser.parse_args()[1]


number = int(sys.argv[1])       # read in from the command line how many numbers to ask for input to add up
sum = 0  
for i in range(number):
    userNum = input("Please enter a number: ")
    sum += userNum      # keep a running sum
    if options.runtot == True:        # Note here we check to see whether the option has been invoked or not!
    	print "Current total:",sum
print "The sum is",sum