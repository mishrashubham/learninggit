import time
import socket
import binascii
import time,csv,sys
import random
from optparse import OptionParser
from array import *
import struct
import multiprocessing
from multiprocessing import Process, Lock, Pool

### Command line options..
parser = OptionParser(usage="usage: %prog [options]",
                          version="%prog 1.0")



parser.add_option("--port", dest="port",
                  help="port")

parser.add_option("--ip", dest="ip",
                  help="ip")

parser.add_option("--startTime",
                  dest="StartTime",
                  default="2015-08-10-10",
                  help="Start Time for data (Default = 2015-08-10-10)")

parser.add_option("--EndTime",
                  dest="EndTime",
                  default="2015-08-10-13",
                  help="End Time for Data (Default = 2015-08-10-13)")

parser.add_option("--Radiusfile", dest="file_name",
                  help="Radius File")


parser.add_option("--I", dest="packetsInSession",
                  help="number of packets in a particular session of SCE records")


(options, args) = parser.parse_args()

UDP_PORT=int(options.port)
UDP_IP=options.ip

nas_string,adsl_string=dict(),dict()

def fun(a):
    
    x=[]
    for i in range(0,len(a),2):
        if i==(len(a)-1):
            x.append("0xF%x" % (int(a[i])))  
        else:
            x.append("0x%x%x" % (int(a[i+1]),int(a[i])))
        
    
    return x
    #print hex(20694)


def split_in_two(s):
    if '0x' in s:
        s=s.split('0x')[1]
    return ['0x'+s[i:i+2] for i in range(0, len(s), 2)]


def MACRO(k,b):
    if k=='Macro':
        ans=['0x00']
    else:
        ans=['0x01']
    
    c=b.split('-')
    if len(c[1])==2:
        pass
    else:
        
        x=c[1][2]
        c[1]=c[1].replace(c[1][2],'')
        c[0]=c[0]+x
        
        
    
    ans.extend((fun(c[0])))
    ans.extend((fun(c[1])))
    s= (hex(int(c[2]))).split('0x')[1]
   

    s=s.zfill(8)
    
    
    ans.extend(split_in_two(s))
    return ans



def ECGI(b):
    ans=[]
    
    c=b.split('-')
    if len(c[1])==2:
        pass
    else:
        
        x=c[1][2]
        c[1]=c[1].replace(c[1][2],'')
        c[0]=c[0]+x
        
        
    
    ans.extend((fun(c[0])))
    ans.extend((fun(c[1])))
    s= (c[2]).split('0x')[1]
   

    s=s.zfill(8)
    
    
    ans.extend(split_in_two(s))
    return ans



def PLMN(b):
    ans=[]
    
    c=b.split('-')
    if len(c[1])==2:
        pass
    else:
        
        x=c[1][2]
        c[1]=c[1].replace(c[1][2],'')
        c[0]=c[0]+x
        
        
    
    ans.extend((fun(c[0])))
    ans.extend((fun(c[1])))
    
    return ans

def GUTI(b):
    ans=[]
    
    c=b.split('-')
    if len(c[1])==2:
        pass
    else:
        
        x=c[1][2]
        c[1]=c[1].replace(c[1][2],'')
        c[0]=c[0]+x
        
        
    
    ans.extend((fun(c[0])))
    ans.extend((fun(c[1])))
    s= (c[2]).split('0x')[1]
    ans.extend(split_in_two(s))
    
    s= (c[3]).split('0x')[1]
    ans.extend(split_in_two(s))
    s= (c[4]).split('0x')[1]
    ans.extend(split_in_two(s))
    return ans





def ip(ip):
    k= binascii.hexlify(socket.inet_aton(ip)).upper()
    k=['0x'+k[i:i+2] for i in range(0, len(k), 2)]
    return k


def padded_hex(h,k=0):
    if k==0:
        s=hex(h).split('0x')[1].upper()
        return '0x'+s.zfill(((len(s)/2)+len(s)%2)*2)
    else:
        s=hex(h).split('0x')[1].upper()
        return '0x'+s.zfill(k)



  

def string_to_binary(i):
    return (["0x%02X" % (ord(x)) for x in i])



def ip6(ip):
    k= binascii.hexlify(socket.inet_pton(socket.AF_INET6,ip)).upper()
    k=['0x'+k[i:i+2] for i in range(0, len(k), 2)]
    return k


def get_starting_ip(srcIp):
    srcIp=socket.htonl(srcIp)
    ip=socket.inet_ntoa(struct.pack('!L',srcIp))
    return str(ip)

