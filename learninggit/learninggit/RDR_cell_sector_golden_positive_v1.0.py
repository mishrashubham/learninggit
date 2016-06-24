'''
Created on Feb 5, 2015

@author: devang.sethi
Updated by rishabh.jain for HTTP records and stitching with Radius records
'''


import socket
import binascii
import time,csv,sys
from optparse import OptionParser
from array import *
import struct
import random
import sys
import multiprocessing
from multiprocessing import Process, Lock, Pool
### Command line options..
parser = OptionParser(usage="usage: %prog [options]",
                          version="%prog 1.0")



parser.add_option("--port", dest="port",
                  help="port")

parser.add_option("--ip", dest="ip",
                  help="ip")

parser.add_option("--SCEfile", dest="file_name",
                  help="SCE File")

parser.add_option("--s", dest="session_duration",
                  help="duration of the session in secs")

parser.add_option("--startTime",
                  dest="StartTime",
                  default="2015-08-10-10",
                  help="Start Time for data (Default = 2015-08-10-10)")

parser.add_option("--EndTime",
                  dest="EndTime",
                  default="2015-08-10-13",
                  help="End Time for Data (Default = 2015-08-10-13)")

parser.add_option("--I", dest="packetsInSession",
                  help="number of packets in a particular session")


(options, args) = parser.parse_args()

UDP_PORT=int(options.port)
UDP_IP=options.ip

class ParseConfig:
    '''
     Parse Config file and store the parameters into a dictionary
     with values as its tuple.
    '''
    def __init__(self, dictExporterInpFiles):
        self.httpHostFile = dictExporterInpFiles['http-host']
        self.httpUserAgentFile = dictExporterInpFiles['http-user-agent']
        self.ttFile = dictExporterInpFiles['ProtocolSignature']
	self.httpInfoFile=dictExporterInpFiles['http-info']

    def storeFileInMem(self, fileName):
        f = open(fileName)
        lines = f.readlines()
        f.close()

        listStoredFile = list()
        for line in lines:
            line = line.strip('\n\r\t ')
            if not line or line.startswith('#'):
                continue
            listStoredFile.append(line)
        return listStoredFile

    def parseConfig(self, dictParseConfig):
        # Store all the configuration and input files in dictionary.
#        dictParseConfig = dict()

        # Parse Traffic Type Headers file
        dictParseConfig['tt'] = self.storeFileInMem(self.ttFile)

        # Parse http-user-agent file
        dictParseConfig['http-user-agent'] = self.storeFileInMem(self.httpUserAgentFile)
        listStoredFile = dictParseConfig['http-user-agent']
        for i in xrange(len(listStoredFile)):
            line = listStoredFile[i]

            line = line.strip('"')
            line = line.replace('""','"')
            line = line.replace('"','""')
            line = '"' + line + '"'
            listStoredFile[i] = line


        # Parse http-host file
        dictParseConfig['http-host'] = self.storeFileInMem(self.httpHostFile)
        listStoredFile = dictParseConfig['http-host']
        for i in xrange(len(listStoredFile)):
            line = listStoredFile[i]
        
            line = line.strip('"')
            line = line.replace('""','"')
            line = line.replace('"','""')
            line = '"' + line + '"'
            listStoredFile[i] = line

	# Parse http-info file
        dictParseConfig['http-info'] = self.storeFileInMem(self.httpInfoFile)
        listStoredFile = dictParseConfig['http-info']
        for i in xrange(len(listStoredFile)):
            line = listStoredFile[i]

            line = line.strip('"')
            line = line.replace('""','"')
            line = line.replace('"','""')
            line = '"' + line + '"'
            listStoredFile[i] = line
	

        # Parse PortList file
        #dictParseConfig['portList'] = self.storeFileInMem(self.portListFile)

        # Parse appProtocolList file
        #dictParseConfig['appProtocolList'] = self.storeFileInMem(self.appProtocolListFile)

	return dictParseConfig


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

