import multiprocessing
import os
import commands
import time
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--config",dest="config_file_path",
                   help="the file in which you want to write the converted data")


(options, args) = parser.parse_args() 
def check(value):
      baremetal_ip=value[0]
      VM_alldetails=value[1]
      for VM_details in VM_alldetails:
       print "VM_details:",VM_details
       VM_NAME=VM_details[0:-3]
       Directory=VM_details[-3]
       User_name=VM_details[-2]
       User_password=VM_details[-1]
       vm_check_command="ovftool  vi://%s:%s@%s"%(User_name,User_password,baremetal_ip)
       print vm_check_command
       status,output=commands.getstatusoutput(vm_check_command)
       vm_name_list=output.split("\n")[1:]
       print vm_name_list
       list_of_values=[]
       VM_NAME=VM_details[0:-3]
       if VM_NAME[0] in vm_name_list:
          list_of_values.append(VM_NAME[0])
      if len(list_of_values)==0:
         return list_of_values,False
      else:
         return list_of_values,True
def backup(value):
      baremetal_ip=value[0]
      VM_details=value[1]
      VM_NAME=VM_details[0:-3]
      Directory_for_backup=VM_details[-3]
      User_name=VM_details[-2]
      User_password=VM_details[-1]
      os.system("mkdir -p %s"%Directory_for_backup)
      for i in VM_NAME:
            print "entering the backup loop for",i
            #os.chdir("/Applications/VMware OVF Tool")
            poweroffcmd="ovftool --powerOffSource --noSSLVerify vi://%s:%s@%s/%s"%(User_name,User_password,baremetal_ip,i)
            cmd="ovftool --X:connectionRetryCount=5 --X:connectionReconnectCount=5 --noSSLVerify vi://%s:%s@%s/%s %s/%s.ovf"%(User_name,User_password,baremetal_ip,i,Directory_for_backup,i)
            status2,output2=commands.getstatusoutput(poweroffcmd)
            start_time=time.time()
            print start_time
            status,output=commands.getstatusoutput(cmd)
            end_time=time.time()
            while status!=0:
             if (status!=0) and (start_time-end_time<=60):
                print output
                break
             elif (status!=0) and (start_time-end_time>=1500):
                print output
                print "retrying" 
                os.system("rm -rf %s/%s*"%(Directory_for_backup,i))              
                status,output=commands.getstatusoutput(cmd)
             elif status!=0 and ("Progress:" in output ):
               print output
               os.system("rm -rf %s/%s*"%(Directory_for_backup,i))
               status,output=commands.getstatusoutput(cmd)
          
             elif status!=0:
               print status,output
               os.system("rm -rf %s/%s*"%(Directory_for_backup,i))
               break
            else:
               print output
             
def restore(value):
     #os.chdir("/Applications/VMware OVF Tool")
     baremetal_ip=value[0]
     VM_alldetails=value[1]
     #os.chdir("/Applications/VMware OVF Tool")
     same_name_list,x=check(value)
     if x:
         print same_name_list
         exit()
     else:

      for VM_details in VM_alldetails:
       print "VM_details:",VM_details
       VM_NAME=VM_details[0:-3]
       Directory=VM_details[-3]
       User_name=VM_details[-2]
       User_password=VM_details[-1]
            
        
       cmd="ovftool --name=%s -dm=thin --X:connectionRetryCount=5 --X:connectionReconnectCount=5 -ds=datastore1 %s/%s.ovf vi://%s:%s@%s"%(VM_NAME[0],Directory,VM_NAME[1],User_name,User_password,baremetal_ip)
       status,output=commands.getstatusoutput(cmd)
       print "inside restore loop"
       while status!=0:
          if status!=0 and "Invalid target datastore specified" in output:
            database=output.split("\n")[-2].strip()
            print database,"database modified"
            cmd1="ovftool --name=%s -dm=thin --X:connectionRetryCount=5 --X:connectionReconnectCount=5 -ds=%s %s/%s.ovf vi://%s:%s@%s"%(VM_NAME[0],database,Directory,VM_NAME[1],User_name,User_password,baremetal_ip)
            print "second",cmd1
            status,output=commands.getstatusoutput(cmd1)
            print output
          elif status!=0 and "The task was canceled by a user" in output:
           file_path="%s/%s.ovf"%(Directory,VM_NAME[1])
           os.system("sed -i 's/cdrom.iso/cdrom.atapi/g' file_path")
           comnd="mv %s/%s.mf %s/%s.mf_1"%(Directory,VM_NAME[1],Directory,VM_NAME[1])
           os.system(comnd)
           print "third:",cmd1
           status,output=commands.getstatusoutput(cmd1)  
          elif ("Bus error" in output) or ("Progress:" in output ):
            status,output=commands.getstatusoutput(cmd1)
          else:
           print "this error was not handled and error observed is :",output
           break
       else:
         poweroncmd="ovftool --powerOn --noSSLVerify vi://%s:%s@%s/%s"%(User_name,User_password,baremetal_ip,VM_NAME[0])
         status2,output2=commands.getstatusoutput(poweroncmd)
         print output

if __name__=="__main__":
 file1=options.config_file_path
 def pasre(file1):
       d_backup=dict()
       d_restore=dict()
       for i in open("%s"%file1,"r+"):
        if ("Baremetal_backup_details" in i) and (i.strip("\n").split(":")[1]!=''):
         baremetal_backup=i.strip("\n").split(":")[1]
         baremetalip_backup=baremetal_backup.split(",")[0]
         d_backup[baremetalip_backup]=baremetal_backup.split(",")[1:]
      
        elif ("Baremetal_restore_details" in i) and (i.strip("\n").split(":")[1]!=''):
         baremetal_restore=i.strip("\n").split(":")[1]
         baremetalip_restore=baremetal_restore.split(",")[0]
         if baremetalip_restore in d_restore:
                d_restore[baremetalip_restore].append(baremetal_restore.split(",")[1:])
         else:
              d_restore[baremetalip_restore]=list()
              d_restore[baremetalip_restore].append(baremetal_restore.split(",")[1:])
           
        elif "Type" in i:
             print "parser",i
             type=i.strip("\n").split(":")[1]
       return type.strip(),d_backup.items(),d_restore.items() 
 operation_type,Dataset_backup,Dataset_restore=pasre(file1)
 print "Dataset_backup:",Dataset_backup
 print "Dataset_restore:",Dataset_restore
 print operation_type 
 NO_of_backup_Process=len(Dataset_backup)
 NO_of_restore_Process=len(Dataset_restore)
 if NO_of_backup_Process!=0:
  process1=["p"+str(i) for i in range(NO_of_backup_Process)]
 if NO_of_restore_Process!=0:
   process2=["p"+str(i) for i in range(NO_of_restore_Process)]
   process3=["p"+str(i) for i in range(NO_of_restore_Process)]
 if operation_type=="Backup":
     for i in range (0,NO_of_backup_Process):
       process1[i]=multiprocessing.Process(target=backup, args=(Dataset_backup[i],))
       process1[i].start()
 elif operation_type=="Restore":
        
        for i in range (0,NO_of_restore_Process):
         process2[i]=multiprocessing.Process(target=restore, args=(Dataset_restore[i],))
         process2[i].start()
 elif operation_type=="Both":
     for i in range (0,NO_of_backup_Process):
       process1[i]=multiprocessing.Process(target=backup, args=(Dataset_backup[i],))
       process1[i].start()      
     for i in range (0,NO_of_restore_Process):
         process2[i]=multiprocessing.Process(target=restore, args=(Dataset_restore[i],))
         process2[i].start()
 else:
     print "wrong parameters given"
     exit()
