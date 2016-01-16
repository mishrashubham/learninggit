'''
Created on 12-Jan-2016

@author: shubham.mishra
'''
import os
import socket
import pickle
import commands
import time
import glob
from optparse import OptionParser

parser = OptionParser()



parser.add_option("--i", dest="ip",
                  help="Destination ips")
(options, args) = parser.parse_args()
os.system("mkdir -p /data/comparison/")
#master_collector,standby_collector,master_atlas,standby_atlas,master_rge=options.ip.split(",")
#for i in options.ip.split(","):
    #print i
    #os.system( "cat mover.py|ssh root@%s python -"%i)
def compare(a,b):
         p=0
         file1=pickle.load(open("/data/comparison/IB%s.txt"%a,"rb"))
         file2=pickle.load(open("/data/comparison/IB%s.txt"%b,"rb"))
         if len(file1.keys())==len(file2.keys()):
           for i in file1.keys():
               if i in file2.keys():
                      if file1[i]==file2[i]:
                        p=0
                      else:
                          f.write(" for  %s md5sum is not same in both machine\n"%i)
               else:
                   f.write(" %s is not present %s\n"%(i,b))
                   p=1
           if p==0:
                 f.write(" md5sum of all ibs  present on  both machine is same\n")
         else:
                diff=list(set(file1.keys())-set(file2.keys()))
                if len(diff)==0:
                     diff1=list(set(file2.keys())-set(file1.keys()))
               
                     for i in diff1:
                          f.write(" %s is not present in %s but present in %s\n"%(i,a,b))
                else:
                    for i in diff:
                          f.write(" %s is not present in %s but present in %s\n"%(i,b,a))
def initialisation(master_collector):
       p="192.168.191.133"
       i='/opt/catalogue/atlas/'
        
       list_directories=os.listdir(i)
       d={}
       for y in list_directories:
            d[y]=os.popen("md5sum %s/%s"%(i,y)).read().split()[0]
       pickle.dump(d,open("/data/IB%simage.txt"%master_collector,"wb"))
       os.system("scp /data/IB%simage.txt root@%s:/data/comparison"%(master_collector,p))
       #os.system("rm -rf /data/IB%simage.txt"%master_collector)
def imagecomparer(master_collector):
       os.chdir("/data/comparison/")
       list1=glob.glob("IB%s*"%master_collector)
       
       f.write("checking md5sum for %s and %s\n"%(list1[0][2:len(list1[0])-4],list1[1][2:len(list1[1])-4]))
       compare(list1[0][2:len(list1[0])-4],list1[1][2:len(list1[1])-4])
       
      
if __name__=="__main__":
                     status_file='/data/comparison/status.txt'
                     os.system("touch %s"%status_file)
                     f=open("/data/comparison/status.txt","w+")
                     master_collector,standby_collector,master_atlas,standby_atlas,master_rge=options.ip.split(",")
                     for i in options.ip.split(","):
                            print "calculating md5 of all ibs for  %s"%i
                            command="cat mover.py|ssh root@%s python -"%i
                            status,output=commands.getstatusoutput(command)
                     ipcombination_list=[(master_collector,master_atlas),(master_atlas,master_rge),(master_collector,standby_collector)]
                     print "calculating md5 of all ibs for image"
                     initialisation(master_collector)
                     imagecomparer(master_collector)
                     for m,v in ipcombination_list:
                       f.write("checking md5sum for %s and %s\n"%(m,v))
                       compare(m,v)
                     rubix_list=[master_atlas,standby_atlas,master_rge]
                     for x in rubix_list:
                             command2="cat atlasdata.py|ssh root@%s python -"%x
                             print command2
                             status,output=commands.getstatusoutput(command2)
                     os.chdir("/data/comparison")
                     os.system("rm -rf IB*")
