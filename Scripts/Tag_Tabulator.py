#! python
import sys;

##Script takes Tags.fastq and converts it to Tag_Counts.txt

##Usage:
#python Tag_Tabulator.py Tags.fastq

File = "Tags.fastq"
F1= open(File)

TotalFile = open("Tag_Counts.txt", "w")

Tags = {}
counter = 0
for line in F1:
        LINE = line.rstrip('\r\n')
        Lst = LINE.split('\t')
        ele = list(Lst[0])
        counter += 1
        
        if counter == 2:
        	#print Lst[0]
        	if len(ele) == 16:
        		if Lst[0] in Tags:
        			Tags[Lst[0]] += 1
        		else:
        			Tags[Lst[0]] = 1
        	else:
        		pass
        
        elif counter == 4:
        	counter = 0
        else:
        	pass
        	
for key, value in Tags.iteritems():
    Entry = '\t'.join([key,str(value)])
    print >>TotalFile, Entry

        
print "Done"

