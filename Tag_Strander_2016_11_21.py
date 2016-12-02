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
MidMatchCor = 0
MidMatchRev = 0
LastDitchRev = 0
LastDitchCor = 0
TopThirdMatchCor = 0
TopThirdMatchRev = 0
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
            if (bool(re.search( 'CAAGAAGGGCGGCAAGAT', ''.join(R1_Seq[0:30]))) is True):
            	AsIs += 1
            	FivePrimeMatch += 1
            	print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
            	print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
            	
            ##Match 3' seed to Read one: inverted oriented fragments
            elif (bool(re.search( 'ACGCTCTTCCGATCT', ''.join(R1_Seq[0:30]))) is True):
				Reverse += 1
				ThreePrimeMatchR1 += 1
				print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
				print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
                
            #Match 3' seed to Read two: confirms correctly oriented fragments with mutation in 5' seed      
            elif (bool(re.search( 'ACGCTCTTCCGATCT', ''.join(R2_Seq[0:30]))) is True):
            	AsIs += 1
            	ThreePrimeMatchR2 += 1
            	print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
            	print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
                
            #Match Backbone plus XbaI seed to Read two: confirms correctly oriented fragments w/ mutants in 5' AND 3' seeds 
            elif (bool(re.search( 'TCTAGAATTATTACA', ''.join(R2_Seq[25:65]))) is True):
            	Reverse += 1
            	FivePrimeMatchR2 += 1
            	print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
            	print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
            
            elif (bool(re.search( 'TGTAATAATTCTAGA', ''.join(R1_Seq[90:110]))) is True):
            	AsIs += 1
            	DoubleSeedMuts += 1
            	print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
            	print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
            
            
            #Match 5' Sfi site: confirms correctly oriented fragments w/ lots of mutants
            elif (bool(re.search( 'GATTCTCATTAAGGCCA', ''.join(R1_Seq[45:90]))) is True):
            	AsIs += 1
            	LotsMuts += 1
            	print >>FivePrime,''.join(R1_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n" ,''.join(R1_Qual)
            	print >>ThreePrime,''.join(R2_Name)+"\n",''.join(R2_Seq)+"\n" ,''.join(R2_Strand)+"\n" ,''.join(R2_Qual)
            
            #Match Middle  to Read one: confirms correctly oriented fragments
            elif (bool(re.search( 'CCAAGAAGGGCGGCAA', ''.join(R1_Seq[65:95]))) is True):
                AsIs += 1
                MidMatchCor += 1                     
                print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
                print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
                
            ##Match Middle seed to Read two: inverted oriented fragments
            elif (bool(re.search( 'CCAAGAAGGGCGGCAA', ''.join(R2_Seq[65:95]))) is True):
                Reverse += 1
                MidMatchRev += 1
                print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
                print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
            
            #Match Middle Inv to Read one: confirms correctly oriented fragments
            elif (bool(re.search( 'TTGCCGCCCTTCTTGG', ''.join(R2_Seq[50:80]))) is True):
                AsIs += 1
                MidMatchCor += 1                     
                print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
                print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
                
            ##Match 3' Inv seed to Read two: inverted oriented fragments
            elif (bool(re.search( 'TTGCCGCCCTTCTTGG', ''.join(R1_Seq[50:80]))) is True):
                Reverse += 1
                MidMatchRev += 1
                print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
                print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
            
            #Match TopThird  to Read one: confirms correctly oriented fragments
            elif (bool(re.search( 'ACTGACCGGCAAGTTG', ''.join(R1_Seq[15:45]))) is True):
                AsIs += 1
                MidMatchCor += 1                     
                print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
                print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
                
            ##Match TopThird seed to Read two: inverted oriented fragments
            elif (bool(re.search( 'ACTGACCGGCAAGTTG', ''.join(R2_Seq[15:45]))) is True):
                Reverse += 1
                MidMatchRev += 1
                print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
                print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
              
            ##MatchTopThird Inv seed to Read two: inverted oriented fragments
            elif (bool(re.search( 'CAACTTGCCGGTCAGT', ''.join(R1_Seq[80:110]))) is True):
                Reverse += 1
                TopThirdMatchRev += 1
                print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
                print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
            #MatchTopThird Inv to Read one: confirms correctly oriented fragments
            elif (bool(re.search( 'CAACTTGCCGGTCAGT', ''.join(R2_Seq[80:110]))) is True):
                AsIs += 1
                TopThirdMatchCor += 1                     
                print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
                print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
              
            #Last Ditch to Read one: confirms correctly oriented fragments
            elif (bool(re.search( 'TCCGCGAGA', ''.join(R1_Seq[45:65]))) is True):
                AsIs += 1
                LastDitchCor += 1                     
                print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
                print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
                
            ##Last Ditch to Read two: inverted oriented fragments
            elif (bool(re.search( 'TCCGCGAGA', ''.join(R2_Seq[45:65]))) is True):
                Reverse += 1
                LastDitchRev += 1
                print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
                print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
              
            ##MatchTopThird Inv seed to Read two: inverted oriented fragments
            elif (bool(re.search( 'TCTCGCGGA', ''.join(R1_Seq[65:80]))) is True):
                Reverse += 1
                LastDitchRev += 1
                print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
                print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
            #MatchTopThird Inv to Read one: confirms correctly oriented fragments
            elif (bool(re.search( 'TCTCGCGGA', ''.join(R2_Seq[65:80]))) is True):
                AsIs += 1
                LastDitchCor += 1                     
                print >>FivePrime, ''.join(R1_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
                print >>ThreePrime, ''.join(R2_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)    
            
            else:
            	print >>Garbage, ''.join(R1_Name)+"\t"+''.join(R1_Qual)+"\t"+''.join(R2_Qual)

print "Total Correct (5' ends Read 1 and 3' ends Read2): ",AsIs
print "Total Swapped (5' ends Read 2 and 3' ends Read1): ",Reverse
print "Percent Read: ",100*((AsIs+Reverse)/TotCount)
print "Total Correct 5' Seed Matches to R1 (Correct): ", FivePrimeMatch
print "Total Correct 3' Seed Matches to R1 (Inverted): ", ThreePrimeMatchR1
print "Total Correct 3' Seed Matches to R2 (Correct): ", ThreePrimeMatchR2
print "Total Correct 5' Seed Matches to R2 (Inverted): ", FivePrimeMatchR2
print "Total Correct Middle Matches (Correct): ", MidMatchCor
print "Total Correct Middle Matches (Inverted): ", MidMatchRev
print "Total Correct Last Ditch 9bp Match (Correct): ", LastDitchCor
print "Total Correct Last Ditch 9bp Match (Inverted): ", LastDitchRev
print "Total Correct Top Third Matches (Correct): ", TopThirdMatchCor
print "Total Correct Top Third (Inverted): ", TopThirdMatchRev
print "Total Align KpnI, XbaI, and backbone (Correct): ", DoubleSeedMuts
print "Total R1 Align 5' SfiI (Correct): ", LotsMuts

