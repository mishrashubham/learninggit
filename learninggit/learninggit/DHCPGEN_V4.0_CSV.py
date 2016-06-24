import time
import sys
import socket
import netaddr
import random
import array
import csv
import copy
from optparse import OptionParser


parser = OptionParser()



parser.add_option("--port", dest="port",
                  help="Destination Server Port")

parser.add_option("--ip", dest="ip",
                  help="Server Ip")


parser.add_option("--EndTime",
                  dest="EndTime",
                  default="2015-08-10-13",
                  help="Time til the packets would be send (Default = 2015-08-10-13)")

parser.add_option("--subn", dest="subn",
                  help="Total number of Subscribers")

parser.add_option("--CsvFile", dest="csvfile",
                  default="/data/pawan/DHCP_DATA.csv",
                  help="Input CSV File.")

parser.add_option("--Relay_Agent", dest="relayAgent",
                  default="Yes",
                  help="For enabling Relay Aggent Field(Yes/No).")

parser.add_option("--Fixed_Fields", dest="fixedFields",
                  default="Yes",
                  help="For enabling mandatory fields (Yes/No).")

(options, args) = parser.parse_args()

Addr_Dict={'CIADDR':['0x00','0x00','0x00','0x00'],\
           'YIADDR':'192.168.193.1',\
           'SIADDR':'192.168.193.6',\
           'GIADDR':['0x00','0x00','0x00','0x00'],\
           'CHADDR':'58:98:35:6a:1c:1a',\
	   'Sname':['0x00']*64,\
	   'File':['0x00']*128,\
           'Magic Cookie':'99.130.83.99'}

Option_Dict={'53':{'Length':1,'Value':5},\
             '01':{'Length':4,'Value':'255.255.0.0'},\
             '03':{'Length':4,'Value':'101.185.242.254'},\
             '06':{'Length':4,'Value':'61.9.226.1'},\
             '51':{'Length':4,'Value':14400},\
             '54':{'Length':4,'Value':'172.56.18.216'},\
             '58':{'Length':4,'Value':7200},\
             '59':{'Length':4,'Value':10800},\
             '255':{'Length':0,'Value':None}}
if options.relayAgent.upper()=="YES":
	Field_formt=['CIADDR','YIADDR','SIADDR','GIADDR','CHADDR','Sname','File','Magic Cookie','53','01','03','06','51','54','58','59','82','255']
else:
	Field_formt=['CIADDR','YIADDR','SIADDR','GIADDR','CHADDR','Sname','File','Magic Cookie','53','01','03','06','51','54','58','59','255']
#Default Value of Relay Agent Information is with option 1 having Agent circuit Id as AVC00000911593
Relay_agent_dict={'82':{'Length':'17','Value':['0x01','0x0f','0x41','0x56','0x43','0x30','0x30','0x30','0x30','0x30','0x39','0x31','0x31','0x35','0x39','0x39','0x33']}}

Relay_packet_dict={"CABLE":[1,2,9],"DSL":[1,2],"NBN":[1]}

Option_relay_mapping={1:'Agent Circuit Id',2:'Agent Remote Id',9:'Vender Info'}

fixed_part=['0x02','0x01','0x06','0x00','0x70','0x00','0x89','0x45','0x00','0x10','0x00','0x00']
'''
Bootp_Dict={'OP':['0x02'],\
            'HTYPE':[['0x01'],['0x02'],['0x04'],['0x03'],['0x05']],\
            'HLEN':[['0x06'],['0x07'],['0x08'],['0x09'],['0x10']],\
            'HOPES':['0x00'],\
            'XID':['0x70','0x00','0x89','0x45'],\
            'SECS':['0x00','0x10'],\
            'FLAGS':[['0x00','0x00'],['0x80','0x00']]}
Bootp_format=['OP','HTYPE','HLEN','HOPES','XID','SECS','FLAGS']
'''
Bootp_Dict={'OP':['0x02'],\
	    'HTYPE':[['0x01'],['0x02'],['0x04'],['0x03'],['0x05']],\
	    'HLEN':[['0x06'],['0x07'],['0x08'],['0x09'],['0x10']],\
	    'HOPES':['0x00'],\
	    'XID':['0x70','0x00','0x89','0x45'],\
	    'SECS':['0x00','0x10'],\
	    'FLAGS':[['0x00','0x00'],['0x80','0x00']]}
