#! python

import sys

#This script takes the Input Files from PI Down Sampling and outputs a combined counts file
#List files in ascending order of PI
##Example Call:
#python 2016_12_20_PI_DownSampleMerge.py PI88_Inert_Tag_Counts.txt PI_90_Inert_Tag_Counts.txt PI_92_Inert_Tag_Counts.txt PI_94_Inert_Tag_Counts.txt PI_96_Inert_Tag_Counts.txt PI_98_Inert_Tag_Counts.txt > Merged_INERT_Tag_Counts.tt
#Initalize master Hashe
Tags = {}

#List of dicts loaded
files = []

#File loading loop:
for numb in range (1,int(len(sys.argv))):
	#Initialize file hash and push into array
	exec( '_'.join(["PI",str(numb)]) + " = {}")
	exec( "files.append(dict(" + '_'.join(["PI",str(numb)]) + " ))")
	
	#Open File
	Handl = open(sys.argv[int(numb)])
		
	for line in Handl:
		LINE = line.rstrip('\n\r')
		lst = LINE.split('\t')
		
		#Load the designated hashes		
		Tags[lst[0]] = lst[0]
		#exec( "files[numb-1]" + '_'.join(["PI",str(numb)]) + "[lst[0]] = str(lst[1])")
		files[numb-1][lst[0]] = str(lst[1])
		
	#close file
	Handl.close();

#Print out Merged File
for tag in Tags:
	#Store tag bases as value
	counts = []
	
	#Loop indv hashes
	for hash in files:
		#If val exists store in counts, else store zero
		if (tag in hash):
			temp = str(hash[tag])		
			counts.append(temp)
		else:
			counts.append(0)
	entry = '\t'.join([tag,'\t'.join(str(x) for x in counts)])
	print entry
	
