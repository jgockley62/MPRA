MPRA Pipeline Maual
========================================================

This pipeline is designed to process and aggregate GZipped Fastq files from MPRA sequenceing runs. The software requirments of the pipeline are as follows, the version represents the version under which the pipeline was built. This pipeline is specific to MPRA assays which are comparing allele states as the Annotation run mode will look to incorperate a translation file between allele states to include CRE and corresponding comparison allele CRE in the same line.

Python - Version: 2.7.12

R - Version 3.2.1

Bowtie2 - Version: 2.2.9

samtools - Version: 0.1.18

cutadapt - Version: 1.4.1

pear - Version: 0.9.10

FASTX Toolkit - Version: 0.0.13

## Total Flag List

-h, --help                  Show this help message and exit

-r RUN, --run           Specify Run Mode. Options: COMP, INERT, EXP, TAGComparison, or ANOTE

-R1, --Read1     Read 1 file or comma delimited list of Read 1 files. Use a comma at the end of a single file path with * autocomplete flag
  
-R2, --Read2    Read 2 file or comma delimited list of Read 2 files. Use a comma at the end of a single file path with * autocomplete flag

-s, --sample         Sample Type. Must specify if in EXP mode ex. Rep2_1_pDNA

-PI, --PercentID  Percent ID Threshold. Must an decimal >= 0 and <= 1

-I, --INERTtag     Inert tag counts, must specify when in annotate mode

-C, --COMPtag       Competent Library Seq Tag Counts Optional to specify in annotate mode

-EP, --PLAStag      Experimental Plasmid Tag Counts: can be a single file or comma delimited list of Read 1 files. Use a comma at the end of a single file path with * autocomplete flag.

-ET, --TRANtag      Experimental Transcript Tag Counts: can be a single file or comma delimited list of Read 1 files. Use a comma at the end of a single file path with * autocomplete flag.

-R, --Resource     File Path to Annotation Resource Files

-o, --out     Specify the out file to store Pipeline Log

## Run Modes:

### Inert Run Mode (-r INERT)
This mode processes Inert tag 2x250bp reads. These reads must be generated with the corresponding primer sets to ensure that the Strander sub routine is properly applied. Tags with multiple CRE assignments are discared in this run mode after filtering for percent ID. 

Example Call:

```r
  python Pipeline.py -r INERT -PI .98 -R1 ReadGroup1.fastq.gz -R2 ReadGroup2.fastq.gz -R Path/To/Resource/Files/ -o Inert_Pipeline_OUT.txt
```

Required Flags:

-PI: Specify the percent identity as a decimal to filter aligned CREs. Only fragments which have X% of bases matching the reference CRE. Deletions and insertions are also scored the same as a mutation therefore with a 140bp fragment and PI of .98 there can be no more than 2 base changes, deletions, or insertions within the CRE sequence.

-R1 and -R2: Specify the read one and read two files. These files must be gziped fastq files. Reads can be specified in four ways. Reads can be specified as; 

* Single files. ex: -R1 File1.fastq.gz

* A comma delimited list of files. ex: -R1 File1.fastq.gz,File2.fastq.gz 

* An autocompleted file path (If only a single path you MUST put a comma delimter at the end!). ex: -R1 Path_to/File\*.fastq.gz, 

* A comma delimited list of autocompleted file paths. ex: -R1 Path_to/File\*.fastq.gz,Different_Path_to/File\*.fastq.gz 

-R: Path to resource files used for file processing. Must include trailing backslash! Specific files required for INERT Library processing are:

* A tab delimited translation file of fragment name (Col 1) to alignment corrdinates to the Library Bowtie2 library index (Col 2)

* A Bowtie2 Library index

* ProcessR_Pipeline.R

-o: Output logfile, will store run details and log all calls exported to command line.

### Competent Run Mode (-r COMP)
This mode processes Competent tag 2x150bp reads. These reads must be generated with the corresponding primer sets to ensure that the Strander sub routine is properly applied. 

Example Call:

```r
  python Pipeline.py -r COMP -R1 ReadGroup1.fastq.gz -R2 ReadGroup2.fastq.gz -o Inert_Pipeline_OUT.txt
```

Required Flags:

-R1 and -R2: Specify the read one and read two files. These files must be gziped fastq files. Reads can be specified in four ways. Reads can be specified as; 

* Single files. ex: -R1 File1.fastq.gz

* A comma delimited list of files. ex: -R1 File1.fastq.gz,File2.fastq.gz 

* An autocompleted file path (If only a single path you MUST put a comma delimter at the end!). ex: -R1 Path_to/File\*.fastq.gz, 

* A comma delimited list of autocompleted file paths. ex: -R1 Path_to/File\*.fastq.gz,Different_Path_to/File\*.fastq.gz 

-o: Output logfile, will store run details and log all calls exported to command line.

### Experimental Run Mode (-r EXP)
This mode processes Experimental tag 2x150bp reads. These reads must be generated with the corresponding primer sets to ensure that the Strander sub routine is properly applied. This mode is called independently on Plasmid DNA reads and Transcript cDNA Reads.  

Example Call:

```r
  python Pipeline.py -r EXP -s Rep_2_2_cDNA -R1 ReadGroup1.fastq.gz -R2 ReadGroup2.fastq.gz -o Inert_Pipeline_OUT.txt
```

Required Flags:

-R1 and -R2: Specify the read one and read two files. These files must be gziped fastq files. Reads can be specified in four ways. Reads can be specified as; 

* Single files. ex: -R1 File1.fastq.gz

* A comma delimited list of files. ex: -R1 File1.fastq.gz,File2.fastq.gz 

* An autocompleted file path (If only a single path you MUST put a comma delimter at the end!). ex: -R1 Path_to/File\*.fastq.gz, 

