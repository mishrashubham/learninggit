from pyspark import SparkConf, SparkContext
from pyspark.sql import *
from optparse import OptionParser
import commands
parser = OptionParser()
parser.add_option("--file",dest="file_path",
                    help="file you want to convert")
parser.add_option("--col",dest="columns",
                   help="columns u want to continue")
parser.add_option("--out",dest="op_path",
                   help="the file in which you want to write the converted data")
(options, args) = parser.parse_args()

APP_NAME = " HelloWorld of Big Data"

     
a,b,c,d,e= [int(i) for i in options.columns.split(",")]

def showresult(sc1,filename):
  status,output=commands.getstatusoutput("hdfs dfs -lsr %s > temp.txt"%filename)
  status,output=commands.getstatusoutput("hdfs dfs -put /var/home/root/temp.txt /data/collector")
  status,output=commands.getstatusoutput("rm -rf temp.txt")
  k=sc1.textFile("/data/collector/temp.txt")
  p=k.map(lambda x: "/"+x.split("/",1)[1].strip("\n")).collect()
  f=open("refoutput.txt","w+")
  for i in p:
       f.write("%s\n"%i)
  status,output=commands.getstatusoutput("hdfs dfs -rmr /data/collector/temp.txt")
  return p
def processing(sc1,sqlContext,x):
   t=showresult(sc1,filename)
   f=open("%s"%x,"a+")
   for i in t:
     if ("_DONE" or "_SUCCESS") not in i:
         SubSegFile = sqlContext.parquetFile("%s"%i)
         output=SubSegFile.map(lambdareplica).collect()
         for k in output:   
             f.write("%s\n"%list(k))
         f.write("\n\n")
def lambdareplica(x):
       return x[a],x[b],x[c],x[d],x[e]
    

if __name__=="__main__":
   conf = SparkConf().setAppName(APP_NAME)
   conf = conf.setMaster("local[*]")
   sc1   = SparkContext(conf=conf)
   sqlContext = SQLContext(sc1)
   sqlContext.sql("SET spark.sql.parquet.binaryAsString =True")
   filename=options.file_path
   output_file=options.op_path
   showresult(sc1,filename)
   processing(sc1,sqlContext,output_file)