csv_dict=dict()
def mesg():

    
    header_dictionary={
                           'Traffic-Processor-id':['0x01'],
                           'RDR-Length':['%s'],
                           'sourceIPsample':['0x02'],
                           'destIPsample':['0x03'],
                           'sourcePort':split_in_two(padded_hex(4000,4)),
                           'destPort':split_in_two(padded_hex(5000,4)),
                           'FlowContextId':split_in_two(padded_hex(1,8)),
                           'RDR-Tag':['0xF0','0xF0','0xF0','0x10'],
                           'NumofFields':split_in_two(padded_hex(1,2))
                           }
    
    
    data_dictionary={
                     'SUBSCRIBER_ID':string_to_binary('john@telstra.com'),
                     'package_id':split_in_two(padded_hex(100,4)),
                     'SERVICE_id':split_in_two(padded_hex(2,8)),
                     'protocol_id':split_in_two(padded_hex(200,4)),
                     'SKIPPED_SESSIONS':split_in_two(padded_hex(1,8)),
                     'SERVER_IP':ip('1.2.3.4'),
                     'server_port':split_in_two(padded_hex(21,4)),
                     'access_string':string_to_binary('dj.punjab.com'),
                     'info_string':string_to_binary('/en/INDIA/partner'),
                     'client_IP':ip('12.22.32.42'),
                     'client_port':split_in_two(padded_hex(136,4)),
                     'initiating_side':split_in_two(padded_hex(0)),
                     'report_time':['%s'],
                     'millisec':split_in_two(padded_hex(60000,8)),
                     'time_frame':split_in_two(padded_hex(1)),
                     'down_vol':split_in_two(padded_hex(100,8)),
                     'up_vol':split_in_two(padded_hex(100,8)),
                     'counter_id':split_in_two(padded_hex(4,4)),
                     'global_counter_id':split_in_two(padded_hex(5,4)),
                     'package_counter_id':split_in_two(padded_hex(6,4)),
                     'ip_protocol':split_in_two(padded_hex(17)),
                     'protocol_signature':split_in_two(padded_hex(8,8)),
                     'zone_id':split_in_two(padded_hex(9,8)),
                     'flavour_id':split_in_two(padded_hex(10,8)),
                     'flow_close_mode':split_in_two(padded_hex(11)),
                     'session_link_id':split_in_two(padded_hex(12)),
                     'ip_type':split_in_two(padded_hex(0)), 
                     'server_ip6':string_to_binary('2001:0db8:f0fd:a0bd:1234:98dc:cccc:aa24'),
                     'client_ip6':string_to_binary('2001:1'),
		     'USER_AGENT':string_to_binary('Mozilla'),
		     'HTTP_REFERER':string_to_binary('http://addition.cnn.com'),
		     'HTTP_COOKIE':string_to_binary('SelectedAddition=Addition;CNNid=3459286729-09'),
                     'ATTRIBUTE_INDICATOR':split_in_two(padded_hex(1,8)),
                     'ACCT-MULTI-SESSION-ID':string_to_binary('Subscriber1'),
                     'ACCT-SESSION-ID':string_to_binary('acct-session-id'),
                     'FRAMED-IP-ADDRESS':ip('12.22.32.42'),
                     'CALLED-STATION-ID':split_in_two(padded_hex(32,8)),
                     '3GPP-IMEISV':string_to_binary('3GPP_IMEISV'),
                     '3GPP-IMSI':string_to_binary('3GPP_IMSI'),
                     '3GPP-RAT-TYPE':string_to_binary('3GPP-RAT-TYPE'),
                     '3GPP-SGSN-ADDRESS':ip('12.25.32.42'),
                     '3GPP-SGSN-MCC-MNC':string_to_binary('3GPP-SGSN-MCC-MNC'),
                     '3GPP-USER-LOCATION-INFO':string_to_binary('3GPP-USER-LOCATION-INFO'),
                     'WIMAX-BSID':string_to_binary('WIMAX-BSID'),
                     '3GPP2-MEID':string_to_binary('3GPP-MEID'),
                     '3GPP2-ESN':string_to_binary('3GPP2-ESN'),
                     '3GPP2-PCF-IP-Address':ip('12.25.32.244'),
                     '3GPP2-Home-Agent-IPAddress':ip('12.25.234.234'),
                     'Framed-IPv6-Prefix':string_to_binary('Framed-IPv6-Prefix'),
     
                     
                     }
    return (header_dictionary,data_dictionary)