def mesg():

    data_dictionary={
                     'User-Name':string_to_binary('radius@cisco.com'),
                     'Acct-Status-Type':split_in_two(padded_hex(2,8)),
                     'Acct-Session-Id':string_to_binary('100000'),
                     'Event-Timestamp':split_in_two(padded_hex(3,4)),
                     'Framed-IP-Address':split_in_two(padded_hex(1,8)),
                     'ADSL-Agent-Circuit-ID':string_to_binary(''),
		     'Calling-Station-Id':string_to_binary(''),
                     'Acct-Input-Octets':split_in_two(padded_hex(80,8)),
                     'Acct-Output-Octets':split_in_two(padded_hex(80,8)),
                     'Acct-Session-Time':split_in_two(padded_hex(80,8)),
                     'Acct-Input-Packets':split_in_two(padded_hex(80,8)),
                     'Acct-Output-Packets':split_in_two(padded_hex(1080,8)),
                     'Acct-Delay-Time':split_in_two(padded_hex(1,8)),
                     'Service-Type':split_in_two(padded_hex(1,8)),
                     'Acct-Authentic':split_in_two(padded_hex(1,8)),
                     'ERX-Dhcp-Options':split_in_two(padded_hex(2,8)),
                     'ERX-Dhcp-Gi-Address':split_in_two(padded_hex(3,8)),
                     'ERX-Dhcp-Mac-Address':split_in_two(padded_hex(4,4)),
                     'ERX-Input-Gigapkts':split_in_two(padded_hex(5,4)),
                     'Acct-Input-Gigawords':split_in_two(padded_hex(6,8)),
                     'NAS-Identifier':string_to_binary('vll-citywestaaaaaaaaaaaaaaaaaaaaaaaaaaa'),
                     'NAS-Port':split_in_two(padded_hex(8,8)),
                     'NAS-Port-Id':string_to_binary(''),
                     'NAS-Port-Type':split_in_two(padded_hex(10,8)),
                     'ERX-Output-Gigapkts':split_in_two(padded_hex(11)),
                     'Acct-Output-Gigawords':split_in_two(padded_hex(12,8)),
                     'ERX-IPv6-Acct-Input-Octets':split_in_two(padded_hex(80)), 
                     'ERX-IPv6-Acct-Output-Octets':split_in_two(padded_hex(80)),
                     'ERX-IPv6-Acct-Input-Packets':split_in_two(padded_hex(80)),
		     'ERX-IPv6-Acct-Output-Packets':split_in_two(padded_hex(80)),
		     'ERX-IPv6-Acct-Input-Gigawords':split_in_two(padded_hex(80)),
                     'ERX-IPv6-Acct-Output-Gigawords':split_in_two(padded_hex(80)),
		     'ERX-Virtual-Router-Name':string_to_binary('abcdefghikabcd_k'),
		     'ERX_Pppoe-Description':string_to_binary('abcdefghikabcdefkabcdefghikabcdefghik'),
                     'ADSL-Agent-Remote-ID':split_in_two(padded_hex(80000000)),
		     'NAS-IP-Address':ip('12.22.32.42')
		
		
		 }
    return (data_dictionary)


tag_fields={ 
                 'User-Name':split_in_two(padded_hex(1)),
		 'Acct-Status-Type':split_in_two(padded_hex(40)),
                 'Acct-Session-Id':split_in_two(padded_hex(44)),
                 'Event_Timestamp':split_in_two(padded_hex(55)),
                 'Framed_IP_Address':split_in_two(padded_hex(8)),
                 'ADSL-Agent-Circuit-ID':split_in_two(padded_hex(32)),
		 'Calling-Station-Id':split_in_two(padded_hex(31)),
		 'Acct-Input-Octets':split_in_two(padded_hex(42)),
                 'Acct-Output-Octets':split_in_two(padded_hex(43)),
                 'Acct-Session-Time':split_in_two(padded_hex(46)),
                 'Acct-Input-Packets':split_in_two(padded_hex(47)),
                 'Acct-Output-Packets':split_in_two(padded_hex(48)),
                 'Acct-Delay-Time':split_in_two(padded_hex(41)),
                 'Service-Type':split_in_two(padded_hex(6)),
                 'Acct-Authentic':split_in_two(padded_hex(45)),
                 'ERX-Dhcp-Options':split_in_two(padded_hex(2)),
                 'ERX-Dhcp-Gi-Address':split_in_two(padded_hex(3)),
                 'ERX-Dhcp-Mac-Address':split_in_two(padded_hex(4)),
                 'ERX-Input-Gigapkts':split_in_two(padded_hex(5)),
                 'Acct-Input-Gigawords':split_in_two(padded_hex(52)),
                 'NAS-Identifier':split_in_two(padded_hex(37)),
                 'NAS-Port':split_in_two(padded_hex(5)),
                 'NAS-Port-Id':split_in_two(padded_hex(87)),
                 'NAS-Port-Type':split_in_two(padded_hex(61)),
                 'ERX-Output-Gigapkts':split_in_two(padded_hex(11)),
                 'Acct-Output-Gigawords':split_in_two(padded_hex(53)),
                 'ERX-IPv6-Acct-Input-Octets':split_in_two(padded_hex(80)),
                 'ERX-IPv6-Acct-Output-Octets':split_in_two(padded_hex(80)),
                 'ERX-IPv6-Acct-Input-Packets':split_in_two(padded_hex(80)),
                 'ERX-IPv6-Acct-Output-Packets':split_in_two(padded_hex(80)),
                 'ERX-IPv6-Acct-Input-Gigawords':split_in_two(padded_hex(80)),
                 'ERX-IPv6-Acct-Output-Gigawords':split_in_two(padded_hex(80)),
                 'ERX-Virtual-Router-Name':split_in_two(padded_hex(80)),  
                 'ERX_Pppoe-Description':split_in_two(padded_hex(80)),
                 'ADSL-Agent-Remote-ID':split_in_two(padded_hex(80)),
                 'NAS-IP-Address':split_in_two(padded_hex(4))

                
                }



