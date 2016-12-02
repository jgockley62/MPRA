#! python
import sys;
import os
import subprocess

#This Script Translate the Genomic alignment back to fragment assignment 
#TRANSLATION FILE:
#LOC=~/Genomes/MPRA/Lib_Align_Files/Condensed_HC_Lib/Masked_LibTranslation.txt
#Chr10:100590123-100590143_NeGCNTRL	chr10:100590051-100590215_12_152_140
FileT = '/home/jkg36/Genomes/MPRA/Lib_Align_Files/Condensed_HC_Lib/Masked_LibTranslation.txt'
FT= open(FileT)

Translate = {}

for line in FT:
        LINE = line.rstrip('\r\n')
        Lst = LINE.split('\t')
        
        Translate[Lst[1].strip(' ')] = Lst[0].strip(' ')
         
File = sys.argv[1]
F1= open(File)
#File
#HWI-D00306:695:HK5VKBCXX:2:1101:1541:1884	 AAACGACCGGTTGTGG        chr2b:129200368-129200658_Chimp_76_213_137	 137M    0	 137     137     0	 0	 0	 0	 0	 0	 0 $
for line in F1:
        LINE = line.rstrip('\r\n')
        Lst = LINE.split('\t')
        
        if Lst[2].strip(' ') in Translate:
        	Temp = Translate[Lst[2].strip(' ')]
        	Lst[2] = Temp
        	Entry = "\t".join(Lst)
        	print Entry
        else:
        	pass

