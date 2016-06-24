'''
Created on 08-Apr-2016

@author: shubham.mishra
'''
import xsd_lookup
import type_template_mapping
import os
import re


def value_extracter(path_for_reference_xsd,xsd_path):
    
    directory_list=os.listdir("%s"%path_for_reference_xsd)
    values=xsd_lookup.parent_and_type_extracter(xsd_path)
    
    xyz={}

    for i in values.keys():
        xyz[i]=list()
        #print i
        for y in directory_list:
           
           temp_value=re.search(r'%s_(\d)'%i,y)
           #print temp_value
           if temp_value:
               xyz[i].append(y)
    #print xyz 
    return xyz



def selector(path_for_reference_xsd,xsd_path):
    
    dict_list=value_extracter(path_for_reference_xsd,xsd_path)
    #print dict_list
    final_dict={}
    for i in dict_list:
        if len(dict_list[i])<=1:
            
            final_dict[i]=str(dict_list[i]).strip("[").strip("]").strip("'")
        else:
           k=[y.split("_")[1].split("-")[0] for y in dict_list[i]] 
           if len(set(k))>1:
               p=sorted(k)[-1]
               get_best_value=k.index(p)
               final_dict[i]=dict_list[i][get_best_value]
           else:
              templist=[y.split("_")[1].split("-")[1].split(".xsd")[0] for y in dict_list[i]]
              index=templist.index(max(templist))
              final_dict[i]=str(dict_list[i][index])
    #print final_dict
    return final_dict
       


if __name__=="__main__":
    path_for_reference_xsd="/Users/shubham.mishra/desktop/docis/DOCSIS"
    xsd_path1="/Users/shubham.mishra/desktop/DOCSIS-CMTS-CM-DS-OFDM-PROFILE-STATUS-TYPE_3.5.1-B.1.xsd"
    value_extracter(path_for_reference_xsd,xsd_path1)
    selector(path_for_reference_xsd,xsd_path1)
    
        
    
    
    