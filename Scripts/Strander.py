#! python
#This Script takes mate pair FASTQ files as input
#It scans MPRA Sequencing data and translates reads so that:
#Read one is always five Prime 
#Read two is always 3 prime
#All reads are from the same strand
from itertools import izip, izip_longest
import re
import sys
import os

Read1 = sys.argv[1]
Read2 = sys.argv[2]

##Counter variable to track conversation stats:
AsIs = 0
Reverse = 0
Complement = 0
RevComp = 0

##Temp Line variables
R1_Name = ""
R1_Seq = ""
R1_Strand = ""
R1_Qual = ""

R2_Name = ""
R2_Seq = ""
R2_Strand = ""
R2_Qual = ""

#Open Output Files
FivePrime = open("ReadOne.fastq", "w")
ThreePrime = open("ReadTwo.fastq", "w")
Garbage = open("Garbage_IDs.txt", "w")

#Complement Dict
Trans = {'A': 'T', 'T': 'A', 'C': 'G', 'G' : 'C', 'N' : 'N'}

Assign = {1: "R1_Name = LINE1; R2_Name = LINE2", 2: "R1_Seq = LINE1; R2_Seq = LINE2", 3: "R1_Strand = LINE1; R2_Strand = LINE2", 4: "R1_Qual = LINE1; R2_Qual = LINE2"}

FivePrimeMatch = 0
ThreePrimeMatchR2 = 0
ThreePrimeMatchR1 = 0
FivePrimeMatchR2 = 0
DoubleSeedMuts = 0
LotsMuts = 0
LotsMutsInverted = 0 
ShortSeed = 0
ShortSeedInv = 0

TotCount = 0
LineCounter=1
#Loop through files simultaneously here 
#don't need izip longest bc mate pair files are same length
with open(Read1) as file1, open(Read2) as file2:
    for line1, line2 in izip(file1, file2):  
        line1 = line1.rstrip('\r\n')
        line2 = line2.rstrip('\r\n')
        
        Line1 = line1.rstrip()
        Line2 = line2.rstrip()
        
        #Split each line to determine value
        LINE1 = list(Line1)
        LINE2 = list(Line2)
        
        #Assign the temp fastq values based on the commands stored in the array
        #This allows you to skip using
        
        exec(Assign[LineCounter])
        
        
    	if(LineCounter < 4): #Name @
        	
        	LineCounter += 1
        	
        else:
        	#print ''.join(R1_Seq[0:35])
        	LineCounter = 1
        	TotCount += 1
        	
        	#Match 5' seed to Read one: confirms correctly oriented fragments
        	if (bool(re.search( 'CAGGTGCCAGAACATTTCTCT', ''.join(R1_Seq[0:35]))) is True):
        		AsIs += 1
        		FivePrimeMatch += 1     		
        		print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
        		print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
        	
        	##Match 3' seed to Read one: inverted oriented fragments
        	elif (bool(re.search( 'CTGCTCGAAGCGGCCGGCC', ''.join(R1_Seq[0:35]))) is True):
        		Reverse += 1
        		ThreePrimeMatchR1 += 1
        		print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
        		print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
        	
        	#Match 3' seed to Read two: confirms correctly oriented fragments with mutation in 5' seed	
        	elif (bool(re.search( 'CTGCTCGAAGCGGCCGGCC', ''.join(R2_Seq[0:35]))) is True):
        		AsIs += 1
        		ThreePrimeMatchR2 += 1
        		print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
        		print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
        	
        	##Match 5' seed to Read two: inverted oriented fragments with mutation in 3' seed	
        	elif (bool(re.search( 'CAGGTGCCAGAACATTTCTCT', ''.join(R2_Seq[0:35]))) is True):
        		Reverse += 1
        		FivePrimeMatchR2 += 1
        		print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
        		print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
        	
        	##Match 5' Sfi site: Inverted fragments w/ lots of mutants 
        	elif (bool(re.search( 'GGCCTAACTGGCC', ''.join(R2_Seq[20:45]))) is True):
        		Reverse += 1
        		LotsMutsInverted += 1
        		print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
        		print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
        		
        	#Match Backbone plus KpnI and XbaI seed to Read one: confirms correctly oriented fragments w/ mutants in 5' AND 3' seeds
        	elif (bool(re.search( 'CACTGCGGCTCCTGCGGTACCTCT', ''.join(R1_Seq[120:220]))) is True):
        		AsIs += 1
        		DoubleSeedMuts += 1
        		print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
        		print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
        	      	
        	#Match 5' Sfi site: confirms correctly oriented fragments w/ lots of mutants 
        	elif (bool(re.search( 'GGCCTAACTGGCC', ''.join(R1_Seq[20:45]))) is True):
        		AsIs += 1
        		LotsMuts += 1
        		print >>FivePrime,''.join(R1_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n" ,''.join(R1_Qual)
        		print >>ThreePrime,''.join(R2_Name)+"\n",''.join(R2_Seq)+"\n" ,''.join(R2_Strand)+"\n" ,''.join(R2_Qual)

			#Match Shorter 5'seed: confirms correctly oriented fragments w/ lots of mutants 
        	elif (bool(re.search( 'CAGGTGCCAGAACA', ''.join(R1_Seq[3:23]))) is True):
        		AsIs += 1
        		ShortSeed += 1
        		print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
        		print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
        		
        	##Match Shorter 5'seed: confirms inverted fragments w/ lots of mutants 
        	elif (bool(re.search( 'CAGGTGCCAGAACA', ''.join(R2_Seq[3:23]))) is True):
        		Reverse += 1
        		ShortSeedInv += 1
        		
        		print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
        		print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
        				
        	else:
        		print >>Garbage, ''.join(R1_Name)+"\t"+''.join(R1_Qual)+"\t"+''.join(R2_Qual)
					
print "Total Correct (5' ends Read 1 and 3' ends Read2): ",AsIs
print "Total Swapped (5' ends Read 2 and 3' ends Read1): ",Reverse	
print "Percent Read: ",100*((AsIs+Reverse)/TotCount)	
print "Total Correct 5' Seed Matches to R1 (Correct): ", FivePrimeMatch
print "Total Correct 3' Seed Matches to R1 (Inverted): ", ThreePrimeMatchR1
print "Total Correct 3' Seed Matches to R2 (Correct): ", ThreePrimeMatchR2 
print "Total Correct 5' Seed Matches to R2 (Inverted): ", FivePrimeMatchR2
print "Total R2 Align Upstream SfiI (Inverted): ", LotsMutsInverted
print "Total Align KpnI, XbaI, and backbone (Correct): ", DoubleSeedMuts
print "Total R1 Align 5' SfiI (Correct): ", LotsMuts
print "Total Short Seed Correct Orientation: ", ShortSeed
print "Total Short Seed Inverted Orientation: ", ShortSeedInv

    
#os.system('sed "s/\s*$//" ReadOne.fastq > R_One.fastq')
#os.system('sed "s/\s*$//" ReadTwo.fastq > R_Two.fastq')

#os.system('rm ReadOne.fastq')
#os.system('rm ReadTwo.fastq')