'''
Created on 12-Jan-2016

@author: shubham.mishra
'''
import os
def atlascheck():
    k=["dcRegion.id.map","device_edc.id.map"]
    d={}
    d2={}
    p=0
    f=open("/data/atlas_check.txt","w+")
    os.chdir("/data/ib/inbox")
    for i in k:
       d[i]=os.popen("md5sum %s"%i).read().split()[0]
    os.chdir("/data/atlasdata")
    for y in k:
       d2[y]=os.popen("md5sum %s"%y).read().split()[0] 
    for i in k:
         if d[i]==d2[i]:
            p=0
         else:
             f.write("%s is not some in atlasdata and inbox\n"%i)
             p=1
    if p==0:
         f.write("all ibs are  some in atlasdata and inbox\n")
    os.system("scp %s root@%s:/data/comparison"%('/data/atlas_check.txt','192.168.191.133'))
atlascheck()