fields=[
		 'User-Name',
                 'Acct-Status-Type',
                 'Acct-Session-Id',
                 'Event_Timestamp',
                 'Framed_IP_Address',
                 'ADSL-Agent-Circuit-ID',
		 'Calling-Station-Id',
		 'Acct-Input-Octets',
                 'Acct-Output-Octets',
                 'Acct-Session-Time',
                 'Acct-Input-Packets',
                 'Acct-Output-Packets',
                 'Acct-Delay-Time',
                 'Service-Type',
                 'Acct-Authentic',
                 'ERX-Dhcp-Options',
                 'ERX-Dhcp-Gi-Address',
                 'ERX-Dhcp-Mac-Address',
                 'ERX-Input-Gigapkts',
                 'Acct-Input-Gigawords',
                 'NAS-Identifier',
                 'NAS-Port',
                 'NAS-Port-Id',
                 'NAS-Port-Type',
                 'ERX-Output-Gigapkts',
                 'Acct-Output-Gigawords',
                 'ERX-IPv6-Acct-Input-Octets',
                 'ERX-IPv6-Acct-Output-Octets',
                 'ERX-IPv6-Acct-Input-Packets',
                 'ERX-IPv6-Acct-Output-Packets',
                 'ERX-IPv6-Acct-Input-Gigawords',
                 'ERX-IPv6-Acct-Output-Gigawords',
                 'ERX-Virtual-Router-Name',
                 'ERX_Pppoe-Description',
                 'ADSL-Agent-Remote-ID',
                 'NAS-IP-Address'

                 ]


(data_dictionary)=mesg()


csv_dict=dict()

session_start_time=time.time()



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def getTime(type,time_diff,currTime,type_flag):
	currTime=currTime
	if type_flag:
		if type==1:
			min=int(time.strftime("%M",time.gmtime(currTime)))
			if min in range(0,10):
				recTime=currTime-(currTime%3600)+60-time_diff
			elif min in range(30,40):
				recTime=currTime-(currTime%3600)+60+1800-time_diff
			elif min in range(55,57):
				recTime=currTime-(currTime%3600)+60+3300-time_diff
		elif type==3:
			min=int(time.strftime("%M",time.gmtime(currTime)))
			if min in range(0,10):
				recTime=currTime-(currTime%3600)+120-time_diff
			elif min in range(30,40):
				 recTime=currTime-(currTime%3600)+120+1800-time_diff
			elif min in range(55,57):
				recTime=currTime-(currTime%3600)+60+3300-time_diff
		elif type==2:
			min=int(time.strftime("%M",time.gmtime(currTime)))
			if min in range(0,10):
				recTime=currTime-(currTime%3600)+590-time_diff
			elif min in range(30,40):
				recTime=currTime-(currTime%3600)+590+1800-time_diff
			elif min in range(55,57):
				recTime=currTime-(currTime%3600)+90+3300-time_diff
	else:
                if type==1:
			recTime = currTime - currTime%3600+30
		elif type==3:
			recTime = currTime - currTime%3600+1920
		elif type==2:
			recTime = currTime - currTime%3600  + 3599-240
	return recTime

