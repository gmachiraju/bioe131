#! usr/bin/python

#-------------------------------------------------------------------------------------
# This Python script returns probability analysis of Stockholm Data 
# by Gautam Machiraju, BioE 131 Fall 2015 (Worked with Taner D.)
#-------------------------------------------------------------------------------------
from __future__ import division
import sys
import math
import operator

#----------------
# Error Checking
#----------------

## Opening the input file, with exception Handling ##
try: 
	inFile = open(sys.argv[1])

# Exception: if user didn't enter a filename
except IndexError: 
	print ("You must specify a stockholm filename to run. Command line should read: " 
 		   "'entropizer.py fileName.stock'")
	sys.exit()

# Exception: if filename is not openable
except FileNotFoundError: 
	print("The file you entered could not be opened. Check to make sure it "
		  "is in the current directory and that you spelled it correctly in the "
		  "command line.")
	sys.exit()


#-----------------
# Data Structures
#-----------------

# Takes in the opened file and puts the relevant information in list format: [[name1, seq1], [name2, seq2] ...]
def makeList(inFile):
	myList = []
	for line in inFile: 
		if "//" in line:
			break
		if line[0] != "#": 
			nameStarted = False
			nameEnded = False
			name = ""
			seq = ""
			for char in line: 
				if char != " " and nameStarted == False and nameEnded == False:
					nameStarted = True
					name += char
				elif char != " " and nameEnded == False:
					name += char
				elif char == " " and nameStarted:
					nameEnded = True
				elif char != " ":
					seq += char
			myList += [[name,seq]]
	return myList


#makes dictionary of (key = column index) and (value = entropy)
def makeEntropyDict(myList):
	myEntropyDict = {}
	numCols = len(myList[1][1])
	for i in range(numCols-1):
		prob = calcProb(myList, i)
		ent = calcEntropy(prob)
		myEntropyDict[i] = ent
	return myEntropyDict


def makeCountDict(myList, i, j):
	countDict = {}
	for line in myList:
		char1 = line[1][i]
		char2 = line[1][j]
		try:
			countDict[char1, char2] = countDict[char1, char2] + 1
		except KeyError:
			countDict[char1, char2] = 1
	return countDict


#makes dictionary of (key = column index) and (value = mutual information)
def makeJEntropyDict(myList):
	myJEntropyDict = {}
	numCols = len(myList[1][1])
	for i in range(0, numCols-1):
		for j in range(i+1, numCols-1):
			myJEntropyDict = makeCountDict(myList, i, j)

	# numRows = len(myList)
	# for key in myJEntropyDict.keys():
	# 	val = myJEntropyDict[key]
	# 	myJEntropyDict[key] = val/numRows

	# for key in myJEntropyDict.keys():
	# 	prob = myJEntropyDict[key]
	# 	ent = calcEntropy([prob])
	# 	myJEntropyDict[key] = ent

	return myJEntropyDict


def makeMIDict(myEntropyDict, myJEntropyDict):
	myMIDict = {}
	for i in range(len(myList[1][1])-1):
		for j in range(i+1,len(myList[1][1])-1):
			mutInfo[i,j] = myEntropyDict[i] + myEntropyDict[j] - myJEntropyDict[i,j]
	return myMIDict


#-----------------------
# Calculation Functions
#-----------------------

#Calculates the probability of finding an A, U, C, G or gap at positions in column i.  
def calcProb(myList, i): 
	Acount = 0 
	Ccount = 0
	Ucount = 0
	Gcount = 0
	gapCount = 0 
	for [key, value] in myList:
		if value[i] == "U": Ucount += 1
		if value[i] == "A": Acount += 1
		if value[i] == "G": Gcount += 1
		if value[i] == "C": Ccount += 1
		if value[i] == "." or value[i] == "-": 
			gapCount += 1
	toReturn = [Acount, Ccount, Ucount, Gcount, gapCount]
	#print toReturn
	numRows = len(myList)
	return [i/numRows for i in toReturn]


#Calculates the entropy of the given discrete probability distribution by summing over all of the 
#probabilities using the formula: - sum (P(x)*log(P(x))). We call this H_i.
def calcEntropy(distribution):
	ent = 0
	for val in distribution: 
		if val > 0:
			ent += val*math.log(val,2)
	return -ent


#---------------
# Graded Output
#---------------

#Output - Bottom 10 entropy data points.
def bottomTen(myDict):
	sortedDict = sorted(myDict.items(), key = operator.itemgetter(1))
	#print sortedDict
	for i in range(10):
		print sortedDict[i][0]


#Output - Top 50 mutual information data points.
def topFifty(myDict):
	sortedDict = sorted(myDict.items(), key = operator.itemgetter(1))
	print sortedDict
	for i in range(50):
		print sortedDict[-i][0]


#--------------
# Main Routine
#--------------

myList = makeList(inFile)

myEntropyDict = makeEntropyDict(myList)
bottomTen(myEntropyDict)

# cd = makeCountDict(myList,0,1)
# print cd

myJEntropyDict = makeJEntropyDict(myList)
print myJEntropyDict
#myMIDict = makeMIDict(myEntropyDict, myJEntropyDict)
#topFifty(myMIDict)