Bootp_format=['OP','HTYPE','HLEN','HOPES','XID','SECS','FLAGS']

Drop_format=Bootp_format+['CIADDR','YIADDR','SIADDR','GIADDR','CHADDR','Sname','File','Magic Cookie']
class FileParser():
    def __init__(self,csv_file_name):
	self.csv_file_name=csv_file_name
        self.mac_list,self.cable_circuit_id_list,self.dsl_circuit_id_list,self.dsl_remote_id_list,self.nbn_circuit_id_list,self.CIADDR_list,self.YIADDR_list,self.SIADDR_list,self.GIADDR_list=list(),list(),list(),list(),list(),list(),list(),list(),list()
        
    
    def getList(self,file_name,list_name):
        try:
            f=open(file_name,'r')
        except IOError as ex:
            print "Error in opening the %s file is %s" %(file_name,ex)
            sys.exit()
        for line in f:
            list_name.append(line.strip())
    #File Format:
    #CIADDR,YIADDR,SIADDR,GIADDR,CHADDR,CABLE_CIRCUIT_ID,DSL_CIRCUIT_ID,DSL_REMOTE_ID,NBN_CIRCUIT_ID

    def getListFromCSV(self,file_name):
	try:
            f=open(file_name,'rU')
        except IOError as ex:
            print "Error in opening the %s file is %s" %(file_name,ex)
            sys.exit()
	lines =csv.reader(f,dialect=csv.excel_tab)
	for row in lines:
		if row[-1].startswith("#"):
			pass
		else:
   			self.CIADDR_list.append(row[-1].split(",")[0])
			self.YIADDR_list.append(row[-1].split(",")[1])
			self.SIADDR_list.append(row[-1].split(",")[2])
			self.GIADDR_list.append(row[-1].split(",")[3])
			self.mac_list.append(row[-1].split(",")[4])
			self.cable_circuit_id_list.append(row[-1].split(",")[5])
			self.dsl_circuit_id_list.append(row[-1].split(",")[6])
			self.dsl_remote_id_list.append(row[-1].split(",")[7])
			self.nbn_circuit_id_list.append(row[-1].split(",")[8])
		
    def main_parser(self):
	'''
        #Getting Mac_address
        self.getList(self.mac_file, self.mac_list)
        #Getting Cable Circuit Id
        self.getList(self.cable_circuit_id_file, self.cable_circuit_id_list)
        #Getting ASP-DSL Circuit Id
        self.getList(self.dsl_circuit_id_file, self.dsl_circuit_id_list)
        #Getting ASP-DSL Remote ID
        self.getList(self.dsl_remote_id_file, self.dsl_remote_id_list)
        #Getting NBN Circuit ID
        self.getList(self.nbn_circuit_id_file, self.nbn_circuit_id_list)
	'''
	self.getListFromCSV(self.csv_file_name)
	#print self.CIADDR_list
	#print self.YIADDR_list
        

