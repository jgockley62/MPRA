#!/usr/bin/env Rscript
##Exp
#R CMD BATCH PercentID.R
#####Inert Library Processing Code
#args <- commandArgs(trailingOnly = F)
#myargument <- args[length(args)]
#myargument <- sub("-","",myargument)

#FILE <- args[1]
#LibType <-args[2]
#setwd("/Users/Sazerac/Desktop/MPRA_StrandTestSCRIPT/CIGAR_STRING_PARSE/")
WD<-getwd()

Parsed<-read.table(file="UniqTags_Translated_Parsed_Cigar_withTAG_TrimedPI_gt88.txt", header=F, sep="\t")

dim(Parsed[Parsed[,17] >= .98,])[1]
dim(Parsed[Parsed[,17] >= .95,])[1]

#ID
pdf(file=paste(WD,"/","PercentID.pdf",sep=""))
  plot.new()
  hist(Parsed[,17], breaks=200, xlim=c(.88,1), las=1, main="Percent ID", xlab="Percent ID", font=2)
  rect(par("usr")[1], par("usr")[3], par("usr")[2], par("usr")[4], col = "grey")
  hist(Parsed[,17], breaks=200, xlim=c(.88,1),col="lemonchiffon4", las=1, add=TRUE, main="Percent ID Chimp Lib", xlab="Percent ID", font=2)
  abline(v=.95, col="yellow", lwd=3, lty=4)
  abline(v=.98, col="red", lwd=3, lty=4)
dev.off()
