#! python
import sys;
import os
import subprocess

#This script will Tabulate counts by tag and Tabulate Tags per Library Fragments
#python Tabulater.py

File1 = 'UniqTags_Translated_Parsed_Cigar_withTAG_TrimedPI_gt88.txt'

TagsCount = {}
TagsLibFrag = {}

F1= open(File1)
for line in F1:    
    LINE = line.rstrip('\r\n')
    Lst = LINE.split('\t')
    if Lst[1] in TagsCount:
    	TagsCount[Lst[1]] += 1
    else:
    	TagsCount[Lst[1]]  = 1
    	TagsLibFrag[Lst[1]] = Lst[2]
    	
F1.close()

TagFile = open("Tag_Counts.txt", "w")
LibCounts = {}

for key, value in TagsCount.iteritems():
	Entry = '\t'.join([key,str(TagsCount[key]),TagsLibFrag[key]])
	print >>TagFile, Entry
	
	if TagsLibFrag[key] in LibCounts:
		LibCounts[TagsLibFrag[key]] += 1
	else:
		LibCounts[TagsLibFrag[key]] = 1
LibFile = open("Lib_Counts.txt", "w")
for key, value in LibCounts.iteritems():
	Entry = '\t'.join([key,str(LibCounts[key])])
	print >>LibFile, Entry
	

