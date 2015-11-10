#! /usr/bin/python

#-------------------------------------------------------------------------------------
# This Python script returns probability analysis of Stockholm Data 
# by Gautam Machiraju, BioE 131 Fall 2015 (Worked with Taner D.)
#-------------------------------------------------------------------------------------

import sys
from itertools import groupby
import textwrap


def stockholm_reader(stockholmName):
	stockList = []
	with open(stockholmName) as f:
		for line in f:
			if (line[0] != '#') and (line[0] != '//'):
				stockList.append(line)
	#print stockList
	#print len(stockList)
	return stockList

def stockholm_tuples(stockholmName):
	stockTuples = []
	for i in range(0,len(stockholmName)-1,2):
		tup = (stockholmName[i], stockholmName[i+1])
		stockTuples.append(tup)
	print stockTuples


fileName = sys.argv[1]
stockList = stockholm_reader(fileName)
stockTuples = stockholm_tuples(stockList)







