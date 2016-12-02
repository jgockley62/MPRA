#! python
import sys;
import os
import subprocess

#This script will remove all reads from repeated tags
#python RepeatFilter.py

File1 = 'RepeatedTags.txt'
File2 = 'Translated_Parsed_Cigar_withTAG_TrimedPI_gt88_temp.txt'

Filter = {}
F1= open(File1)
for line in F1:    
    LINE = line.rstrip('\r\n')
    Filter[LINE] = LINE
F1.close()

TotalFile = open("UniqTags_Translated_Parsed_Cigar_withTAG_TrimedPI_gt88.txt", "w")

F2= open(File2)
for line in F2:
	LINE = line.rstrip('\r\n')
	Lst = LINE.split('\t')
	if Lst[1] in  Filter:
		pass
	else:
		print >>TotalFile, LINE
F2.close()
