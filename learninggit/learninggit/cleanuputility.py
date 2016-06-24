import os
import commands
def cleanup():
      decision='y'
      while(decision=='y'):
        p=raw_input("enter the next director you wanna clean:")
        status,output=commands.getstatusoutput("find %s -type f -size 0 > %s/cleanup.txt"%(p,p))
        for i in open("%s/cleanup.txt"%p,"r+"):
          os.system("rm -rf %s"%i)
          #call(["rm","-rf",i])
        decision=raw_input("you want to continue with cleaning process(y/n):")
if __name__=='__main__':
       cleanup()
