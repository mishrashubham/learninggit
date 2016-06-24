#Command to use script:

   python backup_restore.py --config vmbackuprestoreconfig.txt


#Parametes used in config.txt

1.)Type:Use "Backup" when you want to backup the vm and "Restore" if you want to restore the vm

2.)Baremetal_backup_details:<baremetal_ip>,<VM_names>,<directory in which you want to take backuo>,<username>,<password>
      Note:<VM_names> value can be repeated 
3.)Baremetal_restore_details=<baremetal_ip>,<name of the new vm>,<name of the old vm>,<directory in which backup is restored>,<username>,<password>
4.)If you want both restore and backup to run simultaneuosly ,pass "both" against "Type" parameter  


#Note:
Make sure that VM_names which are restored and VM's which are present on baremetal should be different else for the VM_names given or script will fail  
