
args=(commandArgs(TRUE))
ID <- args[1]
print(ID)
Anote <- function(Temp){
  
  Foo<-cbind(Temp[,1:14], Temp[,6])
  Foo<-cbind(Foo[,1:15], Foo[,8]+Foo[,9]+Foo[,10]+Foo[,11]+Foo[,12]+Foo[,13]+Foo[,14]) 
  Foo<-cbind(Foo[,1:16], (Foo[15]-Foo[,16])/Foo[,15])
  colnames(Foo)<-c("Name", "Tag", "Alingment", "CIGAR", "NM", "Length", "M-M", "MisMatches","Insertion","Deletion","Skip","SoftClip","HardClip","Padding","ActualLen", "Diffs", "PercentID")
  return(Foo)
}

Liba <- read.table(file="CigarParsedMatched.txt", header=T, sep="\t")
Lib2a<-Anote(Liba)
LibaTrim<-Lib2a[Lib2a[,17] > ID,]
write.table(LibaTrim,"Parsed_Cigar_withTAG_TrimedPI_gt88_temp.txt" , sep = "\t", row.names = F, col.names = F)

q()
