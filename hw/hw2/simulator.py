#! /usr/bin/python
#-----------------------------------------------------------------------
# This Python script returns a uniformaly distributed, randomly generated DNA FASTA 
# sequence based on statistical input given or the defualt at 25% for each base.

# by Gautam Machiraju, BioE 131 Fall 2015 (independent work)
#-----------------------------------------------------------------------

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
myParser = optparse.OptionParser()
myParser.add_option("--calc", action = "store", help = "first calculate nucleotide composition, number of sequences, and length statistics (e.g. average sequence length).")
myParser.add_option("--load", action = "store", help = "loads the parameters from the named parameter file. Note: leave off .csv extension in input." )
myParser.add_option("--save", action = "store", help = "Saves calculated composition and length statistics to a file in the csv format. Note: leave off .csv extension in input.")

#Extra credit:
myParser.add_option("--gd", action = "store", help = "Statistics are computed on a geometric distribution.")

options = myParser.parse_args()[0]

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
		paramsName = str(fileName) + ".csv"
		inFile = open(paramsName)  
	except IOError:
		print "Error: file not found / no file input detected."
		sys.exit()


def findStopCodon(orf):
    catch = numpy.arange(0, len(orf), 3)
    stopCodonPositions = []

    for i in catch:
        codon = orf[i:i + 3]
        if codon == 'TAA' or codon == 'TAG' or codon == 'TGA':
            stopCodonPositions.append(i)
    
    return stopCodonPositions


def foundStopCodon(orf):
    catch = numpy.arange(0, len(orf), 3)
    stopCodonPositions = []

    for i in catch:
        codon = orf[i:i + 3]
        if codon == 'TAA' or codon == 'TAG' or codon == 'TGA':
            stopCodonPositions.append(i)

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
	#Generate uniformly distributed sequence first
	dna = "ATG"
	for count in range(length-3):
		dna += weightedChoice([("C", cComp), ("G", gComp), ("A", aComp), ("T", tComp)])

	#Convert dna to list since Python lists are immutable
	dnaL = list(dna)

	#Error checking: finding STOP codon positions
	stops = findStopCodon(dna)

	if len(stops) > 0:
		for stop in stops:

			#Generating replacement codon, and then checking those
			stopFlag = True
			while stopFlag == True:
				codon = ""

				for i in range(0, 3):
					codon += weightedChoice([("C", cComp), ("G", gComp), ("A", aComp), ("T", tComp)])
				
				if codon != 'TAA' and codon != 'TAG' and codon != 'TGA':
					stopFlag = False
					#replacing STOP with newly generated codon
		        	dnaL[stop] = codon[0]
		        	dnaL[stop+1] = codon[1]
		        	dnaL[stop+2] = codon[2]
		        	dna = "".join(dnaL)

	#final check: (uncomment to test for stops)
	#-------------------------------------------
	# print stops
	# print findStopCodon(dna)
	# print foundStopCodon(dna)

	seq = "\n".join(textwrap.wrap(dna, 80))
	return seq


def seqCalc(fasta_name):
	# number of sequence inputs
	SEQ_NUMBER = 0 
	totalSeq = ""
	fh = open(fasta_name)
	dataBlock = (x[1] for x in groupby(fh, lambda line: line[0] == ">"))
	
	for header in dataBlock:
		header = header.next()[0:].strip()
		seq = "".join(s.strip() for s in dataBlock.next())
		totalSeq += seq
		SEQ_NUMBER += 1

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
	results = (countC, countG, countA, countT, L, SEQ_NUMBER)
	#Used for printing statistics
	params = (percentC, percentG, percentA, percentT, L, SEQ_NUMBER)
	return (results, params)


def seqSave(results, params, param_name):
	savedName = str(param_name) + ".csv"
	
	with open(savedName,'w') as out:
		csvOut = csv.writer(out)
		csvOut.writerow(["percent C", "percent G", "percent A", "percent T", "total seq length", "# of sequences"])
		csvOut.writerow(params)
		csvOut.writerow([" "])
		csvOut.writerow(["count C", "count G", "count A", "count T", "total seq length", "# of sequences"])
		csvOut.writerow(results)