tag_fields={ 
                 'SUBSCRIBER_ID':split_in_two(padded_hex(41)),
                 'package_id':split_in_two(padded_hex(12)),
                 'SERVICE_id':split_in_two(padded_hex(13)),
                 'protocol_id':split_in_two(padded_hex(12)),
                 'SKIPPED_SESSIONS':split_in_two(padded_hex(16)),
                 'SERVER_IP':split_in_two(padded_hex(16)),
                 'server_port':split_in_two(padded_hex(15)),
                 'access_string':split_in_two(padded_hex(41)),
                 'info_string':split_in_two(padded_hex(41)),
                 'client_IP':split_in_two(padded_hex(16)),
                 'client_port':split_in_two(padded_hex(15)),
                 'initiating_side':split_in_two(padded_hex(11)),
                 'report_time':split_in_two(padded_hex(16)),
                 'millisec':split_in_two(padded_hex(16)),
                 'time_frame':split_in_two(padded_hex(11)),
                 'up_vol':split_in_two(padded_hex(16)),
                 'down_vol':split_in_two(padded_hex(16)),
                 'counter_id':split_in_two(padded_hex(15)),
                 'global_counter_id':split_in_two(padded_hex(15)),
                 'package_counter_id':split_in_two(padded_hex(15)),
                 'ip_protocol':split_in_two(padded_hex(14)),
                 'protocol_signature':split_in_two(padded_hex(13)),
                 'zone_id':split_in_two(padded_hex(13)),
                 'flavour_id':split_in_two(padded_hex(13)),
                 'flow_close_mode':split_in_two(padded_hex(14)),
                 'session_link_id':split_in_two(padded_hex(11)),
                 'ip_type':split_in_two(padded_hex(14)),
                 'server_ip6':split_in_two(padded_hex(41)),
                 'client_ip6':split_in_two(padded_hex(41)),
		 'USER_AGENT':split_in_two(padded_hex(41)),
                 'HTTP_REFERER':split_in_two(padded_hex(41)),
                 'HTTP_COOKIE':split_in_two(padded_hex(41)),
                 'ATTRIBUTE_INDICATOR':split_in_two(padded_hex(16)),
                 'ACCT-MULTI-SESSION-ID':split_in_two(padded_hex(41)),
                 'ACCT-SESSION-ID':split_in_two(padded_hex(41)),
                 'FRAMED-IP-ADDRESS':split_in_two(padded_hex(16)),
                 'CALLED-STATION-ID':split_in_two(padded_hex(16)),
                 '3GPP-IMEISV':split_in_two(padded_hex(41)),
                 '3GPP-IMSI':split_in_two(padded_hex(41)),
                 '3GPP-RAT-TYPE':split_in_two(padded_hex(41)),
                 '3GPP-SGSN-ADDRESS':split_in_two(padded_hex(16)),
                 '3GPP-SGSN-MCC-MNC':split_in_two(padded_hex(41)),
                 '3GPP-USER-LOCATION-INFO':split_in_two(padded_hex(41)),
                 'WIMAX-BSID':split_in_two(padded_hex(41)),
                 '3GPP2-MEID':split_in_two(padded_hex(41)),
                 '3GPP2-ESN':split_in_two(padded_hex(41)),
                 '3GPP2-PCF-IP-Address':split_in_two(padded_hex(16)),
                 '3GPP2-Home-Agent-IPAddress':split_in_two(padded_hex(16)),
                 'Framed-IPv6-Prefix':split_in_two(padded_hex(41))

      		           
                }


