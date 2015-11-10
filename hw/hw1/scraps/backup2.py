#! /usr/bin/python

#-------------------------------------------------------------------------------------
# This Python script returns the reverse complement of a sequence (either RNA or DNA) 
# by Gautam Machiraju, BioE 131 Fall 2015
#-------------------------------------------------------------------------------------
#things to do still: no "python" in command

import sys
from itertools import groupby
import textwrap

#---------------------------
# Error Checking & Handling
#---------------------------

# Checking for a file input.
try:	
	inFile = open(sys.argv[1])  
except IOError:
	print "Error: file not found / no file input detected."
	sys.exit()
	
#Checking if file input is of FASTA format.
filename = sys.argv[1]
if filename[-6:] != ".fasta":
	print "Error: cannot read file -- it is not of FASTA format."
	sys.exit()

# Reads in the 2nd input: the type of sequence (either RNA or DNA)
numVars = len(sys.argv)
if numVars == 2:
	print "Note: defaulting to DNA reverse complement."
elif (numVars == 3) and (sys.argv[2] != "rna"):
	print "Error: please enter a valid sequence type."
	sys.exit()

#--------------
# Main Routine
#--------------

# Defining a mapping library for the base complements and do the replacement
if (numVars == 3) and (sys.argv[2] == "rna"):
	complement = {'A':'U', 'U':'A', 'C':'G', 'G':'C'}
else: #default
	complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}

# Using lambda functions and grouping to parse fasta file with generator output
# ~Referenced from BioStars and StackOverflow~
def fasta_iter(fasta_name):
	fh = open(fasta_name)
	dataBlock = (x[1] for x in groupby(fh, lambda line: line[0] == ">"))
	for header in dataBlock:
	    header = header.next()[0:].strip()
	    # join all sequence lines to one
	    seq = "".join(s.strip() for s in dataBlock.next())
	    L = len(seq)
	    newHeader = header + ", " + str(L) + " bp"
	    # reversing and applying complement mapping
	    reverse = reversed(seq)
	    reverseComplement = "".join(complement.get(base, base) for base in reverse)
	    # restricting seq output to 80 characters/line
	    newSeq = "\n".join(textwrap.wrap(reverseComplement, 80))
	    yield newHeader, newSeq

# generator output for (sequence,header) tuple
seqGen = fasta_iter(filename)  
# convert generator of tuples to list of tuples
seqList = list(seqGen)

for tup in seqList:
	for item in tup:
		print item

inFile.close()

