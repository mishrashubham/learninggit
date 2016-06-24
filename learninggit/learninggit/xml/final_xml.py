'''
Created on 10-Apr-2016

@author: shubham.mishra
'''
import value_extacter
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as Etree
import type_template_mapping
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--config",dest="config_file_path",
                   help="the file in which you want to write the converted data")
(options, args) = parser.parse_args() 

def test(file1,file2,path_for_reference_xsd, xsd_path):
    k=value_extacter.assigner(file1, file2, path_for_reference_xsd, xsd_path)
    m,y=type_template_mapping.csv_mapping_for_dat_type(file1, file2)
    template_string_value=xsd_path.split("/")[-1].split("_")[0]
    last_value=xsd_path.split("/")[-1]
    if template_string_value in y:
         template_numric_value=y[template_string_value]
    #for i in k:
        
    return k,template_numric_value,template_string_value,last_value
def creating_xml(file1,file2,path_for_reference_xsd, xsd_path,schema_url,outputfile):
    value_list,template_id,templatestring,last_value1=test(file1,file2,path_for_reference_xsd, xsd_path)
    root=Element("template")
    
    p=templatestring.split("-",1)[1]
    tree=ElementTree(root)
    root.set("xsi:schemaLocation","https://appliedbroadband.com/ipdr/template_block template_block.xsd")
    root.set("xmlns","https://appliedbroadband.com/ipdr/template_block")
    root.set("xmlns:xsi","http://www.w3.org/2001/XMLSchema-instance")
    templateId=Element("templateId")
    schemaName=Element("schemaName")
    typeName=Element("typeName")
    root.append(templateId)
    root.append(schemaName)
    root.append(typeName)
    templateId.text=str(template_id)
    schemaName.text=str(schema_url)+str(last_value1)
    typeName.text=str(templatestring)+":"+str(templatestring.split("-",1)[1])
    for i in value_list:
        field=Element("field")
        root.append(field)
        typeId=Element("typeId")
        fieldId=Element("fieldId")
        fieldName=Element("fieldName")
        isEnabled=Element("isEnabled")
        field.append(typeId)
        field.append(fieldId)
        field.append(fieldName)
        field.append(isEnabled)
        typeId.text=str(i[0])
        fieldId.text=str(i[1])
        fieldName.text=str(i[2])
        isEnabled.text=str(i[3])
    print Etree.tostring(root)
    tree.write(open(r'%s'%outputfile,"w+"))   
        
    

    
    
if __name__=="__main__":
 file1=options.config_file_path
 def parser(file):
     for i in open(file,"r+"):
         interim_i=i.strip("\n").split(":")[0]
         #interim_value=i.strip("\n").split(":")[1]
         if "XSD_LOCATION" in i:
             XSD_LOCATION=i.strip("\n").split(":")[1].strip()
         elif "REFERENCE_LOCATION_FOR_XSD" in i:
              REFERENCE_XSD_LOCATION1=i.strip("\n").split(":")[1].strip()
         elif "SCHEMA_URL" in i:
             interim_shema_url=i.strip("\n").split(":",1)[1].strip()
         elif "OUTPUT_XML_PATH" in i:
                 OUTPUT_XML_PATH=i.strip("\n").split(":")[1].strip()
         else:
              exit()
     return XSD_LOCATION,REFERENCE_XSD_LOCATION1,interim_shema_url,OUTPUT_XML_PATH
 
 xsd_path1,path_for_reference_xsd1,schema_url,outputfile=parser(file1) 
 file_x="datatype_mapping.csv"
 file_y="template_mapping.csv"    
 #file_x="/Users/shubham.mishra/desktop/Workbook5.csv"
 #file_y="/Users/shubham.mishra/desktop/Workbook6.csv"
 #xsd_path1="/Users/shubham.mishra/desktop/DOCSIS-CMTS-CM-DS-OFDM-PROFILE-STATUS-TYPE_3.5.1-B.1.xsd" 
 #path_for_reference_xsd1="/Users/shubham.mishra/desktop/docis/DOCSIS"
 creating_xml(file_x,file_y,path_for_reference_xsd1,xsd_path1,schema_url,outputfile)
