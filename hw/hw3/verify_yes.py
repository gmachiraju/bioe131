#Code by Gautam Machiraju for BioE 131 - HW3; discussed with Kadhir Manickam.
#This is a pseudocode of the functions that would validate a YES gate.
#Note: only pass OFF sequences in as input.

def verifyYesCorrectness(RNAsequence, coordinates):
    #go to dataParsing(RNAsequence)
    #parse the subsequent PDF for presence of stem I, III, and IV
    #boolean for OFF sequence = offSequence
    #if everything looks good -> offSequence = 1, else offSequence = 0
    
    #then remove the OBS sequence from RNAsequence using coordinates
    #send the subsequent sequence into dataParsing(RNAsequence)
    #parse the subsequent PDF for presence of stem I, II, and III
    #boolean for ON sequence = onSequence
    #if everything looks good -> onSequence = 1, else onSequence = 0
    
    #return [offSequence, onSequence] (1 = good, 0 = bad)
    
def dataParsing(RNAsequence):
    #put the sequence through RNAfold
    #extract the output
    #put the sequence through RNAplot
    #convert the dot.ps output to pdf
