#! /usr/bin/python
import sys

infile = open(sys.argv[1])  # Creates a variable to store the opened file to reference later

#-------------
lines = infile.read().splitlines() # added to take away extra return
# or do: lines = f.readlines()
#-------------
val = 0

for line in lines:  # edited infile --> lines
	if line.startswith("+") and type(int(line[2])) == int:
		print "Do addition!"
		val = val + int(line[2])
		print val
	elif line.startswith("-") and type(int(line[2])) == int:
		print "Do subtraction!"
		val = val - int(line[2])
		print val
	elif line.startswith("*") and type(int(line[2])) == int:
		print "Do multiplication!"
		val = val * int(line[2])
		print val
	elif line.startswith("/") and type(int(line[2])) == int:
		print "Do division!"
		val = val / int(line[2])
		print val
	else:  # If it does not begin with a math symbol
		print "Ignored line:", line

infile.close()