fields_TUR=[
                 'SUBSCRIBER_ID',
                 'package_id',
                 'SERVICE_id',
		 'protocol_id',
                 'SKIPPED_SESSIONS',
                 'SERVER_IP',
                 'server_port',
                 'access_string',
                 'info_string',
                 'client_IP',
                 'client_port',
                 'initiating_side',
                 'report_time',
                 'millisec',
                 'time_frame',
                 'up_vol',
                 'down_vol',
                 'counter_id',
                 'global_counter_id',
                 'package_counter_id',
                 'ip_protocol',
                 'protocol_signature',
                 'zone_id',
                 'flavour_id',
                 'flow_close_mode',
                 'session_link_id',
                 'ip_type',
                 'server_ip6',
                 'client_ip6'
]
'''
fields_HTTP={
                 1:{'SUBSCRIBER_ID':True},
                 2:{'package_id':True},
                 3:{'SERVICE_id':True},
                 4:{'protocol_id':True},
                 5:{'SKIPPED_SESSIONS':True},
                 6:{'SERVER_IP':True},
                 7:{'server_port':True},
                 8:{'access_string':True},
                 9:{'info_string':True},
                 10:{'client_IP':True},
                 11:{'client_port':True},
                 12:{'initiating_side':True},
                 13:{'report_time':True},
                 14:{'millisec':True},
                 15:{'time_frame':True},
                 16:{'up_vol':True},
                 17:{'down_vol':True},
                 18:{'counter_id':True},
                 19:{'global_counter_id':True},
                 20:{'package_counter_id':True},
                 21:{'ip_protocol':True},
                 22:{'protocol_signature':True},
                 23:{'zone_id':True},
                 24:{'flavour_id':True},
                 25:{'flow_close_mode':True},
		 26:{'USER_AGENT':False},
		 27:{'HTTP_REFERER':True},
		 28:{'HTTP_COOKIE':True},
                 29:{'session_link_id':True},
                 30:{'ip_type':True},
                 31:{'server_ip6':True},
                 32:{'client_ip6':True},
		 33:{'ATTRIBUTE_INDICATOR':True},
		 34:{'ACCT-MULTI-SESSION-ID':True},
		 35:{'ACCT-SESSION-ID':True},
		 36:{'FRAMED-IP-ADDRESS':True},
		 37:{'CALLED-STATION-ID':True},
		 38:{'3GPP-IMEISV':True},
		 39:{'3GPP-IMSI':True},
		 40:{'3GPP-RAT-TYPE':True},
		 41:{'3GPP-SGSN-ADDRESS':True},
		 42:{'3GPP-SGSN-MCC-MNC':True},
		 43:{'3GPP-USER-LOCATION-INFO':True},
		 44:{'WIMAX-BSID':True},
		 45:{'3GPP2-MEID':True},
		 46:{'3GPP2-ESN':True},
		 47:{'3GPP2-PCF-IP-Address':True},
		 48:{'3GPP2-Home-Agent-IPAddress':True},
		 49:{'Framed-IPv6-Prefix':True}}
'''
fields_HTTP=[
                 'SUBSCRIBER_ID',
                 'package_id',
                 'SERVICE_id',
                 'protocol_id',
                 'SKIPPED_SESSIONS',
                 'SERVER_IP',
                 'server_port',
                 'access_string',
                 'info_string',
                 'client_IP',
                 'client_port',
                 'initiating_side',
                 'report_time',
                 'millisec',
                 'time_frame',
                 'up_vol',
                 'down_vol',
                 'counter_id',
                 'global_counter_id',
                 'package_counter_id',
                 'ip_protocol',
                 'protocol_signature',
                 'zone_id',
                 'flavour_id',
                 'flow_close_mode',
                 'USER_AGENT',
                 'HTTP_REFERER',
                 'HTTP_COOKIE',
                 'session_link_id',
                 'ip_type',
                 'server_ip6',
                 'client_ip6',
                 'ATTRIBUTE_INDICATOR',
                 'ACCT-MULTI-SESSION-ID',
                 'ACCT-SESSION-ID',
                 'FRAMED-IP-ADDRESS',
                 'CALLED-STATION-ID',
                 '3GPP-IMEISV',
                 '3GPP-IMSI',
                 '3GPP-RAT-TYPE',
                 '3GPP-SGSN-ADDRESS',
                 '3GPP-SGSN-MCC-MNC',
                 '3GPP-USER-LOCATION-INFO',
                 'WIMAX-BSID',
                 '3GPP2-MEID',
                 '3GPP2-ESN',
                 '3GPP2-PCF-IP-Address',
                 '3GPP2-Home-Agent-IPAddress',
                 'Framed-IPv6-Prefix']

