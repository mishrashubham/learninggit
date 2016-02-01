pollutantmean<-function(directory,id=1:10){

  l<-list.files(directory)
  
  sums <- 0
  counts <- 0
  for (i in id){
    b<-read.csv(paste0(directory,"/",l[i]))
    b
    x.sub3 <- subset(b,select = c("nitrate","sulfate"))
    k<-table(factor(complete.cases(x.sub3)))[["TRUE"]]
    
  }
}


















