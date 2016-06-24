'''
Created on 12-Jan-2016

@author: shubham.mishra
'''
import  os
import socket
import pickle
k=['/data/ib/inbox']
def mover():
     p='192.168.191.133'
     for i in k:
       os.chdir(i)
       list_directories=os.listdir(i)
       d={}
       for y in list_directories:
            d[y]=os.popen("md5sum %s"%y).read().split()[0]   
       pickle.dump(d,open("/data/IB%s.txt"%socket.getfqdn(),"wb"))
       os.system("scp /data/IB%s.txt root@%s:/data/comparison"%(socket.getfqdn(),p))
       os.system("rm -rf /data/IB%s.txt"%socket.getfqdn())
mover()
