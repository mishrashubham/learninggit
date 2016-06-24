'''
Created on 08-Apr-2016

@author: shubham.mishra
'''
import type_template_mapping
import xsd_lookup
import latest_file_selecter
import re
import operator
from xml.dom import minidom
import commands
def getter(file1,file2,path_for_reference_xsd, xsd_path):
    
     type_dict,service_provider_dict=type_template_mapping.csv_mapping_for_dat_type(file1, file2) 
     lookup_dict=xsd_lookup.parent_and_type_extracter(xsd_path)
     best_path_dict=latest_file_selecter.selector(path_for_reference_xsd, xsd_path)
     field_list=xsd_lookup.xsd_ref_value_extracter(xsd_path)
     return field_list,type_dict,service_provider_dict,lookup_dict,best_path_dict



def assigner(file1,file2,path_for_reference_xsd, xsd_path,):
  try:
    field_list1,type_dict1,service_provider_dict1,lookup_dict1,best_path_dict1=getter(file1,file2,path_for_reference_xsd, xsd_path)
    value_assigner={}
    fieldparameter=xsd_lookup.field_index(xsd_path) 

    for i in lookup_dict1:
      
        if i in best_path_dict1:
      
          #print i,lookup_dict1[i],best_path_dict1[i]
          file_for_extraction="%s/%s"%(path_for_reference_xsd,best_path_dict1[i])   
          for y in lookup_dict1[i]:
              if y in  value_assigner:
                k1=extracter(i,file_for_extraction,y)
                if k1.upper() in type_dict1:
                    k=type_dict1[k1.upper()]
                else:
                    k=k1   
                    
                value_assigner[y].append(k)
                value_assigner[y].append(fieldparameter.index(y)+1)
                temp_value=str(i)+":"+str(y)
                value_assigner[y].append(temp_value)
              else:
                value_assigner[y]=list() 
                k1=extracter(i,file_for_extraction,y)
                if k1.upper() in type_dict1:
                    k=type_dict1[k1.upper()]
                else:
                    k=k1
                
                value_assigner[y].append(k)
                value_assigner[y].append(fieldparameter.index(y)+1)
                temp_value=str(i)+":"+str(y)
                value_assigner[y].append(temp_value)
    
    for i in value_assigner:
        value_assigner[i].append("True")
  except IndexError:
     type_dict1,service_provider_dict=type_template_mapping.csv_mapping_for_dat_type(file1, file2)
     value_assigner={}
     interim_dict=boundary_case(xsd_path) 
    #print value_assigner 
     index_maintainer123=index_maintain(xsd_path)
     for i in interim_dict:
        value_assigner[i]=[]
        if interim_dict[i].upper() in type_dict1:
             type=type_dict1[interim_dict[i].upper()]
        value_assigner[i].append(type)
        if i in index_maintainer123:
             value_assigner[i].append(index_maintainer123[i])
        value_assigner[i].append(i)
        value_assigner[i].append("True")
        
     values_dump=sorted(value_assigner.values(), key=operator.itemgetter(1), reverse=False) 
  return values_dump     
def boundary_case(xsd_path):
    boundary_dict={}  
    for i in open(xsd_path,"r+"):
        if re.search(r'<element name=(.*)(\s)type=(.*)>',i):
             boundary_dict[re.sub(r'type|\'|"+','',i.split("=")[1]).strip()]=re.sub(r'>|\r\n|\'|"+','',i.split("=")[-1])#.strip(">").strip("\r\n").strip('"').strip().strip('"').strip(">").strip("'")
        elif re.search(r'<element name=(.*)>',i):
            interim_value=i.split("=")[1].strip("type").strip('"').strip("\r\n").strip(">").strip('"').strip()
            boundary_dict[interim_value]=re.sub(r"u",'',str(type_not_present(xsd_path,interim_value)))#.strip("u'")
        else:
            continue
    return boundary_dict      
def index_maintain(xsd_path):
         cmd23="cat %s|grep -i 'element name='"%xsd_path
         status,output=commands.getstatusoutput(cmd23)
         index_maintainer={}
         for i in output.split("\r\n"):
                 index_maintainer[re.sub(r'type|\'|"+|>','',i.split("=")[1]).strip()]=output.split("\r\n").index(i)+1
         return index_maintainer
def extracter(lok_up,file_path67,value):
    file=open(file_path67,"r+")

    for i in file:
       
       if ("element name" in i) and (value in i) and (len(i.strip("\n").split())==3):
         
             temp_value=i.strip("\n").split()[2].split("=")[1].strip(">")  
             if re.search(r'%s:(\w)'%lok_up,temp_value):
               
                 value12=temp_value.split(":")[1].strip('"')
               
                 get_valu1=special_handling(file_path67,value12)
             else:
                 get_valu1=temp_value           
             break
    
       elif ("element name" in i) and (value in i) and (len(i.strip("\n").split())==2):
           get_valu1=type_not_present(file_path67,value)
           #get_valu1="x"
           break
       else:
       
          get_valu1="z"
    return re.sub(r'"|\'|ipdr:','',get_valu1)
def type_not_present(file_path,value_searched):
    xmldoc=minidom.parse(file_path)
    typecast=xmldoc.getElementsByTagName("element")
    for i in typecast:
      if i.getAttribute("name")==value_searched:
       finaldatatype=i.getElementsByTagName("simpleType")
       for y in finaldatatype:
         vaulue=y.getElementsByTagName("restriction")
         for p in vaulue:
          x=p.getAttribute("base")
    return x.strip("u'")
def special_handling(file_path123,value_searched123):
    xmldoc=minidom.parse(file_path123)
    final_special_datatype=xmldoc.getElementsByTagName("simpleType")

    for i in final_special_datatype:
        if i.getAttribute("name")==value_searched123:
         typecast_special=i.getElementsByTagName("restriction")
         for p in typecast_special:
          x=p.getAttribute("base")

    return x.strip("u'")
    


if __name__=="__main__" :        
 file_x="/Users/shubham.mishra/desktop/Workbook5.csv"
 file_y="/Users/shubham.mishra/desktop/Workbook6.csv"
 xsd_path1="/Users/shubham.mishra/desktop/DOCSIS-CMTS-CM-DS-OFDM-PROFILE-STATUS-TYPE_3.5.1-B.1.xsd" 
 path_for_reference_xsd1="/Users/shubham.mishra/desktop/docis/DOCSIS"
 getter(file_x,file_y,path_for_reference_xsd1,xsd_path1)
 list_oo=assigner(file_x,file_y,path_for_reference_xsd1,xsd_path1)

 for i in list_oo:
     print i


 