class DHCPGEN(FileParser):
    def __init__(self,server_host,server_port,tot_sub,csv_file_name):
        FileParser.__init__(self, csv_file_name)
        self.server_host,self.server_port=server_host,int(server_port)
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.ip_start=netaddr.IPAddress(start_ip)
        self.tot_sub=int(tot_sub)
        self.cable_vendar_spec=[['0x09','0x0b','0x00','0x00','0x11','0x8b','0x06','0x01','0x40','0x01','0x02','0x03','0x00'],['0x09','0x0b','0x00','0x00','0x11','0x8b','0x06','0x01','0x40','0x01','0x02','0x02','0x00'],['0x09','0x0b','0x00','0x00','0x11','0x8b','0x06','0x01','0x40','0x01','0x02','0x01','0x00']]
        self.total_counter=0
	self.main_parser()
 
    def getStringToHex(self,strr):
        return (["0x%02X" % (ord(x)) for x in strr])
        
    def getIptoHex(self,ip):
        hex_ip_bytes=["0x"+hex(int(value)).lstrip("0x").zfill(2).upper() for value in ip.split(".")]
        return hex_ip_bytes

    def splitIntwo(self,byte):
	return ['0x'+ byte[i:i+2] for i in range(0,len(byte),2)]
		
    
    def getIntTopaddingHex(self,value,Len=0):
	if value:
            if Len:
                hex_val=hex(value).lstrip('0x').upper()
                return self.splitIntwo(hex_val.zfill(Len))
            else:
                hex_val=hex(value).lstrip('0x').upper()
                return self.splitIntwo(hex_val.zfill(((len(hex_val)/2)+len(hex_val)%2)*2))
	else:
		return ['0x00']
    
    def getmacToHex(self,mac_add):
        return ['0x'+val.upper().zfill(2) for val in mac_add.split(":")]
    
    def getLeaseTime(self,value):
	if not value%4:
		return 200
	elif value%4==1:
		return 800
	elif value%4==2:
		return 1200
	else:
		return 14400

    def getBootpPacket(self,format_list):
	temp_packet=list()
	for key in format_list:
		if Bootp_Dict.has_key(key):
			if key in ['HTYPE','HLEN','FLAGS']:
				temp_packet+=random.choice(Bootp_Dict[key])
				print temp_packet,key
			elif key =='XID':
				temp_packet+=self.getIntTopaddingHex(random.randrange(0,4294967295),8)
			elif key=='SECS':
				temp_packet+=self.getIntTopaddingHex(65535,4)
			elif key=='HOPES':
				temp_packet+=self.getIntTopaddingHex(255,2)
			else:
				print Bootp_Dict[key],key
				temp_packet+=Bootp_Dict[key]
		else:
			pass
	#print "BOOT PACKET %s" %(str(temp_packet))
	return temp_packet

    def getRelayPacket(self,packet_type,index):
        relay_packet=list()
        sub_packet=list()
        for key in Relay_packet_dict.keys():
            if key==packet_type:
                for value in Relay_packet_dict[key]:
                    if Option_relay_mapping.has_key(value):
                        if Option_relay_mapping[value]=='Agent Circuit Id':
                            if packet_type=="CABLE":
                                hex_value=self.getStringToHex(self.cable_circuit_id_list[index])
				print "Cable_circuit_id %s" %(str(hex_value))
                                sub_packet+=self.getIntTopaddingHex(value,2)+self.getIntTopaddingHex(len(hex_value))+hex_value
				print "Cable_circuit_id_complete packet %s" %(str(self.getIntTopaddingHex(value,2)+self.getIntTopaddingHex(len(hex_value))+hex_value))
                            elif packet_type=="DSL":
                                hex_value=self.getStringToHex(self.dsl_circuit_id_list[index])
				print "DSL_circuit_id %s" %(str(hex_value))
                                sub_packet+=self.getIntTopaddingHex(value,2)+self.getIntTopaddingHex(len(hex_value))+hex_value
				print "DSL_circuit_id_complete packet %s" %(str(self.getIntTopaddingHex(value,2)+self.getIntTopaddingHex(len(hex_value))+hex_value))
                            elif packet_type=="NBN":
                                hex_value=self.getStringToHex(self.nbn_circuit_id_list[index])
				print "NBN_circuit_id %s" %(str(hex_value))
                                sub_packet+=self.getIntTopaddingHex(value,2)+self.getIntTopaddingHex(len(hex_value))+hex_value
				print "NBN_circuit_id_complete packet %s" %(str(self.getIntTopaddingHex(value,2)+self.getIntTopaddingHex(len(hex_value))+hex_value))
                            else:
                                pass
                        elif Option_relay_mapping[value]=='Agent Remote Id':
                            if packet_type=="CABLE":
				if self.mac_list[index]:
                                	hex_value=self.getStringToHex(self.cable_circuit_id_list[index])
					#hex_value=self.getmacToHex(self.mac_list[index])
					print "Cable Remote_circuit_id %s" %(str(hex_value))
                               		sub_packet+=self.getIntTopaddingHex(value,2)+self.getIntTopaddingHex(len(hex_value))+hex_value
					print "Cable_Remote_id_complete packet %s" %(str(self.getIntTopaddingHex(value,2)+self.getIntTopaddingHex(len(hex_value))+hex_value))
				else:
					hex_value=self.getStringToHex(self.mac_list[index])
					sub_packet+=self.getIntTopaddingHex(value,2)+self.getIntTopaddingHex(len(hex_value))+hex_value
                            elif packet_type=="DSL":
                                hex_value=self.getStringToHex(self.dsl_remote_id_list[index])
                                sub_packet+=self.getIntTopaddingHex(value,2)+self.getIntTopaddingHex(len(hex_value))+hex_value
				print "DSL Remote_circuit_id %s" %(str(hex_value))
				print "DSL_Remote_id_complete packet %s" %(str(self.getIntTopaddingHex(value,2)+self.getIntTopaddingHex(len(hex_value))+hex_value))
                            else:
                                pass
                        elif Option_relay_mapping[value]=='Vender Info':
                            if packet_type=="CABLE":
                                hex_value=random.choice(self.cable_vendar_spec)
                                sub_packet+=hex_value
				print "Cable_vender %s" %(str(hex_value))
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
            else:
                pass
            
        relay_packet=self.getIntTopaddingHex(int(Relay_agent_dict.keys()[-1]),2)+ self.getIntTopaddingHex(len(sub_packet))+sub_packet
	#print "Complete Relay_packet %s" %(str(relay_packet))
        return relay_packet
                       
                
    
    def main(self):
        #Creating Data Dictionaries
        #self.main_parser()
        print " Inside subroutine"