(header_dictionary,data_dictionary)=mesg()


csv_data=dict()

session_start_time=time.time()


#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect((options.ip, int(options.port)))

def tur_record(data_dict,sock,st_epoc):
 total=0
 while(total<len(data_dict.keys())):
    initiating_side,client_ip,server_ip,package_id,up_vol,dn_vol,protocol_id,server_port,client_port,ip_protocol,flavour_id,zone_id=data_dict[total]["TUR"][-1].split(",")
    data_dictionary['initiating_side']=split_in_two(padded_hex(int(initiating_side),2))
    data_dictionary['client_IP']=split_in_two(padded_hex(int(client_ip),8))
    data_dictionary['SERVER_IP']=split_in_two(padded_hex(int(server_ip),8))
    data_dictionary['package_id']=split_in_two(padded_hex(int(package_id),4))
    data_dictionary['down_vol']=split_in_two(padded_hex(int(dn_vol),8))
    data_dictionary['up_vol']=split_in_two(padded_hex(int(up_vol),8))
    data_dictionary['client_port']=split_in_two(padded_hex(int(client_port),4))
    data_dictionary['server_port']=split_in_two(padded_hex(int(server_port),4))
    data_dictionary['ip_protocol']=split_in_two(padded_hex(int(ip_protocol),2))
    data_dictionary['zone_id']=split_in_two(padded_hex(int(zone_id),8))
    #print client_ip,data_dictionary['client_IP']
    if protocol_id:
	data_dictionary['protocol_id']=split_in_two(padded_hex(int(protocol_id),4))
        data_dictionary['flavour_id']=split_in_two(padded_hex(int(flavour_id),8))
    else:
	 data_dictionary['protocol_id']=string_to_binary("")
         data_dictionary['flavour_id']=string_to_binary("")

    for num in range(0,int(options.packetsInSession)):
        mesg_buffer=[]
        count=0
        for i in fields_TUR:
            	mesg_buffer.extend(tag_fields[i])
            	if i in ['report_time']:
                	mesg_buffer.extend(split_in_two(padded_hex(4,8)))
                	mesg_buffer.extend(data_dictionary[i])
			#print i,split_in_two(padded_hex(4,8)),data_dictionary[i]
            	elif i in ['SERVER_IP','client_IP']:
                	if data_dictionary['ip_type']==['0x01']:
                    		mesg_buffer.extend(split_in_two(padded_hex(1,8)))
                   	 	mesg_buffer.extend(['0x00'])
                	else :
                    		mesg_buffer.extend(split_in_two(padded_hex(len(data_dictionary[i]),8)))
                    		mesg_buffer.extend(data_dictionary[i])
				#print i,split_in_two(padded_hex(len(data_dictionary[i]),8)),data_dictionary[i]
            	elif i in ['server_ip6','client_ip6']:
                	data_dictionary[i]=string_to_binary(' ')
                	mesg_buffer.extend(split_in_two(padded_hex(len(data_dictionary[i]),8)))
                	mesg_buffer.extend(data_dictionary[i])

            	else:

                	mesg_buffer.extend(split_in_two(padded_hex(len(data_dictionary[i]),8)))
                	mesg_buffer.extend(data_dictionary[i])
			#print i,split_in_two(padded_hex(len(data_dictionary[i]),8)),data_dictionary[i]
            	count +=1

        header_dictionary['NumofFields']= split_in_two(padded_hex(count,2))

        #currTime=int(time.time())
        report_time= str(split_in_two(padded_hex((st_epoc-st_epoc%300+290),8))).replace('[','').replace(']','').replace("'","")
        mesg_buffer=str(mesg_buffer).replace('[','').replace(']','').replace("'","")
        mesg_buffer1=mesg_buffer%(report_time).replace('[','').replace(']','')

        mesg_buffer1=mesg_buffer1.split(',')

	#print split_in_two(padded_hex(len(data_dictionary['protocol_id']),8)),data_dictionary['protocol_id']
        header = []
        header.extend(header_dictionary['Traffic-Processor-id'])
        header.extend(string_to_binary(str(len(mesg_buffer1)+15).zfill(4)))
     #   header.extend(split_in_two(padded_hex(len(mesg_buffer1)+15,4)))
        header.extend(header_dictionary['sourceIPsample'])
        header.extend(header_dictionary['destIPsample'])
        header.extend(header_dictionary['sourcePort'])
        header.extend(header_dictionary['destPort'])
        header.extend(header_dictionary['FlowContextId'])
        header.extend(['0xF0','0xF0','0xF4','0x38'])
        #header.extend(header_dictionary['RDR-Tag'])
        header.extend(split_in_two(padded_hex(29)))
        #header.extend(header_dictionary['NumofFields'])
        #http - F0F0F43C
        #tur - F0F0F438
	

        header.extend(mesg_buffer1)

        print "Sending tur data for timestamp %s" %st_epoc
        mess=[int(i,16) for i in header]

        byte_array = array('B',mess)
        sock.send(byte_array)
    total+=1
