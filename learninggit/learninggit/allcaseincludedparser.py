import json
from pprint import pprint
import pickle
import sys
import os
from optparse import OptionParser
import re
import time
parser = OptionParser()
parser.add_option("--instartTime",
                  dest="Input_StartTime",
                  default="2015-08-10-10",
                  help="Start Time for input data (Default = 2015-08-10-10)")
parser.add_option("--jobtype",
                   dest="Job",
                   help="which job's output to be parse i.e CoreJobCubes or Edrcubes")
parser.add_option("--out",dest="op_path",
                   help="the file in which you want to write the converted data")
parser.add_option("--type",dest="TYPE",
                   default="all",
                   help="you want all the cubes to be emiited by a job a dumped into a file or want selectivecubes.Use 1.)all for all cubes,2.)Select for selective cubes")
parser.add_option("--id",dest="cubeid",
                   help="mention the cube id in comma separated form")
                   

(options, args) = parser.parse_args()

def time_convertor():
  in_st_struc=time.strptime(options.Input_StartTime,"%Y-%m-%d-%H")

  in_st_epoc=int(time.mktime(in_st_struc))
  expcted_format=time.strftime('%Y/%m/%d/%H',time.gmtime(in_st_epoc))
  return expcted_format

def header():
 list=["/data/cubedpi.json","/data/cubetethering.json"]
 d=dict()
 for r in list:
  with open(r) as data_file:
    data = json.load(data_file)
    if r=="/data/cubedpi.json":

      atlascubes=data["cubes"].keys()
    else:
      tetheringcubes=data["cubes"].keys()
  for i in data["cubes"].keys():
    for y in data["cubes"][i].keys():
        if y=="dimension_types":
         dimension_set=[str(k.keys()).strip("]").strip("[").strip("u'")+"(dimension)" for k in data["cubes"][i][y]]
         for m in dimension_set:
          if bool(re.search(r'\',(\s)(\w)\'_',m)):
             index_value=dimension_set.index(m)
             dimension_set[index_value]=re.sub(r'\',(\s)(\w)\'.*','',dimension_set[index_value])+"(dimension)"
        elif y=="measure_operations":
         measure_set=[str(k.keys()).strip("]").strip("[").strip("u'")+"(measure)" for k in data["cubes"][i][y]]
        else:
           continue
    m=dimension_set+measure_set
    d[i]=m
 return d

def splitter(path,cubes,file):
   time_format=time_convertor()
   print time_format
   s=header()
   k=cubes
   for i in k:
    file.write("Cube_id: %s\n"%i)
    try:
      if options.Job=="CoreJobcubes":
        getRec = 'hdfs dfs -text %s/%s/*/X.*|grep -i "^%s\^" > result.txt'%(path,time_format,i)
      else:
        getRec = 'hdfs dfs -text %s/%s/X.*|grep -i "^%s\^" > result.txt'%(path,time_format,i)
      if i in s.keys():
            print "x"            
            getOutput = os.system(getRec)
            print "y"
            file.write("%s\n"%s[i])
            for line in open("result.txt", "r"):
            
                line = line.strip("\n")
                if i!='123':  
                   line = re.split(r'(\s)0',line)
                else:
                   line = re.split(r'(\s)1',line)
                dimension = line[0]
                measure = line[2]

                dimension_x= dimension.split("^")
                matching_pattern=bool(re.search( r'(\d{1}).*(\d{1}).*(\d{1})',dimension_x[2],re.M|re.I))
                if not matching_pattern:
                  dimension= dimension.split("^")

                  if i=="200010":
                   dime=dimension[5:]
                   complete_dimension=[re.sub(r'\]\[(\d{2})|\]+','',p) for p in dime]

                  else:  
                   getNo = dimension[2][-1]
                   getNo = int(getNo)
                   final_dim = dimension[3:3+getNo]
                
                   popped_value = final_dim[-1]
                   popped_value = popped_value.split("]")
                   popped_get = popped_value[0]
                   final_dim.pop()
                   final_dimension = final_dim + [popped_get]
                   if "SUBCR(dimension)" in s[i] or i in ['83','84','85','133','200011','200002','200003']:
                    algo = dimension[-1].strip("]]")
                    complete_dimension = final_dimension + [algo]
                   else:
                    complete_dimension = final_dimension
                  
                else:
                 dimension_y = str(dimension).split("[")
                 getNo = dimension_y[1]
                 getNo = int(getNo)
                 final_dim = dimension_y[2:2+getNo]
                 complete_dimension=[re.sub(r'\[|\]+$|(\d+)\^','',y) for y in final_dim]
                if i!='123':   
                 measure = measure.split("^")
                 getMeasureNo = measure[0][-1]
                 getMeasureNo = int(getMeasureNo)
                 final_mea = measure[1:1+getMeasureNo]
                 popped_mea = final_mea[-1]
                 popped_mea = popped_mea.split("]")
                 popped_mea_get = popped_mea[0]
                 final_mea.pop()
                 final_measure = final_mea + [popped_mea_get]
                 if "SUBCR_COUNT(measure)" in s[i]:
                    if i in ['27','4']:
                     final_measure=final_measure+[measure[9].split(")")[0].strip("'(")]
                    elif i in ['200010','200004','200006']:
                     if options.Job=="CoreJobcubes":
                     
                      final_measure1=final_measure+[measure[-2].split(")")[0].strip("'(")]
                      final_measure=final_measure1+[measure[-1].split(")")[0].strip("'(")]
                     else:
                      final_measure1=final_measure+[measure[-3].split(")")[0].strip("'(")]
                      final_measure=final_measure1+[measure[-2].split(")")[0].strip("'(")]
                    else: 
                     final_measure=final_measure+[measure[-2].split(")")[0].strip("'(")]
                else:
                     measure = measure.split("^")
                     final_measure=re.sub(r'\]\](\d)\[(\d)|\]+','',measure[4])
                     final_measure=[final_measure]
                final_list=complete_dimension + final_measure
                file.write("%s\n"%final_list)

    except IndexError:
          if i=='200002':

                 dimension= dimension.split("^")
                 getNo = dimension[2][-1]
                 getNo = int(getNo)
                 final_dim = dimension[3:3+getNo]
                
                 popped_value = final_dim[-1]
                 popped_value = popped_value.split("]")
                 popped_get = popped_value[0]
                 final_dim.pop()
                 final_dimension = final_dim + [popped_get]
                 algo = dimension[-1].strip("]]").strip("]]\t'")
                 complete_dimension = final_dimension + [algo]
                 final_measure=["No values for measure found"]
                 
                 final_list=complete_dimension + final_measure

                 file.write("%s\n"%final_list)
          else:
              file.write("indexerror for :%s"%i)
          continue
    file.write("\n\n")
