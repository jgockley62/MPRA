#! python
#This Script takes Cre Fastq and matches to Tag fastq
#Reads Must be ordered	

from itertools import izip, izip_longest
import re
import sys
import os

Read1 = sys.argv[1]
Read2 = sys.argv[2]

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
FivePrime = open("Compiled_Cre_tags.txt", "w")
Cres = open("Final_Cres.fastq", "w")
Tags = open("Final_Tags.fastq", "w")

Assign = {1: "R1_Name = LINE1; R2_Name = LINE2", 2: "R1_Seq = LINE1; R2_Seq = LINE2", 3: "R1_Strand = LINE1; R2_Strand = LINE2", 4: "R1_Qual = LINE1; R2_Qual = LINE2"}
LineCounter=1
#Loop through files simultaneously here 
#don't need izip longest bc mate pair files are same length
UnCut=0
with open(Read1) as file1, open(Read2) as file2:
    for line1, line2 in izip(file1, file2):  
        LINE1 = line1.rstrip('\r\n')
        LINE2 = line2.rstrip('\r\n')
        
        exec(Assign[LineCounter])
        
        
    	if(LineCounter < 4): #Name @
        	
        	LineCounter += 1
        	
        else:
        	LineCounter = 1
        	
        	#Split names to exclude read number
        	L1 = re.split('\s+', R1_Name)
        	L2 = re.split('\s+', R2_Name)
        	
        	if (L1[0] == L2[0]):
        		#print >>FivePrime, L1[0]+"\t"+R1_Seq+"\t"+R2_Seq
        		
        		if (R1_Seq == R2_Seq):
        			UnCut += 1
        		else:
        			print >>FivePrime, L1[0]+"\t"+R1_Seq+"\t"+R2_Seq
        			print >>Cres, ''.join(R1_Name)+"\n",''.join(R1_Seq)+"\n",''.join(R1_Strand)+"\n",''.join(R1_Qual)
        			print >>Tags, ''.join(R2_Name)+"\n",''.join(R2_Seq)+"\n",''.join(R2_Strand)+"\n",''.join(R2_Qual)
        		
        	else:
        		print "ERROR"
print UnCut
        	
        	
        	
        	
        	
        	
        	
        	
        	
        	
        	
        	