'''
Created on 08-Apr-2016

@author: shubham.mishra
'''
def csv_mapping_for_dat_type(file1,file2):
    
    dat_type_mapping=dict()
    service_type_mapping=dict()
    
    for i in open(file1,"rU"):
    
          if "DataType"   in i.split(",")[0].strip("\r").strip():
            continue
          else:
             dat_type_mapping[i.split(",")[0].strip()]=i.split(",")[1].strip().strip("\n").strip("\r")
    
    for y in open(file2,"rU"):
        
        if "TemplateId" in y.split(",")[2].strip("\r").strip():
            continue
        else:
            service_type_mapping[y.split(",")[0].strip()]=y.split(",")[2].strip().strip("\n").strip("\r")
    return dat_type_mapping,service_type_mapping

if __name__=="__main__":
    file_x="/Users/shubham.mishra/desktop/datatype_mapping.csv"
    file_y="/Users/shubham.mishra/desktop/template_mapping.csv"   
    data_tye,service_type=csv_mapping_for_dat_type(file_x,file_y)
    print data_tye
    print service_type