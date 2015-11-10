
def seqSave(fasta_name, param_name):
	savedName = str(param_name)
	output = seqCalc(fasta_name)
	params = output[1]

	outfile = open(savedName, "w")
	outfile.write("percent C   percent G   percent A   percent T   total seq length   # of sequences\n")
	outfile.write(str(params))
	outfile.close()


#Inputs: simulator.py  --calc seqfile.fasta  --save myparams
if (options.calc != None) and (options.load == None) and (options.save != None):
	errorCheck(options.calc)
	output = seqCalc(options.calc)
	seqSave(options.calc, options.save)
	results = output[0]
	#print results

	C = results[0]
	G = results[1]
	A = results[2]
	T = results[3]
	L = results[4]

	print results
	print output[1]
	
	print createSeq(C, G, A, T, L)
	sys.exit()



def createSeq(cComp, gComp, aComp, tComp, length): 
	dna = "ATG"
	for count in range(length):
		dna += weightedChoice([("C", cComp), ("G", gComp), ("A", aComp), ("T", tComp)])
    
	seq = "\n".join(textwrap.wrap(dna, 80))

	#Error checking for STOP codons
	if foundStopCodon(seq) == True:
		createSeq(cComp, gComp, aComp, tComp, length)

	#print len(seq) #This doesn't seem to be adding length correctly...
	return seq




	dna = "ATGCCCTAACCC"
	#Error checking for STOP codons
	dna = removeStopCodons(dna)
	print dna
	print foundStopCodon(dna)
	print weightedChoice([("C", cComp), ("G", gComp), ("A", aComp), ("T", tComp)])




	# while len(dna) <= 12 #length
	# 	dna += weightedChoice([("C", cComp), ("G", gComp), ("A", aComp), ("T", tComp)])





# def findStopCodons(orf):
#     catch = numpy.arange(0, len(orf), 3)
#     startCodonPositions = []
#     stopCodonPositions = []
#     for i in catch:
#         codon = orf[i:i + 3]
#         if codon == 'ATG':
#             startCodonPositions.append(i + 1)
#         if codon == 'TAA' or codon == 'TAG' or codon == 'TGA':
#             stopCodonPositions.append(i + 1)
#     return startCodonPositions, stopCodonPositions


# def weightedChoice(items): # this doesn't require the numbers to add up to 100
#     return choice("".join(x * y for x, y in items))


	#print len(seq) #This doesn't seem to be adding length correctly...


def removeStopCodons(orf):
    catch = numpy.arange(0, len(orf), 3)

    for i in catch:
        codon = orf[i:i + 3]
        if codon == 'TAA' or codon == 'TAG' or codon == 'TGA':
            orf = orf[:i]
    return orf




	count = 3 # to account for START codon

	while count < length:
		# codon generation using uniform distribution
		codon = ""
		for i in range(0, 3):
			codon += weightedChoice([("C", cComp), ("G", gComp), ("A", aComp), ("T", tComp)])
		print codon

		# error checking for stop codons
		if codon == 'TAA' or codon == 'TAG' or codon == 'TGA':
			codon = ""

        dna += codon




    


dna = "ATG"
	triplet = ""
	count = 0


	for count in range(length):
		dna += weightedChoice([("C", cComp), ("G", gComp), ("A", aComp), ("T", tComp)])
    


	while count <= length:

		for i in range(1, 4):
			triplet += weightedChoice([("C", cComp), ("G", gComp), ("A", aComp), ("T", tComp)])
			print triplet


		#Error checking for STOP codons
    	if triplet == 'TAA' or triplet == 'TAG' or triplet == 'TGA':
    		triplet = ""
    	else:
    		count += 3
    	
    	dna += triplet

	seq = "\n".join(textwrap.wrap(dna, 80))
	#print len(seq)
	return seq













def createSeq(cComp, gComp, aComp, tComp, length): #need to make start codon at beginning and no premature terminations, with termination at end if want
	dna = "ATG"
	for count in range(length):
		dna += weightedChoice([("C", cComp), ("G", gComp), ("A", aComp), ("T", tComp)])
    
	seq = "\n".join(textwrap.wrap(dna, 80))
	#print len(seq)
	return seq