#   if (total==len(data_dict.keys())):
#       total=0
    
    #time.sleep(1)
def http_record(data_dict,sock,st_epoc):
 total=0
 while(total<len(data_dict.keys())):
    #print data_dict[total]["HTTP"][-1]
    initiating_side,client_ip,server_ip,package_id,up_vol,dn_vol,access_string,info_string,useragent=data_dict[total]["HTTP"][-1].split(",",8)
    #print initiating_side,client_ip,server_ip,package_id,up_vol,dn_vol,access_string,info_string,useragent
    data_dictionary['initiating_side']=split_in_two(padded_hex(int(initiating_side),2))
    data_dictionary['client_IP']=split_in_two(padded_hex(int(client_ip),8))
    data_dictionary['SERVER_IP']=split_in_two(padded_hex(int(server_ip),8))
    data_dictionary['package_id']=split_in_two(padded_hex(int(package_id),4))
    data_dictionary['down_vol']=split_in_two(padded_hex(int(dn_vol),8))
    data_dictionary['up_vol']=split_in_two(padded_hex(int(up_vol),8))
    #print client_ip,data_dictionary['client_IP']
    if useragent:
	data_dictionary['USER_AGENT']=string_to_binary(useragent)
	#print data_dictionary['USER_AGENT']
    else:
	data_dictionary['USER_AGENT']=string_to_binary("")
    if access_string:
	data_dictionary['access_string']=string_to_binary(access_string)
	#print data_dictionary['access_string']
    else:
	data_dictionary['access_string']=string_to_binary("")
	#print data_dictionary['access_string']
    if info_string:
	data_dictionary['info-string']=string_to_binary(info_string)
	#print data_dictionary['info-string']
    else:
	data_dictionary['info-string']=string_to_binary("")
	#print data_dictionary['info-string']

    for num in range(0,int(options.packetsInSession)):
        mesg_buffer=[]
        count=0
        for i in fields_HTTP:
            mesg_buffer.extend(tag_fields[i])
	    #print i,tag_fields[i]
            if i in ['report_time']:
                mesg_buffer.extend(split_in_two(padded_hex(4,8)))
                mesg_buffer.extend(data_dictionary[i])
		#print split_in_two(padded_hex(4,8)),data_dictionary[i]
            elif i in ['SERVER_IP','client_IP']:
                if data_dictionary['ip_type']==['0x01']:
                    mesg_buffer.extend(split_in_two(padded_hex(1,8)))
                    mesg_buffer.extend(['0x00'])
                else :
                    mesg_buffer.extend(split_in_two(padded_hex(len(data_dictionary[i]),8)))
                    mesg_buffer.extend(data_dictionary[i])
		    #print split_in_two(padded_hex(len(data_dictionary[i]),8)),data_dictionary[i]
            elif i in ['server_ip6','client_ip6']:
                if data_dictionary['ip_type']==['0x00']:
                    data_dictionary[i]=string_to_binary(' ')
                    mesg_buffer.extend(split_in_two(padded_hex(len(data_dictionary[i]),8)))
                    mesg_buffer.extend(data_dictionary[i])
		    #print split_in_two(padded_hex(len(data_dictionary[i]),8)),data_dictionary[i]

                else :
                    mesg_buffer.extend(split_in_two(padded_hex(len(data_dictionary[i]),8)))
                    mesg_buffer.extend(data_dictionary[i])
		    #print split_in_two(padded_hex(len(data_dictionary[i]),8)),data_dictionary[i]
            else:

                mesg_buffer.extend(split_in_two(padded_hex(len(data_dictionary[i]),8)))
                mesg_buffer.extend(data_dictionary[i])
		#print split_in_two(padded_hex(len(data_dictionary[i]),8)),data_dictionary[i]
            count +=1

        header_dictionary['NumofFields']= split_in_two(padded_hex(count,2))
	
	#currTime=int(time.time())
        report_time= str(split_in_two(padded_hex((st_epoc-st_epoc%300+290),8))).replace('[','').replace(']','').replace("'","")
        mesg_buffer=str(mesg_buffer).replace('[','').replace(']','').replace("'","")
        mesg_buffer1=mesg_buffer%(report_time).replace('[','').replace(']','')

        mesg_buffer1=mesg_buffer1.split(',')


        header = []
        header.extend(header_dictionary['Traffic-Processor-id'])
        header.extend(string_to_binary(str(len(mesg_buffer1)+15).zfill(4)))
      # header.extend(split_in_two(padded_hex(len(mesg_buffer1)+15,4)))
        header.extend(header_dictionary['sourceIPsample'])
        header.extend(header_dictionary['destIPsample'])
        header.extend(header_dictionary['sourcePort'])
        header.extend(header_dictionary['destPort'])
        header.extend(header_dictionary['FlowContextId'])
        header.extend(['0xF0','0xF0','0xF4','0x3C'])
        #header.extend(header_dictionary['RDR-Tag'])
        header.extend(split_in_two(padded_hex(49)))
        # header.extend(header_dictionary['NumofFields'])
        #http - F0F0F43C
        #tur - F0F0F438
        header.extend(mesg_buffer1)

	#print header
        print "Sending http data for timestamp %s" %st_epoc
        mess=[int(i,16) for i in header]
        byte_array = array('B',mess)
        sock.send(byte_array)
    total+=1
