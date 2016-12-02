#!/usr/bin/python
#This Script will Parse CIGAR Strings inorder to calculate percent Identity

import sys; 
import pysam
#import math
#from decimal import *

#Example Comand:
#python FINAL_Genomic_Parser.py <INUPUT.bam> ~/Scripts/LibTranslation.txt

bamFile    = sys.argv[1];
Translator = sys.argv[2];

KEY = {}
F1= open(Translator)

for line in F1:
	LINE = line.rstrip('\r\n')
	lst = LINE.split('\t')
	KEY[lst[1]] = lst[0]

#Open Output Files
Parsed = open("CigarParsedMatched.txt", "w")
print >>Parsed, "Read_Name","\t","Reference","\t","Cigar","\t","NM","\t","Match+Mismatch","\t","Matches","\t","MisMatches","\t","Insertion","\t","Deletion","\t","Skip","\t","SoftClip","\t","HardClip","\t","Padding"

Failed = open("CigarParsedFailed.txt", "w")
print >>Failed, "Read_Name","\t","Reference","\t","Cigar","\t","NM","\t","Match+Mismatch","\t","Matches","\t","MisMatches","\t","Insertion","\t","Deletion","\t","Skip","\t","SoftClip","\t","HardClip","\t","Padding"

bamFP = pysam.Samfile(bamFile, "rb");

for read in bamFP:
	if( not( read.is_unmapped ) ):   #if it's mapped
		cigarLine=read.cigar;
		Tags = read.tags
		cigarTwo=read.cigarstring;
		name=read.qname
		FAName=bamFP.getrname(read.tid)
		Legth_on_Ref = read.alen
		Start = read.reference_start
                End = read.reference_end
                Flag = read.flag
                UniqID = '_'.join([FAName,str(Start),str(End),str(Legth_on_Ref)])
		
		Seq=read.query
		MM=0
		Insertion = 0
		Deletion = 0
		Skip = 0 
		SoftClip = 0
		HardClip = 0
		Padding = 0
		NM = 0
		
		#Get Edit Distance Tag
		for (TagType,TagLength) in Tags:
			#try:
			if(  TagType == "NM"): #NM number
				NM = TagLength     
			else:
				pass
			
		
		for (cigarType,cigarLength) in cigarLine:
			#try:
			if(  cigarType == 0): #match/mismatch
				MM = MM+cigarLength               
			elif(cigarType == 1): #insertions
				Insertion = Insertion+cigarLength
			elif(cigarType == 2): #deletion
				Deletion = Deletion+cigarLength
			elif(cigarType == 3): #skip
				Skip = Skip+cigarLength
			elif(cigarType == 4): #soft clipping
				SoftClip = SoftClip+cigarLength
			elif(cigarType == 5): #hard clipping
				HardClip = HardClip+cigarLength
			elif(cigarType == 6): #padding
				Padding = Padding+cigarLength
			else:
				print "Wrong CIGAR number";
				sys.exit(1);
			
			#except:
				#print "Problem";
		
		Mismatches = NM-(Insertion+Deletion)
		Matches = MM-Mismatches
		if UniqID in KEY:
			print >>Parsed, name,"\t",UniqID,"\t",cigarTwo,"\t",NM,"\t",MM,"\t",Matches,"\t",Mismatches,"\t",Insertion,"\t",Deletion,"\t",Skip,"\t",SoftClip,"\t",HardClip,"\t",Padding
		else:
			print >>Failed, name,"\t",UniqID,"\t",cigarTwo,"\t",NM,"\t",MM,"\t",Matches,"\t",Mismatches,"\t",Insertion,"\t",Deletion,"\t",Skip,"\t",SoftClip,"\t",HardClip,"\t",Padding


print "DONE"