* A comma delimited list of autocompleted file paths. ex: -R1 Path_to/File\*.fastq.gz,Different_Path_to/File\*.fastq.gz 

-s Replicate Name handle. All files generated will start with this name handle.

-o: Output logfile, will store run details and log all calls exported to command line.

### Tag Comparison Run Mode (-r TAGComparison)
This mode processes will take the previously generated tag counts file from the INERT and COMP run modes and yield count files of shared tags between both the Inert and Competent librarys.

Example Call:

```r
  python ~/Scripts/Pipeline.py -r TAGComparison -I /Path/to/Inert_Tag_Counts.txt -C /Path/to/CompLib_Tag_Counts.txt -o TagMerge_Pipeline_OUT.txt
```

Required Flags:

-I:  Inert library tag counts file.

-C:  Competent library tag counts file. 

-o: Output logfile, will store run details and log all calls exported to command line.

### Annotation Run Mode (-r TAGComparison)
This mode will take Inert, Competent, and Experimental tag counts files and annotate them with fragment coordinates, species, orthologs, alleles, and the position of each allele within the CRE. This annotation file has one line per Tag sequence in the Inert Tag counts file. Additionally for Every CRE without a tag there will be an entry line where the tag sequence is NA.

Example Call:

```r
  python ~/Scripts/Pipeline.py -r ANNOTE -R /Path/To/Resource/Files -I Inert_Tag_Counts.txt -C CompLib_Tag_Counts.txt -EP Rep_1_2_pDNA_Tag_Counts.txt -ET Rep_1_2_cDNA_Tag_Counts.txt -o AnnoteTestOut.txt
```

Required Flags:
-R: Path to resource files used for file processing. Must include trailing backslash! Specific files required for INERT Library processing are:




-I:  Inert library tag counts file.

-C:  Competent library tag counts file.

-EP:  Plasmid tag count files specified in one of the four ways previously described for -R1 or -R2 files. Note: Listing files in corresponding replicate order to the -ET flag may simpilify analysis downstream.

-ET:  Transcript tag count files specified in one of the four ways previously described for -R1 or -R2 files.Note: Listing files in corresponding replicate order to the -EP flag may simpilify analysis downstream.

-o: Output logfile, will store run details and log all calls exported to command line.


### Resource File Descriptions

* Masked_LibTranslation.txt: Translates the parsed alignment of each library CRE to the library index to the CRE name. Generated by alighning the fragment library sent to custom array for synthesis to the bowtie library index. BAM file parsed by taking the chromosome start and stop position from the alignment BAM file to indicate which CRE to assign INERT read alignments. It is tab delimited. First column is the CRE name and the second column is an underscore delimited column of index chromosome contig, start, and stop position of the alignment.

* HC_GenomicBased_Library_Bwtie2Index.\*: This is the bowtie2 library index. This was created by taking the bed coordinates of all fragments (seperate files for each species), padding out by 10 base pairs, sorting and merging the bed cordinates. Then getting the sequence in FASTA format from either hg19 or pantro2 for human and chimp orthologs respectivly. Finally merging species specific FASTA files and submiting to bowtie2 for index construction. 

* ProcessR_Pipeline.R: This is the R script for processing the cigar parsed BAM alignment info, also applies the percent identity cutoff.

* Master_Ortholog_TranslatorFin.txt: This file is a tab delimited file which translates between allele/Orthologous CREs.

* Allele_Master.txt: This is a tab delimited file that has the zerobased coordinates and allele states for each eVar. 4 columns 1 and 3 are corordinates in Chr:Start-Stop format. Columns 2 and 4 are the allele states.

* Human_Subs_Intersect.txt: This file is the human eVar zero based bed coordinates intersected with the human library CRE Fragments. Bedtools was used with the -wa flag to output every single eVar alignment with each CRE to output every eVar - CRE overlap.  

* PanTro2_Subs_Intersect.txt: This file is the chimp eVar zero based bed coordinates intersected with the chimp library CRE Fragments. Bedtools was used with the -wa flag to output every single eVar alignment with each CRE to output every eVar-CRE overlap. 

* Hg_Subs_IntersectAnottate.txt: This is a tab delimited file consisting of one line for every induvidual Human eVar-CRE overlap instance. The first six columns are the bed coordinates of the CRE and eVar respectively. Column 7 is the base position of the eVar in the CRE and Column 8 is the allele state transition in the format of Ancestral->Human_State. 

* PanTro2_Subs_IntersectAnottate.txt: This is a tab delimited file consisting of one line for every induvidual Chimp eVar-CRE overlap instance. The first six columns are the bed coordinates of the CRE and eVar respectively. Column 7 is the base position of the eVar in the CRE and Column 8 is the allele state transition in the format of Ancestral->Human_State.

* Hg19_Fragments_Srt_Fin.bed: This is a tab delimited file consisting of the bed coordinates and name of the human CRE fragments.

* PanTro2_Fragments_srt.bed: This is a tab delimited file consisting of the bed coordinates and name of the chimp CRE fragments.

* Human_Frag_BPandAllele_Anonted.txt: This is a tab delimited file consisting of the bed coordinates and name of the human CRE fragments and in column 5 is a semicolon list of eVar alleles in the format of Ancestral->Human_State within the CRE. Column 6 is a semicolon delimited file of the base pair location of the eVar(s) within the CRE. 

* Chimp_Frag_BPandAllele_Anonted.txt: This is a tab delimited file consisting of the bed coordinates and name of the chimp CRE fragments and in column 5 is a semicolon list of eVar alleles in the format of Ancestral->Human_State within the CRE. Column 6 is a semicolon delimited file of the base pair location of the eVar(s) within the CRE. 