#Field_formt=['CIADDR','YIADDR','SIADDR','GIADDR','CHADDR','Sname','File','Magic Cookie','53','01','03','06','51','54','58','59','82','255']
#Bootp_format=['OP','HTYPE','HLEN','HOPES','XID','SECS','FLAGS']
	self.total_counter=0

        for sub in range(self.tot_sub):
            dhcp_packet=list()
            if options.fixedFields.upper()=="YES":
                dhcp_packet+=self.getBootpPacket(Bootp_format)
                for value in Field_formt:
                    if Addr_Dict.has_key(value):
                        if value=='YIADDR':
			    dhcp_packet+=self.getIptoHex(str(netaddr.IPAddress(int(self.YIADDR_list[sub%len(self.YIADDR_list)]))))
			    #print "YIADDR %s" %(str(self.getIptoHex(str(netaddr.IPAddress(int(self.YIADDR_list[sub%len(self.YIADDR_list)]))))))
                        elif value=='SIADDR':
			    dhcp_packet+=self.getIptoHex(self.SIADDR_list[sub%len(self.SIADDR_list)])
			    print "SIADDR %s" %(str(self.getIptoHex(self.SIADDR_list[sub%len(self.SIADDR_list)])))
                        elif value=='CHADDR':
                            if len(self.mac_list)<=len(self.cable_circuit_id_list):
                                hex_value=self.getmacToHex(self.mac_list[sub%len(self.mac_list)])
                                if len(hex_value) <=16:
                                    hex_value=hex_value+['0x00']*(16-len(hex_value))
                                else:
                                    pass
                                dhcp_packet+=hex_value
                                #print "CHADDR %s" %(str(self.getmacToHex(self.mac_list[sub%len(self.mac_list)])+['0x00','0x00','0x00','0x00','0x00','0x00','0x00','0x00','0x00','0x00']))
                            else:
                                dhcp_packet+=self.getmacToHex(self.mac_list[sub%len(self.cable_circuit_id_list)])
                                #print "CHADDR %s" %(str(self.getmacToHex(self.mac_list[sub%len(self.cable_circuit_id_list)])))
                        elif value=='Magic Cookie':
                            dhcp_packet+=self.getIptoHex(Addr_Dict[value])
                            #print "Magic Cookie %s" %(str(self.getIptoHex(Addr_Dict[value])))
			elif value=='CIADDR':
			    print self.getIptoHex(self.CIADDR_list[sub%len(self.CIADDR_list)])
			    dhcp_packet+=self.getIptoHex(self.CIADDR_list[sub%len(self.CIADDR_list)])
			    #print "CIADDR %s" %(str(self.getIptoHex(self.CIADDR_list[sub%len(self.CIADDR_list)])))
			elif value=='GIADDR':
			    dhcp_packet+=self.getIptoHex(self.CIADDR_list[sub%len(self.GIADDR_list)])
			    print "GIADDR %s" %(str(self.getIptoHex(self.GIADDR_list[sub%len(self.GIADDR_list)])))
                        else:
                            dhcp_packet+=Addr_Dict[value]
                            print "%s %s " %(value,str(Addr_Dict[value]))
                    elif Option_Dict.has_key(value):
                        if value in ['01','03','06','54']:
                            dhcp_packet+=self.getIntTopaddingHex(int(value),2)+self.getIntTopaddingHex(Option_Dict[value]['Length'],2)+self.getIptoHex(Option_Dict[value]['Value'])
                            #print "%s %s" %(value,str(self.getIntTopaddingHex(int(value),2)+self.getIntTopaddingHex(Option_Dict[value]['Length'],2)+self.getIptoHex(Option_Dict[value]['Value'])))
                        elif value in ['51']:
			    #pass
			    dhcp_packet+=self.getIntTopaddingHex(int(value),2)+self.getIntTopaddingHex(0,2)
                            #dhcp_packet+=''
			    print "Lease Time %s" % (str(self.getIntTopaddingHex(int(value),2)+self.getIntTopaddingHex(0,2)))
			    '''
                            lease_value=self.getLeaseTime(sub)
                            dhcp_packet+=self.getIntTopaddingHex(int(value),2)+self.getIntTopaddingHex(Option_Dict[value]['Length'],2)+self.getIntTopaddingHex(lease_value,Option_Dict[value]['Length']*2)
			   ''' 
                        elif value in ['53','58','59','255']:
                            if Option_Dict[value]['Value']:
                                dhcp_packet+=self.getIntTopaddingHex(int(value),2)+self.getIntTopaddingHex(Option_Dict[value]['Length'],2)+self.getIntTopaddingHex(Option_Dict[value]['Value'],Option_Dict[value]['Length']*2)
                                #print "%s %s" %(value,str(self.getIntTopaddingHex(int(value),2)+self.getIntTopaddingHex(Option_Dict[value]['Length'],2)+self.getIntTopaddingHex(Option_Dict[value]['Value'],Option_Dict[value]['Length']*2)))

                            else:
                                dhcp_packet+=self.getIntTopaddingHex(int(value),2)
                                #print "%s %s" %(value,str(self.getIntTopaddingHex(int(value),2)))

                    elif Relay_agent_dict.has_key(value):
                        if value in ['82']:
                            sub_mod=sub%10
                            if sub_mod in [1,2]:
                                if self.total_counter<len(self.nbn_circuit_id_list):
                                        dhcp_packet+=self.getRelayPacket("NBN",self.total_counter)
                                        self.total_counter+=1
                                else:
                                        dhcp_packet+=self.getRelayPacket("NBN",(self.total_counter)%len(self.nbn_circuit_id_list))
                                        self.total_counter+=1
                            elif sub_mod in [3,4]:
                                if len(self.dsl_circuit_id_list)<=len(self.dsl_remote_id_list):
                                        if (self.total_counter<len(self.dsl_circuit_id_list)):
                                                dhcp_packet+=self.getRelayPacket("DSL",self.total_counter)
                                                self.total_counter+=1
                                        else:
                                                dhcp_packet+=self.getRelayPacket("DSL",self.total_counter%(len(self.dsl_circuit_id_list)))
                                                self.total_counter+=1
                                else:
                                        if (self.total_counter<len(self.dsl_remote_id_list)):
                                                dhcp_packet+=self.getRelayPacket("DSL",self.total_counter)
                                                self.total_counter+=1
                                        else:
                                                dhcp_packet+=self.getRelayPacket("DSL",self.total_counter%(len(self.dsl_remote_id_list)))
                                                self.total_counter+=1
                            else:
                                if len(self.cable_circuit_id_list)<=len(self.mac_list):
                                        if (self.total_counter<len(self.cable_circuit_id_list)):
                                                dhcp_packet+=self.getRelayPacket("CABLE",self.total_counter)
                                                self.total_counter+=1
                                        else:
                                                dhcp_packet+=self.getRelayPacket("CABLE",self.total_counter%(len(self.cable_circuit_id_list)))
                                                self.total_counter+=1
                                else:
                                        if (self.total_counter<len(self.mac_list)):
                                                dhcp_packet+=self.getRelayPacket("CABLE",self.total_counter)
                                                self.total_counter+=1
                                        else:
                                                dhcp_packet+=self.getRelayPacket("CABLE",self.total_counter%(len(self.mac_list)))
                                                self.total_counter+=1
                        else:
                            pass
                    else:
                        pass
            else:
                new_bootp_format=copy.deepcopy(Bootp_format)
                new_drop_format=copy.deepcopy(Drop_format)
                drop_sub=sub%len(Drop_format)
                if drop_sub<len(Bootp_format):
                    drop_field=new_bootp_format.pop(drop_sub)
		    print "DROPPED BOOTP field %s" %(str(drop_field))
                    dhcp_packet+=self.getBootpPacket(new_bootp_format)
                    for value in new_drop_format[len(Bootp_format):]:
                        if value=='YIADDR':
                            dhcp_packet+=self.getIptoHex(str(netaddr.IPAddress(int(self.YIADDR_list[sub%len(self.YIADDR_list)]))))
                            print "YIADDR %s" %(str(self.getIptoHex(str(netaddr.IPAddress(int(self.YIADDR_list[sub%len(self.YIADDR_list)]))))))
                        elif value=='SIADDR':
                            dhcp_packet+=self.getIptoHex(self.SIADDR_list[sub%len(self.SIADDR_list)])
                            print "SIADDR %s" %(str(self.getIptoHex(self.SIADDR_list[sub%len(self.SIADDR_list)])))
                        elif value=='CHADDR':
                            if len(self.mac_list)<=len(self.cable_circuit_id_list):
                                hex_value=self.getmacToHex(self.mac_list[sub%len(self.mac_list)])
                                if len(hex_value) <=16:
                                    hex_value=hex_value+['0x00']*(16-len(hex_value))
                                else:
                                    pass
                                dhcp_packet+=hex_value
                                print "CHADDR %s" %(str(hex_value))
                            else:
                                dhcp_packet+=self.getmacToHex(self.mac_list[sub%len(self.cable_circuit_id_list)])
                                print "CHADDR %s" %(str(self.getmacToHex(self.mac_list[sub%len(self.cable_circuit_id_list)])))
                        elif value=='Magic Cookie':
                            dhcp_packet+=self.getIptoHex(Addr_Dict[value])
                            print "Magic Cookie %s" %(str(self.getIptoHex(Addr_Dict[value])))
                        elif value=='CIADDR':
                            dhcp_packet+=self.getIptoHex(self.CIADDR_list[sub%len(self.CIADDR_list)])
                            print "CIADDR %s" %(str(self.getIptoHex(self.CIADDR_list[sub%len(self.CIADDR_list)])))
                        elif value=='GIADDR':
                            dhcp_packet+=self.getIptoHex(self.CIADDR_list[sub%len(self.GIADDR_list)])
                            print "GIADDR %s" %(str(self.getIptoHex(self.GIADDR_list[sub%len(self.GIADDR_list)])))
                        else:
                            dhcp_packet+=Addr_Dict[value]
                            print "%s %s " %(value,str(Addr_Dict[value]))
                else:
                    dhcp_packet+=self.getBootpPacket(new_bootp_format)
                    drop_field=new_drop_format.pop(drop_sub)
                    print "DROP FIeld in ATTR is %s" %(str(drop_field))
                    for value in new_drop_format[len(Bootp_format):]:
                        if value=='YIADDR':
                            dhcp_packet+=self.getIptoHex(str(netaddr.IPAddress(int(self.YIADDR_list[sub%len(self.YIADDR_list)]))))
                            print "YIADDR %s" %(str(self.getIptoHex(str(netaddr.IPAddress(int(self.YIADDR_list[sub%len(self.YIADDR_list)]))))))
                        elif value=='SIADDR':
                            dhcp_packet+=self.getIptoHex(self.SIADDR_list[sub%len(self.SIADDR_list)])
                            print "SIADDR %s" %(str(self.getIptoHex(self.SIADDR_list[sub%len(self.SIADDR_list)])))
                        elif value=='CHADDR':
                            if len(self.mac_list)<=len(self.cable_circuit_id_list):
                                if sub<len(self.mac_list):
                                    hex_value=self.getmacToHex(self.mac_list[sub])
                                else:
                                    hex_value=self.getmacToHex(self.mac_list[sub%len(self.mac_list)])
                                if len(hex_value) <=16:
                                    hex_value=hex_value+['0x00']*(16-len(hex_value))
                                else:
                                    pass
                                dhcp_packet+=hex_value
                                print "CHADDR %s" %(str(hex_value))
                            else:
                                if sub<len(self.cable_circuit_id_list):
                                    dhcp_packet+=self.getmacToHex(self.mac_list[sub])
                                else:
                                    dhcp_packet+=self.getmacToHex(self.mac_list[sub%len(self.cable_circuit_id_list)])
                                print "CHADDR %s" %(str(self.getmacToHex(self.mac_list[sub%len(self.cable_circuit_id_list)])))
                        elif value=='Magic Cookie':
                            dhcp_packet+=self.getIptoHex(Addr_Dict[value])
                            print "Magic Cookie %s" %(str(self.getIptoHex(Addr_Dict[value])))
                        elif value=='CIADDR':
                            dhcp_packet+=self.getIptoHex(self.CIADDR_list[sub%len(self.CIADDR_list)])
                            print "CIADDR %s" %(str(self.getIptoHex(self.CIADDR_list[sub%len(self.CIADDR_list)])))
                        elif value=='GIADDR':
                            dhcp_packet+=self.getIptoHex(self.CIADDR_list[sub%len(self.GIADDR_list)])
                            print "GIADDR %s" %(str(self.getIptoHex(self.GIADDR_list[sub%len(self.GIADDR_list)])))
                        else:
                            dhcp_packet+=Addr_Dict[value]
                            print "%s %s " %(value,str(Addr_Dict[value]))
                dhcp_packet=dhcp_packet+['0x35','0x01','0x05','0xFF']

	    print dhcp_packet
	    final_dhcp_packet=dhcp_packet+['0x00']
            mess=[int(i,16) for i in final_dhcp_packet]
            byte_array = array.array('B',mess)
	    #print byte_array
            self.sock.sendto(byte_array, (self.server_host,self.server_port))

if __name__=="__main__":
    ed_struc=time.strptime(options.EndTime,"%Y-%m-%d-%H")
    ed_epoc=int(time.mktime(ed_struc))
    current_epoc=int(time.time())
    dhcp_obj=DHCPGEN(options.ip,options.port,options.subn,options.csvfile)
    while(current_epoc<ed_epoc):
        dhcp_obj.main()
        time.sleep(300)
