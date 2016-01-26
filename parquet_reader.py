from pyspark import SparkConf, SparkContext
from pyspark.sql import *
from optparse import OptionParser
import commands
import time
parser = OptionParser()
parser.add_option("--file",dest="file_path",
                    help="file you want to convert")
parser.add_option("--out",dest="op_path",
                   help="the file in which you want to write the converted data")
parser.add_option("--instartTime",
                  dest="Input_StartTime",
                  default="2015-08-10-10",
                  help="Start Time for input data (Default = 2015-08-10-10-00)")
parser.add_option("--inendTime",
                  dest="Input_EndTime",
                  default="2015-08-10-10",
                  help="End Time for input data (Default = 2015-08-10-10-00)")
(options, args) = parser.parse_args()

APP_NAME = " HelloWorld of Big Data"
def convertor(epoc):
      k=time.strftime('%Y/%m/%d/%H/%M',time.gmtime(epoc))
      return k


def  header():
        l=[]
        f=open("/data/part-00000","r+")
        k=f.readline()
        p=k.split(",")
        for i in p:
         if "Row" in i:
           l.append(i.split("=")[0][4:].strip(" "))
         else:
            l.append(i.split("=")[0].strip(" "))
        l=str(l).rstrip("]").lstrip("[")
        return l

def showresult(sc1,filename):
  in_st_struc=time.strptime(options.Input_StartTime,"%Y-%m-%d-%H-%M")

  in_st_epoc=int(time.mktime(in_st_struc))
  print in_st_epoc
  out_st_struc=time.strptime(options.Input_EndTime,"%Y-%m-%d-%H-%M")
  out_st_epoc=int(time.mktime(out_st_struc))
  print out_st_epoc
  while in_st_epoc<=out_st_epoc:
     converted_time=convertor(in_st_epoc)
     print "cycle started:",converted_time
     status,output=commands.getstatusoutput("hdfs dfs -lsr %s/%s >> temp.txt"%(filename,converted_time))
     in_st_epoc+=300
     print "cycle done:",converted_time
  status,output=commands.getstatusoutput("hdfs dfs -put temp.txt /data/collector")
  status,output=commands.getstatusoutput("rm -rf temp.txt")
  k=sc1.textFile("/data/collector/temp.txt")
  p=k.filter(lambda x:int(x.split()[4])!=0).map(boundary).collect()
  f=open("refoutput.txt","w+")
  for i in p:
       f.write("%s\n"%i)
  status,output=commands.getstatusoutput("hdfs dfs -rmr /data/collector/temp.txt")
  status,output=commands.getstatusoutput("rm -rf refoutput.txt")
  return p
def boundary(x):
         return x.split()[-1].strip("\n")
def processing(sc1,sqlContext,filename,x):
  try:
   t=showresult(sc1,filename)
   f=open("%s"%x,"w+")
   SubSegFile2=sqlContext.parquetFile("%s"%t[0])
   SubSegFile2.saveAsTextFile("/data/collector/header")
   status,output=commands.getstatusoutput("hdfs dfs -get /data/collector/header/part-00000  /data/")
   status,output=commands.getstatusoutput("hdfs dfs -rmr /data/collector/header")
   header_list=header()
   f.write("%s\n\n"%header_list)
   for i in t:
     if ("_DONE" or "_SUCCESS") not in i:
         SubSegFile = sqlContext.parquetFile("%s"%i)
         output=SubSegFile.map(done).collect()
         print "this is output:",output
         if len(output)!=0:
          for k in output:  
             f.write("%s\n"%list(k))
             f.write("\n\n")
          f.write("\n\n")
  finally:
      status,output=commands.getstatusoutput("hdfs dfs -rmr /data/collector/header")   
def done(x):
    if len(x)!=0:
      return x
if  __name__=="__main__":
   conf = SparkConf().setAppName(APP_NAME)
   conf = conf.setMaster("local[*]")
   sc1   = SparkContext(conf=conf)
   sqlContext = SQLContext(sc1)
   sqlContext.sql("SET spark.sql.parquet.binaryAsString =True")
   filename=options.file_path
   output_file=options.op_path
   processing(sc1,sqlContext,filename,output_file)

