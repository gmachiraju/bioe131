#! /usr/bin/python

import sys 

fastafile = open(sys.argv[1])    # the user will enter the filename from the command line
names = []     # any variable we are going to *modify* must be created ahead of time.

for line in fastafile:
    names.append(line[1:].rstrip())  #  <--- Note the modification here - string slicing!

for name in names:
	print name # <-- printing one line at a time.

# print names <-- original print

#----------Checking for protease---------
# option 1:
found = False
for name in names:
    if name == "protease":
        found = True
if found == True:    # You can also just write "if found" - "if" statements check for truth/existence by default
    print "Found protease in file!"

# option 2:
found = False
if "protease" in names:
    found = True
    print "Found protease in file!"

fastafile.close()