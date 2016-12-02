#! python
import sys;

##Script takes Two counts.txts file and merges them

##Usage:
#python Tag_Merger.py 2016_10_31_Tag_Counts.txt 2016_10_20_Tag_Counts.txt

File1 = sys.argv[1]
F1= open(File1)

File2 = sys.argv[2]
F2= open(File2)

TotalFile = open("Tag_merge_counts.txt", "w")

Tags = {}

for line in F1:
        LINE = line.rstrip('\r\n')
        Lst = LINE.split('\t')
        Tags[Lst[0]] = int(Lst[1])
        

for line in F2:
        LINE = line.rstrip('\r\n')
        Lst = LINE.split('\t')
        if Lst[0] in Tags:
        	Tags[Lst[0]] = int(Tags[Lst[0]])+ int(Lst[1])
        else:
        	Tags[Lst[0]] = Lst[1]
       
        	
for key, value in Tags.iteritems():
    Entry = '\t'.join([key,str(value)])
    print >>TotalFile, Entry

        
print "Done"

