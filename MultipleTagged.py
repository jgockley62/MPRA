#! python
import sys;

##Script isolates 100% perfect alignments

##Usage:
#python MultipleTagged.py Parsed_Cigar_withTAG.txt

#Read_Name      TAG     Reference       Cigar   NM      Match+Mismatch  Matches MisMatches      Insertion       Deletion        Skip    SoftClip        HardClip        Padding
#0                      1       2                       3               4       5                               6               7                       8                       9                       10              11                      12                      13
#HWI-D00306:695:HK5VKBCXX:2:1101:1193:1955      TATTCACGAATTCCTA        Chr6:41436459-41436595_hsSUB    4M2D73M19D38M   21      115     115     0       0       21      0       0       0       0


File = sys.argv[1]
F1= open(File)

F1 = open(File)
TotalFile = open("RepeatedTags.txt", "w")

Tags = {}
RepTags = {}
for line in F1:
        LINE = line.rstrip('\r\n')
        Lst = LINE.split('\t')
        
        if Lst[1].strip(' ') in Tags:
        	if Lst[2].strip(' ') == Tags[Lst[1].strip(' ')]:
        		pass
        	else:
        		RepTags[Lst[1].strip(' ')] = Lst[1].strip(' ')
        else:
        	Tags[Lst[1].strip(' ')] = Lst[2].strip(' ')


for key, value in RepTags.iteritems():
    print >>TotalFile, key

TotalFil = open("SamEntries_RepeatedTags.txt", "w")   


F2 = open(File)

for line in F2:    
	LINE = line.rstrip('\r\n')
	Lst = LINE.split('\t')
	if Lst[1] in RepTags:
		print >>TotalFil, LINE
	else:
		pass
        
print "Done"


