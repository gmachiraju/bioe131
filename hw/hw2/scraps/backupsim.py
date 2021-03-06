#! /usr/bin/python
#-----------------------------------------------------------------------
# This Python script returns a uniformaly distributed, randomly generated DNA FASTA 
# sequence based on statistical input given or the defualt at 25% for each base.

# by Gautam Machiraju, BioE 131 Fall 2015 (independent work)
#-----------------------------------------------------------------------
#TO-DO:
#help message, generation length (985 vs 997)

from __future__ import division
import optparse
import sys
from random import choice
from itertools import groupby
import textwrap
import csv
import numpy

#---------------------------------------------
# Setting up Parser & Variable # of Arguments
#---------------------------------------------
myparser = optparse.OptionParser()
myparser.add_option("--calc", action="store")
myparser.add_option("--load", action="store")
myparser.add_option("--save", action="store", help="This Python script returns the a simulated DNA FASTA sequence based on statistical input")

options = myparser.parse_args()[0]
#print options 

#---------------------------
# Error Checking & Handling
#---------------------------

def errorCheckFasta(fileName):
	# Checking for a valid file input by trying to open it.
	try:	
		inFile = open(fileName)  
	except IOError:
		print "Error: file not found / no file input detected."
		sys.exit()

	# Checking if file input is of FASTA format (checking for popular extensions).
	if (fileName[-6:] != ".fasta") and (fileName[-3:] != ".fa") and (fileName[-4:] != ".fas") and (fileName[-4:] != ".fna") and (fileName[-4:] != ".ffn") and (fileName[-4:] != ".faa") and (fileName[-4:] != ".frn"):
		print "Error: cannot read file -- it is not of FASTA format."
		sys.exit()

def errorCheckParams(fileName):
	# Checking for a valid file input by trying to open it.
	try:	
		inFile = open(fileName)  
	except IOError:
		print "Error: file not found / no file input detected."
		sys.exit()


def foundStopCodon(orf):
    catch = numpy.arange(0, len(orf), 3)
    stopCodonPositions = []

    for i in catch:
        codon = orf[i:i + 3]
        if codon == 'TAA' or codon == 'TAG' or codon == 'TGA':
            stopCodonPositions.append(i + 1)

    if len(stopCodonPositions) > 0:
        return True
    else:
    	return False

#---------------
# Function Defs
#---------------
#~Referenced from StackOverlow~

def weightedChoice(items): # this doesn't require the numbers to add up to 100
	return choice("".join(x * y for x, y in items))


def createSeq(cComp, gComp, aComp, tComp, length): 
	dna = "ATG"
	for count in range(length):
		dna += weightedChoice([("C", cComp), ("G", gComp), ("A", aComp), ("T", tComp)])

	#Error checking for STOP codons
	if foundStopCodon(dna) == True:
		return createSeq(cComp, gComp, aComp, tComp, length)
	else:
		seq = "\n".join(textwrap.wrap(dna, 80))
		#print len(seq) #This doesn't seem to be adding length correctly...
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
	countC = totalSeq.count('C')
	countG = totalSeq.count('G')
	countA = totalSeq.count('A')
	countT = totalSeq.count('T')

	percentC = (totalSeq.count('C')/L)*100
	percentG = (totalSeq.count('G')/L)*100
	percentA = (totalSeq.count('A')/L)*100
	percentT = (totalSeq.count('T')/L)*100

	#Used for printing next sequence generation
	results = (countC, countG, countA, countT, L, seqNumber)
	#Used for printing statistics
	params = (percentC, percentG, percentA, percentT, L, seqNumber)
	return (results, params)


def seqSave(results, params, param_name):
	savedName = str(param_name) + ".csv"
	
	with open(savedName,'w') as out:
		csv_out = csv.writer(out)
		csv_out.writerow(["percent C", "percent G", "percent A", "percent T", "total seq length", "# of sequences"])
		csv_out.writerow(params)
		csv_out.writerow([" "])
		csv_out.writerow(["count C", "count G", "count A", "count T", "total seq length", "# of sequences"])
		csv_out.writerow(results)


def loadSeq(param_name):
	savedName = str(param_name) + ".csv"
	parseList = []
	
	with open(savedName, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			parseList.append(row)

	params = parseList[1]
	results = parseList[4]
	print params
	print results
	return (params, results)


#--------------
# Main Routine
#--------------
# Note: The "--save myparams" command stores the sequence statistics as a .csv file
# I.e. the values are comma-separated and are parsed through as a list when loading

#Inputs: simulator.py
if (options.calc == None) and (options.load == None) and (options.save == None):
	#We desire a kb output for option 1
	num = 997 # 997 
	print createSeq(25, 25, 25, 25, num)
	#print len(createSeq(25, 25, 25, 25, num))
	sys.exit()

#Inputs: simulator.py  --calc seqfile.fasta
if (options.calc != None) and (options.load == None) and (options.save == None):
	errorCheckFasta(options.calc)
	output = seqCalc(options.calc)
	results = output[0]
	#print results

	C = results[0]
	G = results[1]
	A = results[2]
	T = results[3]
	L = results[4]
	
	print createSeq(C, G, A, T, L)
	sys.exit()

#Inputs: simulator.py  --calc seqfile.fasta  --save myparams
if (options.calc != None) and (options.load == None) and (options.save != None):
	errorCheckFasta(options.calc)
	output = seqCalc(options.calc)
	params = output[1]
	results = output[0]
	seqSave(results, params, options.save)
	#print results

	C = results[0]
	G = results[1]
	A = results[2]
	T = results[3]
	L = results[4]

	#print results
	#print params
	
	print createSeq(C, G, A, T, L)
	sys.exit()

#Inputs: simulator.py  --load myparams
if (options.calc == None) and (options.load != None) and (options.save == None):
	errorCheckParams(options.load)
	output = loadSeq(options.load)
	results = output[1]

	C = int(results[0])
	G = int(results[1])
	A = int(results[2])
	T = int(results[3])
	L = int(results[4])

	print createSeq(C, G, A, T, L)

#Inputs: simulator.py  --load myparams  --save myparams2
if (options.calc == None) and (options.load != None) and (options.save != None):
	errorCheckParams(options.load)
	output = loadSeq(options.load)
	params = output[0]
	results = output[1]
	seqSave(results, params, options.save)

	C = int(results[0])
	G = int(results[1])
	A = int(results[2])
	T = int(results[3])
	L = int(results[4])

	print createSeq(C, G, A, T, L)






