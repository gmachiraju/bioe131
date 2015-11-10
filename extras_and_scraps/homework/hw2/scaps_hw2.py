#! /usr/bin/python

#-----------------------------------------------------------------------
# This Python script returns the a simulated DNA FASTA sequence based on 
# statistical input 
# by Gautam Machiraju, BioE 131 Fall 2015 (collaborated with Tanay N.)
#-----------------------------------------------------------------------
from __future__ import division
import optparse
import sys
from random import choice
from itertools import groupby
import textwrap


#---------------------------------------------
# Setting up Parser & Variable # of Arguments
#---------------------------------------------
myparser = optparse.OptionParser()
myparser.add_option("--calc", action="store")
myparser.add_option("--load", action="store")
myparser.add_option("--save", action="store", help="This Python script returns the a simulated DNA FASTA sequence based on statistical input")

options = myparser.parse_args()[0]
print options 

#---------------------------
# Error Checking & Handling
#---------------------------
def errorCheck(fileName):
	# Checking for a valid file input by trying to open it.
	try:	
		inFile = open(fileName)  
	except IOError:
		print "Error: file not found / no file input detected."
		sys.exit()

	# Checking if file input is of FASTA format (checking for popular extensions).
	fileName = options.calc
	if (fileName[-6:] != ".fasta") and (fileName[-3:] != ".fa") and (fileName[-4:] != ".fas") and (fileName[-4:] != ".fna") and (fileName[-4:] != ".ffn") and (fileName[-4:] != ".faa") and (fileName[-4:] != ".frn"):
		print "Error: cannot read file -- it is not of FASTA format."
		sys.exit()

#write more tests...

#---------------
# Function Defs
#---------------
#~Referenced from StackOverlow~

# def weightedChoice(items): # this doesn't require the numbers to add up to 100
#     return choice("".join(x * y for x, y in items))

def weightedChoice(items): # this doesn't require the numbers to add up to 100
    return choice("".join(x * y for x, y in items))


def createSeq(cComp, gComp, aComp, tComp, length): #need to make start codon at beginning and no premature terminations, with termination at end if want
	dna = "AUG"
	for count in range(length):
		dna += weightedChoice([("C", float(cComp)), ("G", gComp), ("A", aComp), ("T", tComp)])
    	seq = "\n".join(textwrap.wrap(dna, 80))
	return seq


def seqCalc(fasta_name):
	seqNumber = 0
	totalSeq = ""

	fh = open(fasta_name)
	dataBlock = (x[1] for x in groupby(fh, lambda line: line[0] == ">"))
	for header in dataBlock:
		header = header.next()[0:].strip()
		seq = "".join(s.strip() for s in dataBlock.next())
		totalSeq += seq
	    #Find the length of the current sequence block
		seqNumber += 1

	L = len(totalSeq)
	percentC = (totalSeq.count('C')/L)*100
	percentG = (totalSeq.count('G')/L)*100
	percentA = (totalSeq.count('A')/L)*100
	percentT = (totalSeq.count('T')/L)*100

	results = (percentC, percentG, percentA, percentT, L, seqNumber)
	return results


def seqSave(fasta_name, param_name):
	savedName = str(param_name)
	results = seqCalc(fasta_name)

	outfile = open(savedName, "w")
	outfile.write("percent C" + "percent G" + "percent A" + "percent T" + "total sequence length" + "# of sequences")
	outfile.write(str(results))
	outfile.close()

#--------------
# Main Routine
#--------------

#Inputs: simulator.py
if (options.calc == None) and (options.load == None) and (options.save == None):
	#We desire a kb output for option 1
	num = 985 # 997 
	print createSeq(25, 25, 25, 25, num)
	print len(createSeq(25, 25, 25, 25, num))
	sys.exit()

#Inputs: simulator.py  --calc seqfile.fasta
if (options.calc != None) and (options.load == None) and (options.save == None):
	errorCheck(options.calc)
	results = seqCalc(options.calc)
	print results

	C = results[0]
	G = results[1]
	A = results[2]
	T = results[3]
	L = results[4]
	
	#print createSeq(C, G, A, T, L)
	print createSeq(21, 20, 14, 75, L)
	sys.exit()

#Inputs: simulator.py  --calc seqfile.fasta  --save myparams
#if (options.calc != None) and (options.load == None) and (options.save != None):

#Inputs: simulator.py  --load myparams
#if (options.calc == None) and (options.load != None) and (options.save == None):

#Inputs: simulator.py  --load myparams  --save myparams2
#if (options.calc == None) and (options.load != None) and (options.save != None):