def  edrtopnsplitter(path,cubes,file):
   s=header()
   time_format=time_convertor()
   k=cubes
   first=['68','67','69','50','53','54','51','52','55','70']
   last=['65','66','46','47','81','82','87','86','88','89','91','90','129','130','134','135']
   for i in k:
    file.write("Cube_id: %s\n"%i)
    getRec = 'hdfs dfs -text %s/%s/X.*|grep -i "^%s\^" > result.txt'%(path,time_format,i)
    if i in s.keys():
            getOutput = os.system(getRec)
            file.write("%s\n"%s[i])
            for line in open("result.txt", "r"):
                 line = line.strip("\n")
                 dimension= line.split("^")
                 getNo = dimension[2][-1]
                 getNo = int(getNo)
                 final_dim = dimension[3:3+getNo]
                
                 popped_value = final_dim[-1]
                 popped_value = popped_value.split("]")
                 popped_get = popped_value[0]
                 final_dim.pop()
                 final_dimension = final_dim + [popped_get]
                 if i in last :
                    algo = dimension[-1].strip("]]").strip("]]\t'")
                    complete_dimension = final_dimension + [algo]
                 else:
            
                    complete_dimension = final_dimension
                 file.write("%s\n"%complete_dimension)

if __name__=="__main__":
   output_path=options.op_path
   file1=open(output_path,"w+")
   corejob_cubes=['5', '6', '7', '8', '9', '10', '11', '12', '18', '19', '22', '23', '24', '27', '28', '29', '30', '31', '35', '36', '39', '40', '41', '59', '63', '64', '80', '83', '84', '85','4', '98', '99', '100', '101', '102', '103', '104', '105', '109', '123', '128', '133', '151', '152', '156','200001','200002','200003','200004','200005','200006','200007','200008','200009','200012','200011','200010']
   edr_cubes_rollupcubes=['4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '59', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107', '151', '152']
   edr_cubes_top_n_cubes=['46', '47', '50', '51', '52', '53', '54', '55', '65', '66', '67', '68', '69', '70', '81', '82', '86', '87', '88', '89', '90', '91', '129', '130', '134', '135']
   edr_cubes_rollupcubes_teth=['200004','200005','200006']
   edr_cubes_AtlasSubcrBytes=['44']
   edr_cubes_AtlasSubDevs=['123']
   path1="/data/output/AtlasRollupCubes"
   path2="/data/output/TopN"
   path3="/data/output/AtlasSubcrBytes"
   path4="/data/output/AtlasSubDevs"
   path0="/data/output/CoreJobCubes"
   if options.TYPE=="all":
    if options.Job=="CoreJobcubes":
      file1.write("corejobcubes\n") 
      splitter(path0,corejob_cubes,file1)
    else:

        file1.write("edr_cubes_rollupcubes\n")
        file1.write("\n")   
        splitter(path1,edr_cubes_rollupcubes,file1)
        splitter(path1,edr_cubes_rollupcubes_teth,file1)
        file1.write("edr_cubes_top_n_cubes\n")
        file1.write("\n")
        edrtopnsplitter(path2,edr_cubes_top_n_cubes,file1)
        file1.write("edr_cubes_AtlasSubcrBytes\n")
        file1.write("\n")
        splitter(path3,edr_cubes_AtlasSubcrBytes,file1)
        file1.write("edr_cubes_AtlasSubDevs\n")
        file1.write("\n")
        splitter(path4,edr_cubes_AtlasSubDevs,file1)
   else:
      cube_set=options.cubeid.split(",")
      print cube_set
      for i in cube_set:
       print "x:",i
       if options.Job=="CoreJobcubes":
        if i in corejob_cubes:
            cube_list=i.split(",")
            splitter(path0,cube_list,file1)
       else:
        if i in edr_cubes_rollupcubes:
           cube_list=i.split(",") 
           splitter(path1,cube_list,file1)
        elif i in edr_cubes_top_n_cubes:
            cube_list=i.split(",")
            edrtopnsplitter(path2,cube_list,file1)
        elif i in edr_cubes_AtlasSubcrBytes:
            cube_list=i.split(",")
            splitter(path3,cube_list,file1)
        elif i in edr_cubes_rollupcubes_teth:
           cube_list=i.split(",")
           splitter(path1,cube_list,file1)
        else:
          cube_list=i.split(",")
          splitter(path4,cube_list,file1)

   os.system("rm -rf /data/result.txt")



