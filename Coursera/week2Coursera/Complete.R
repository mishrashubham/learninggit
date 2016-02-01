complete<-function(directory,id=1:332){
  l<-list.files(directory)
  d<-data.frame()
  for (i in id){
    b<-read.csv(paste0(directory,"/",l[i]))
    if(table(factor(complete.cases(b)))[["FALSE"]]==nrow(b)){
      value<-0
    }
    else{
      value<-table(factor(complete.cases(b)))[["TRUE"]]
    }
    d<-rbind(d,c(i,value))
  }
  colnames(d)<-c("id","nobs")
  d
}