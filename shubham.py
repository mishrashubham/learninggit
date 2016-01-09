from pyspark import SparkConf, SparkContext
from pyspark.sql import *
from optparse import OptionParser
import commands
parser = OptionParser()
parser.add_option("--file",dest="file_path",
                    help="Start Time for data,eg:-December 19 14:25:00 2015")
parser.add_option("--out",dest="op_path")

(options, args) = parser.parse_args()
APP_NAME = " HelloWorld of Big Data"
def showresult(sc1,filename):
  status,output=commands.getstatusoutput("hdfs dfs -lsr %s > temp.txt"%filename)
  status,output=commands.getstatusoutput("hdfs dfs -put /var/home/root/temp.txt /data/collector")
  k=sc1.textFile("/data/collector/temp.txt")
  p=k.map(lambda x: "/"+x.split("/",1)[1].strip("\n")).collect()
  f=open("refoutput.txt","w+")
  for i in p:
       f.write("%s\n"%i)
     
  return p
def processing(sc1,sqlContext,x):
   t=showresult(sc1,filename)
   f=open("%s"%x,"a+")
   
   for i in t:
       if "_DONE" not in i:
         f.write("for partition %s"%i)
         SubSegFile = sqlContext.parquetFile("%s"%i)
         output=SubSegFile.map(lambdareplica).collect()
         #print output
         for k in output:   
             f.write("%s\n"%list(k))
   
         f.write("\n\n")
def lambdareplica(x):
       return x[0],x[1]
    

if __name__=="__main__":
   conf = SparkConf().setAppName(APP_NAME)
   conf = conf.setMaster("local[*]")
   sc1   = SparkContext(conf=conf)
   sqlContext = SQLContext(sc1)
   filename=options.file_path
   output_file=options.op_path
   showresult(sc1,filename)
   processing(sc1,sqlContext,output_file)
