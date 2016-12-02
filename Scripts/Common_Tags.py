#! python
import sys;

#This program takes the competent library tag sequencing file and the 
#Inert library Tag_Counts.txt file and gives the Inert reads that are represented in the competent library
#Example
#python Common_Tags.py /Users/Sazerac/Dropbox/MPRA_Data/2016_11_10_Comp_LibSeq/Tag_merge_counts.txt /Users/Sazerac/Dropbox/MPRA_Data/Inert_Lib_Seq_Results_88PI/Tag_Counts.txt

Competant = sys.argv[1]
F1 = open(Competant)

Inert = sys.argv[2]
F2 = open(Inert)

CompTags = {}

for line in F1:
	LINE = line.rstrip('\r\n')
	lst = LINE.split('\t')
	CompTags[lst[0]] = lst[0]
	
F1.close();
OUT = open("Inert_TagCounts_In_Comp.txt", "w")

for line in F2:
	LINE = line.rstrip('\r\n')
	lst = LINE.split('\t')
	
	if lst[0] in CompTags:
		print >>OUT, LINE
	
	else:
		pass
print "Done!"
	