def seqLoad(param_name):
	loadName = str(param_name) + ".csv"
	parseList = []
	
	with open(loadName, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			parseList.append(row)

	params = parseList[1]
	results = parseList[4]
	return (params, results)


#--------------
# Main Routine
#--------------
# Note: The "--save myparams" command stores the sequence statistics as a .csv file
# I.e. the values are comma-separated and are parsed through as a list when loading

#Inputs: simulator.py
if (options.calc == None) and (options.load == None) and (options.save == None) and (options.gd == None):
	#We desire a 1 kb output for option 1
	NUM = 1000 
	print createSeq(25, 25, 25, 25, NUM)
	sys.exit()

#Inputs: simulator.py  --calc seqfile.fasta
if (options.calc != None) and (options.load == None) and (options.save == None) and (options.gd == None):
	errorCheckFasta(options.calc)
	output = seqCalc(options.calc)
	results = output[0]

	C = results[0]
	G = results[1]
	A = results[2]
	T = results[3]
	L = results[4]
	
	print createSeq(C, G, A, T, L)
	sys.exit()

#Inputs: simulator.py  --calc seqfile.fasta  --save myparams
if (options.calc != None) and (options.load == None) and (options.save != None) and (options.gd == None):
	errorCheckFasta(options.calc)
	output = seqCalc(options.calc)
	params = output[1]
	results = output[0]
	seqSave(results, params, options.save)

	C = results[0]
	G = results[1]
	A = results[2]
	T = results[3]
	L = results[4]

	print createSeq(C, G, A, T, L)
	sys.exit()

#Inputs: simulator.py  --load myparams
if (options.calc == None) and (options.load != None) and (options.save == None) and (options.gd == None):
	errorCheckParams(options.load)
	output = seqLoad(options.load)
	results = output[1]

	C = int(results[0])
	G = int(results[1])
	A = int(results[2])
	T = int(results[3])
	L = int(results[4])

	print createSeq(C, G, A, T, L)

#Inputs: simulator.py  --load myparams  --save myparams2
if (options.calc == None) and (options.load != None) and (options.save != None) and (options.gd == None):
	errorCheckParams(options.load)
	output = seqLoad(options.load)
	params = output[0]
	results = output[1]
	seqSave(results, params, options.save)

	C = int(results[0])
	G = int(results[1])
	A = int(results[2])
	T = int(results[3])
	L = int(results[4])

	print createSeq(C, G, A, T, L)


#Extra credit: very similar to 2nd if statement, "simulator.py  --calc seqfile.fasta"
# Pr(Y=k) = (1 - p)^k * p <-- probability that the kth trial (out of k trials) is the first success

#Inputs: simulator.py  --gd seqfile.fasta
#Outputs: Saves in file called geo.csv
if (options.calc == None) and (options.load == None) and (options.save == None) and (options.gd != None):
	errorCheckFasta(options.gd)
	output = seqCalc(options.gd)
	params = output[1]
	
	pC = params[0]
	pG = params[1]
	pA = params[2]
	pT = params[3]

	distC = []
	p = pC
	for k in range(1, 11):
		distC.append(p*(1-p)**k-1)
	
	distG = []
	p = pG
	for k in range(1, 11):
		distG.append(p*(1-p)**k-1)

	distA = []
	p = pA
	for k in range(1, 11):
		distA.append(p*(1-p)**k-1)

	distT = []
	p = pT
	for k in range(1, 11):
		distT.append(p*(1-p)**k-1)
	
	with open("geo.csv",'w') as out:
		csvOut = csv.writer(out)

		csvOut.writerow(["Discrete C distribution:"])
		csvOut.writerow(range(1,11))
		csvOut.writerow(distC)
		csvOut.writerow(["mean:"])
		csvOut.writerow([1/pC])
		csvOut.writerow(["variance:"])
		csvOut.writerow([(1-pC)/pC**2])
		csvOut.writerow([" "])

		csvOut.writerow(["Discrete G distribution:"])
		csvOut.writerow(range(1,11))
		csvOut.writerow(distG)
		csvOut.writerow(["mean:"])
		csvOut.writerow([1/pG])
		csvOut.writerow(["variance:"])
		csvOut.writerow([(1-pG)/pG**2])
		csvOut.writerow([" "])

		csvOut.writerow(["Discrete A distribution:"])
		csvOut.writerow(range(1,11))
		csvOut.writerow(distA)
		csvOut.writerow(["mean:"])
		csvOut.writerow([1/pA])
		csvOut.writerow(["variance:"])
		csvOut.writerow([(1-pA)/pA**2])
		csvOut.writerow([" "])

		csvOut.writerow(["Discrete T distribution:"])
		csvOut.writerow(range(1,11))
		csvOut.writerow(distT)
		csvOut.writerow(["mean:"])
		csvOut.writerow([1/pT])
		csvOut.writerow(["variance:"])
		csvOut.writerow([(1-pT)/pT**2])
		csvOut.writerow([" "])

	sys.exit()

