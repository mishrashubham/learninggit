import os
import shutil
import time
import glob
import errno
import commands
from subprocess import call

def getextensions(m):
 for i in os.listdir(m):
      p=os.path.splitext(i)
      if  p[1]:
         if p[1] not in l:
            k='*'+p[1]
            l.append(k)
def getallfiles():
 for i in l:
     p=glob.glob(i)
     k=i.strip('*.')
     d[k]=p
def makedirectories(m):
 for i in d.keys():
  try:
      if len(d[i])!=0:  
          os.mkdir('%s/%s'%(m,i))
  except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir('%s/%s'%(m,i)):
            pass
def movefiles(m):
 for i in d:
   for y in d[i]:
       try :
            shutil.move(y,'%s/%s'%(m,i))
            
       except shutil.Error:
           p=raw_input("you want to replace the existing file:(y/n):")
           if p=='n':
                t= y.strip("%s"%i).strip(".")
                call(["mv","%s"%y,"%s/%s/%s_copy"%(m,i,t)])
           else :
                 
                 call(["rm","-f","%s/%s/%s"%(m,i,y)])
                 shutil.move(y,'%s/%s'%(m,i))


if __name__=='__main__':
   p=raw_input("enter the directory in which  want to rearrange:")
   os.chdir(p)
   l=[]
   d={}
   getextensions(p)
   getallfiles()
   makedirectories(p)
   movefiles(p)
   print "Directories for every format has been created and files are moved are moved in respective directory"
