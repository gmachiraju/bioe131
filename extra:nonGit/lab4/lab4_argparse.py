#! /usr/bin/python
import optparse
import sys

myparser = optparse.OptionParser()
myparser.add_option("-r", "--runtot", action="store_true")
myparser.add_option("-m", "--myname", action="store", default="Bogworth", help="allows you to tell the adder your name")

options = myparser.parse_args()[0]
args = myparser.parse_args()[1]
print options
print args

number = int(sys.argv[1])       # read in from the command line how many numbers to ask for input to add up
sum = 0  
for i in range(number):
    userNum = input("Please enter a number: ")
    sum += userNum      # keep a running sum
    if options.runtot == True:        # Note here we check to see whether the option has been invoked or not!
    	print "Current total:",sum
if options.myname != None:            # Note the if loop here.
    print "Hello, "+options.myname+" - The sum is",sum
else:
	print "The sum is",sum
