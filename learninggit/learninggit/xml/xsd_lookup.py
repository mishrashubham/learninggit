'''
Created on 08-Apr-2016

@author: shubham.mishra
'''
import commands



def xsd_ref_value_extracter(xsd_path):
    
    cmd="cat %s|grep -i 'element ref='"%xsd_path
    status,output=commands.getstatusoutput(cmd)
    list_of_ref_value=[]
    #print output
    for i in output.split("\r\n"):
        print i 
        list_of_ref_value.append(i.split("=")[1].strip("/>\r").strip('"').strip('"'))
    return list_of_ref_value



def parent_and_type_extracter(xsd_path):
    
    fields=xsd_ref_value_extracter(xsd_path)
    field_specification={}
    
    for i in fields:
        if i.split(":")[0] in field_specification:
            field_specification[i.split(":")[0]].append(i.split(":")[1])
        else:
            field_specification[i.split(":")[0]]=list()
            field_specification[i.split(":")[0]].append(i.split(":")[1])
            
    return field_specification
def field_index(xsd_path):
    fields12=xsd_ref_value_extracter(xsd_path)
    field_index1=[]
    for i in fields12:
        field_index1.append(i.split(":")[1])
    return field_index1


if __name__=="__main__":

 xsd_path1="/Users/shubham.mishra/desktop/DOCSIS-CMTS-CM-DS-OFDM-PROFILE-STATUS-TYPE_3.5.1-B.1.xsd"
 final=parent_and_type_extracter(xsd_path1)
 m=field_index(xsd_path1)
 print final
 print m
    
    
    
