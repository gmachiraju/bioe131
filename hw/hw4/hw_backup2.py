#! usr/bin/python

#-----------------------------------------------------------------------------------------
# This Python script returns probability analysis and Shannon Entropies of Stockholm Data.
# by Gautam Machiraju, BioE 131 Fall 2015 (Worked with Taner D.)
#-----------------------------------------------------------------------------------------
from __future__ import division
import sys
import math
import operator

#----------------
# Error Checking
#----------------

#Opening the input file, with exception handling.
try: 
	inFile = open(sys.argv[1])

#Exception: if user didn't enter a filename.
except IndexError: 
	print ("You must specify a stockholm filename to run. Command line should read: " 
 		   "'entropizer.py fileName.stock'")
	sys.exit()

#Exception: if filename is not openable.
except FileNotFoundError: 
	print("The file you entered could not be opened. Check to make sure it "
		  "is in the current directory and that you spelled it correctly in the "
		  "command line.")
	sys.exit()


#-----------------
# Data Structures
#-----------------

#Takes in opened file and puts relevant information in list format: [[name1, seq1], [name2, seq2] ...]
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
			line = line.replace("\n", "")
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


#Makes dictionary of (key = column index) and (value = entropy).
def makeEntropyDict(myList):
	myEntropyDict = {}
	numCols = len(myList[1][1])
	for i in range(numCols-1):
		prob = calcProb(myList, i)
		ent = calcEntropy(prob)
		myEntropyDict[i] = ent
	return myEntropyDict

#makes dictionary of (key = (char i, char j)) and (value = count).
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


#makes dictionary of (key = (column i, column j)) and (value = joint entropy).
def makeJEntropyDict(myList):
	myJEntropyDict = {}
	numCols = len(myList[1][1])
	numRows = len(myList)

	for i in range(0, numCols-1):
		for j in range(i+1, numCols-1):
			myCountDict = makeCountDict(myList, i, j)
			#print myCountDict

			myJProbDict = {}
			for key in myCountDict.keys():
				val = myCountDict[key]
				prob = val/numRows
				myJProbDict[key] = prob

			#print myJProbDict

			distribution = myJProbDict.values() 
			ent = calcEntropy(distribution)
			#print ent
			myJEntropyDict[i,j] = ent

	return myJEntropyDict


#makes dictionary of (key = (column i, column j)) and (value = mutual information).
def makeMIDict(myEntropyDict, myJEntropyDict):
	myMIDict = {}
	numCols = len(myList[1][1])
	for i in range(0, numCols-1):
		for j in range(i+1, numCols-1):
			myMIDict[i,j] = myEntropyDict[i] + myEntropyDict[j] - myJEntropyDict[i,j]
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
	sortedDict = sorted(myDict.items(), key = operator.itemgetter(1), reverse = True)
	#print sortedDict
	for i in range(50):
		print sortedDict[i][0]


#--------------
# Main Routine
#--------------

myList = makeList(inFile)

myEntropyDict = makeEntropyDict(myList)
bottomTen(myEntropyDict)

myJEntropyDict = makeJEntropyDict(myList)
myMIDict = makeMIDict(myEntropyDict, myJEntropyDict)
topFifty(myMIDict)