#    if (total==len(data_dict.keys())):
#        total=0

   #time.sleep(1)

def send_process(data_dict,st_epoc):
 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 #print options.ip,int(options.port)
 sock.connect((options.ip, int(options.port)))
 #global sock
 tur_record(data_dict,sock,st_epoc)
 http_record(data_dict,sock,st_epoc)

def getCSVdata(data_dict):
	count=0
        try:
                f=open(options.file_name,'rU')
        except Exception:
                sys.exit(10)
	lines =csv.reader(f,dialect=csv.excel_tab)
	for row in lines:
		if not count%2:
			data_dict[count/2]=dict()
			data_dict[count/2]["TUR"]=row
			count+=1
		else:
			data_dict[(count-1)/2]["HTTP"]=row
			count+=1

if __name__ == '__main__':

	#print "HI"
	print options.StartTime
	st_struc=time.strptime(options.StartTime,"%Y-%m-%d-%H")
	ed_struc=time.strptime(options.EndTime,"%Y-%m-%d-%H")
	st_epoc=int(time.mktime(st_struc))
	ed_epoc=int(time.mktime(ed_struc))
	#print time.ctime(st_epoc),time.ctime(ed_epoc),time.ctime(int(time.time()))
	getCSVdata(csv_dict)
	print time.ctime(st_epoc),time.ctime(ed_epoc),time.ctime(int(time.time()))
	current_epoc=int(time.time())
        if st_epoc>current_epoc:
                time.sleep(st_epoc-current_epoc)
        else:   
                pass
        while (st_epoc<ed_epoc):
            if (st_epoc<ed_epoc<int(time.time())):
                send_process(csv_dict,st_epoc)
                st_epoc+=300
                time.sleep(10)
            elif (st_epoc<=int(time.time()-300)<ed_epoc):
                send_process(csv_dict,st_epoc)
                st_epoc+=300
                time.sleep(10)
            else: 
                send_process(csv_dict,st_epoc)
                st_epoc+=300
                time.sleep(st_epoc-int(time.time()))
        else:
              print "given end time is less than given start time"
