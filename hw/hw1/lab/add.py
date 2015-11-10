#! /usr/bin/python
import sys

number = int(sys.argv[1])
sum = 0
for i in range(number):
	userNum = input("Please enter a number: ")
	sum += userNum     

print "The sum is", sum


#at a "slightly better calculator"