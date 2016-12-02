#! python
import sys;
##Script annotates parsed reads with tag sequences that are 16bp
##Usage
#python Cigar_Tag_Anote.py CigarParsed.txt Compiled_Cre_tags.txt
##CigarParsed.txt
#Read_Name	Reference	Cigar	NM	Match+Mismatch	Matches	MisMatches	Insertion	Deletion	Skip	SoftClip	HardClip	Padding

##Compiled_Cre_tags.txt
#ID	Fragment 	Tag	

CIGAR = sys.argv[1]
Compiled_Cre_tags = sys.argv[2]

F1= open(Compiled_Cre_tags)
ID_Tag = {}

for line in F1:
	LINE = line.rstrip('\r\n')
	Lst = LINE.split('\t')
	Id = Lst[0].strip(' ')
	ID = Lst[0].strip('@')
	Tag = Lst[2].strip(' ')
	if len(Tag) == 16:
		ID_Tag[ID] = Tag
	else:
		pass

F2 = open(CIGAR)
TotalFile = open("Parsed_Cigar_withTAG.txt", "w")

for line in F2:
	LINE = line.rstrip('\r\n')
	Lst = LINE.split('\t')
	id = Lst[0].strip(' ')
	
	if id != "Read_Name":
		if id in ID_Tag:
			Entry = id,ID_Tag[id],Lst[1],Lst[2],Lst[3],Lst[4],Lst[5],Lst[6],Lst[7],Lst[8],Lst[9],Lst[10],Lst[11],Lst[12]
			#print ID_Tag[id]
			print >>TotalFile, '\t'.join(Entry)
		else:
			pass
	else:
		pass

print "DONE"