def rad_rec(data_dict,type,currTime,sock): 
 currTime=currTime
 total = 0
 while(total<len(data_dict.keys())):
    ip,calling_id,nas_id,adsl_id,dict_type,user_name=data_dict[total][-1].split(",")
    if dict_type:
	if ";" in dict_type:
		new_type,time_diff=[int(e) for e in dict_type.split(";")]
		print new_type,time_diff
	else:
		new_type=int(dict_type)
		time_diff=0
		print new_type,time_diff
        recTime=getTime(new_type,time_diff,currTime,True) 	
    else:
	new_type=type
	time_diff=0
	recTime=getTime(new_type,time_diff,currTime,False)

    data_dictionary['Event_Timestamp']=split_in_two(padded_hex(recTime,4))
    data_dictionary['Acct-Status-Type']=split_in_two(padded_hex(new_type,4)) 
    data_dictionary['User-Name']=string_to_binary(user_name ) 
    data_dictionary['ADSL-Agent-Circuit-ID']=string_to_binary(adsl_id)
    data_dictionary['NAS-Port-Id']=string_to_binary(nas_id)
    data_dictionary['Calling-Station-Id']=string_to_binary(calling_id)
    if ip:
	data_dictionary['Framed_IP_Address']=split_in_two(padded_hex(int(ip),4))
    else:
	data_dictionary['Framed_IP_Address']=string_to_binary('')
    #print ip	
    head_buffer=[]
    head_buffer.extend(split_in_two(padded_hex(4)))   # code
    head_buffer.extend(split_in_two(padded_hex(175))) # id
    mesg_buffer=[]
    mesg_buffer.extend(string_to_binary("abcdefghijklmnop"))  # Authenticator
    print data_dictionary['Framed_IP_Address']	
    for i in fields:
	#print i,data_dictionary[i]
    	mesg_buffer.extend(tag_fields[i])
    	mesg_buffer.extend(split_in_two(padded_hex(len(data_dictionary[i]) + 2)))
        mesg_buffer.extend(data_dictionary[i])
        
    #print "Message header is %s" %(str(mesg_buffer))
    mesg_buffer=str(mesg_buffer).replace('[','').replace(']','').replace("'","")
       	 
    mesg_buffer1=mesg_buffer.split(',')
    head_buffer.extend(split_in_two(padded_hex((len(mesg_buffer1) + 20),4)))
       
    head_buffer.extend(mesg_buffer1)  
    mess=[int(i,16) for i in head_buffer]
    #print mess
    byte_array = array('B',mess)

    #print byte_array
    sock.sendto(byte_array, (UDP_IP, UDP_PORT))    
    total+=1

def call_process(data_dict,st_epoc):
    global sock
    currTime=int(st_epoc)
    minute =int(time.strftime("%M",time.gmtime(currTime)))
    currentHour =int(time.strftime("%H",time.gmtime(currTime)))
    start_time=currTime
    start_range=range(0,10)
    intriem_range=range(30,40)
    end_range=range(55,57)
    minute = int(time.strftime("%M",time.gmtime(currTime)))
    if minute in start_range:
	rad_rec(data_dict,1,currTime,sock)
    elif minute in intriem_range:
	rad_rec(data_dict,3,currTime,sock)
    elif minute in end_range:
	rad_rec(data_dict,2,currTime,sock)
    else:
         pass
def getCSVdata():
	count=0
	f=open(options.file_name,'rU')
	lines =csv.reader(f,dialect=csv.excel_tab)
	for row in lines:
		csv_dict[count]=row
		count+=1	

if __name__ == '__main__':
		getCSVdata()
		st_struc=time.strptime(options.StartTime,"%Y-%m-%d-%H")
		ed_struc=time.strptime(options.EndTime,"%Y-%m-%d-%H")
		st_epoc=int(time.mktime(st_struc))
		ed_epoc=int(time.mktime(ed_struc))		
		#print csv_dict
        	current_epoc=int(time.time())
        	if st_epoc>current_epoc:
                	time.sleep(st_epoc-current_epoc)
        	else:
                	pass
                while (st_epoc<ed_epoc):
                   print "data generation started ....."
                   if (st_epoc<ed_epoc<int(time.time())):
                        call_process(csv_dict,st_epoc)
                        st_epoc+=300
                        time.sleep(10)
                   elif (st_epoc<=int(time.time()-300)<ed_epoc):
                        call_process(csv_dict,st_epoc)
                        st_epoc+=300
                        time.sleep(10)
                   else:
                        call_process(csv_dict,st_epoc)
                        st_epoc+=300
                        time.sleep(st_epoc-int(time.time()))
                else: 
                        print "given end time is less than given start time"

 
