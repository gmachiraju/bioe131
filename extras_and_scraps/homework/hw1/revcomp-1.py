#! /usr/bin/python

#-------------------------------------------------------------------------------------
# This Python script returns the reverse complement of a sequence (either RNA or DNA) 
# by Gautam Machiraju, BioE 131 Fall 2015 (independent work)
#-------------------------------------------------------------------------------------

import sys
from itertools import groupby
import textwrap

#---------------------------
# Error Checking & Handling
#---------------------------

# Checking if file input is of FASTA format (checking for popular extensions).
fileName = sys.argv[1]
if (fileName[-6:] != ".fasta") and (fileName[-3:] != ".fa") and (fileName[-4:] != ".fas") and (fileName[-4:] != ".fna") and (fileName[-4:] != ".ffn") and (fileName[-4:] != ".faa") and (fileName[-4:] != ".frn"):
	print "Error: cannot read file -- it is not of FASTA format."
	sys.exit()

# Checking for a valid file input by trying to open it.
try:	
	inFile = open(sys.argv[1])  
except IOError:
	print "Error: file not found / no file input detected."
	sys.exit()
	
# Reads in the 2nd input: the type of sequence (either RNA or DNA).
NUM_VARS = len(sys.argv)
if NUM_VARS == 2:
	print "Note: defaulting to DNA reverse complement."
elif (NUM_VARS == 3) and (sys.argv[2] != "rna"):
	print "Error: please enter a valid sequence type."
	sys.exit()

#--------------
# Main Routine
#--------------

# Defining a mapping library for the base complements and do the replacement.
if (NUM_VARS == 3) and (sys.argv[2] == "rna"):
	complement = {'A':'U', 'T':'A', 'C':'G', 'G':'C'}
else: #default
	complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}

# Using lambda functions and grouping to parse fasta file with generator output.
# ~Referenced from BioStars and StackOverflow~
def fasta_iter(fasta_name):
	fh = open(fasta_name)
	dataBlock = (x[1] for x in groupby(fh, lambda line: line[0] == ">"))
	for header in dataBlock:
	    header = header.next()[0:].strip()
	    # join all sequence lines to one.
	    seq = "".join(s.strip() for s in dataBlock.next())
	    L = len(seq)
	    newHeader = header + ", " + str(L) + " bp"
	    # reversing and applying complement mapping.
	    reverse = reversed(seq)
	    reverseComplement = "".join(complement.get(base, base) for base in reverse)
	    # restricting seq output to 80 characters/line.
	    newSeq = "\n".join(textwrap.wrap(reverseComplement, 80))
	    yield newHeader, newSeq

# generator output for (sequence,header) tuple.
seqGen = fasta_iter(fileName)  
# convert generator of tuples to list of tuples.
seqList = list(seqGen)

for tup in seqList:
	for item in tup:
		print item

inFile.close()

