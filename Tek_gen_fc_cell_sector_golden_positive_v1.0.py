'''
Created on Jan 20, 2015

@author: devang.sethi
Modified by rishabh.jain for Map Reduce changes
'''

###### INPUT #######
#GGSN_IP = ['192.168.194.54','192.168.194.61','192.168.194.54','192.168.193.230','192.168.193.227','192.168.193.229','192.168.193.227','192.168.193.229','60.60.60.229','192.168.193.237','192.168.194.57','192.168.194.54','192.168.194.61','192.168.194.54']

GGSN_IP=['192.168.194.54','192.168.194.59','192.168.193.6']
import socket,sys
import binascii
import time,csv
from optparse import OptionParser
from array import *
import random
from random import randint
import multiprocessing
from multiprocessing import Process, Lock, Pool

### Command line options..
parser = OptionParser(usage="usage: %prog [options]",
                          version="%prog 1.0")



parser.add_option("--port", dest="port",
                  help="port")

parser.add_option("--ip", dest="ip",
                  help="ip")


parser.add_option("--TEKfile", dest="file_name",
                  help="TEK File")
parser.add_option("--r", dest="rec",
                  help="number of DRs ")


parser.add_option("--m", dest="mask",
                  help="number of element ID masks ")

parser.add_option("--startTime",
                  dest="StartTime",
                  default="2015-08-10-10",
                  help="Start Time for data (Default = 2015-08-10-10)")

parser.add_option("--EndTime",
                  dest="EndTime",
                  default="2015-08-10-13",
                  help="End Time for Data (Default = 2015-08-10-13)")

parser.add_option("--v", dest="var",
                  help="number of variable fields ")

(options, args) = parser.parse_args()


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def getSub(num):
    start_num=num
    end_num=num+10000000
    list=range(start_num,end_num+1)
    


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
	self.bearerimei=dictExporterInpFiles['bearer-imei']
	self.httpContent=dictExporterInpFiles['http-content']


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
	

       # Parse Imei file
        dictParseConfig['bearer-imei'] = self.storeFileInMem(self.bearerimei)

        # Parse httpContent file
	dictParseConfig['http-content'] = self.storeFileInMem(self.httpContent)
        listStoredFile = dictParseConfig['http-content']
        for i in xrange(len(listStoredFile)):
            line = listStoredFile[i]

            line = line.strip('"')
            line = line.replace('""','"')
            line = line.replace('"','""')
            line = '"' + line + '"'
            listStoredFile[i] = line


	return dictParseConfig









def split_in_two(s):
    if '0x' in s:
        s=s.split('0x')[1]
    return ['0x'+s[i:i+2] for i in range(0, len(s), 2)]


def hex_to_binary_array(k):
    s=""
   
    for i in k:
        if i == '0x00':
            i='00'
        else:
            i=i.lstrip('0x')
        
        out= bin(int(i,16))
        out=out.lstrip('0b').zfill(8)
        
        
       # s=s+out[::-1]
	s=s+out
        
    return s[::-1]





def ip(ip):
    k= binascii.hexlify(socket.inet_aton(ip)).upper()
    k=['0x'+k[i:i+2] for i in range(0, len(k), 2)]
    return k



#If u want the output to be of 4 bytes, give k=2
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




def Inserting_element_masks(mesg,arr, dict, range_start,range_end):
       # global mesg
             
#        mesg.extend(dict['Length_Element'])
        mesg.extend(dict['Mask'])
        binary_eq_of_mask=hex_to_binary_array(dict['Mask'])
        #print range_end
        #print binary_eq_of_mask 
        
        for index in range(range_start,range_end):
            if int(binary_eq_of_mask[index]) !=0:
		#print arr[index]
                mesg.extend(dict[arr[index]])
                
        
                
def Inserting_element_masks_withCount(mesg,arr, dict, range_start,range_end):
        
        if dict.has_key('Reserved'):
            mesg.extend(dict['Reserved'])
        mesg.extend(dict['Counter'])
        #print str(dict['Counter']).replace('[','').replace(']',''.replace("'",""))
	count=int(str(dict['Counter']).replace('[','').replace(']','').replace("'",""),16)
	
        for i in range(0,count):
            mesg.extend(dict['Mask'])
            binary_eq_of_mask=hex_to_binary_array(dict['Mask'])
            #print range_end
      	    #print binary_eq_of_mask 
        
            for index in range(range_start,range_end):
                if int(binary_eq_of_mask[index]) !=0:
            	    #print arr[index]
                    mesg.extend(dict[arr[index]])
                 


Num_ElementID_mask=int(options.mask)



header_dictionary={
                       'Length_blob':['%s'],
                       'Message_Type':split_in_two(padded_hex(13)),
                       'Data_Type':split_in_two(padded_hex(10)),
                       'Format_Type':split_in_two(padded_hex(11)),
                       'Version':split_in_two(padded_hex(101)),
                       'DrCount':split_in_two(padded_hex(int(options.rec))),
                       
                       'IntAndRes':['0x00', '0x00','0X00']
                       
                       }

header_array=['Length_blob',
                       'Message_Type',
                       'Data_Type',
                       'Format_Type',
                       'Version',
                       'DrCount',
                       'IntAndRes']


#to control the number of element Id masks 
BitMask_array=['0x00','0x08','0x10','0x18','0x20']

Fixed_data_dictionary={
                 'DR Length':['%%s'],
                 'BitMask':[BitMask_array[Num_ElementID_mask]],
                 'Reserved':split_in_two(padded_hex(0)),
                 'DrType':split_in_two(padded_hex(8)),
                 'DrInterface':split_in_two(padded_hex(0)),
                 'Length_Element':['%%s']
                 
                 }

Fixed_data_array=['DR Length',
                 'BitMask',
                 'Reserved',
                 'DrType',
                 'DrInterface',
                 'Length_Element'
                 ]

                
                
                

                 
#Word_Size={
#           'Mask':['0x1F','0xFF','0xFF','0xFF'],
#           'CallNumber':split_in_two(padded_hex(11,8)),
#           'StartTime':['%s'],
#           'StartTimeMicrosec':split_in_two(padded_hex(1,8)),
#           'EndTime':['%s'],
#           'EndTimeMicrosec':split_in_two(padded_hex(1,8)),
#           'CallType':split_in_two(padded_hex(1,8)),
#           'SGSN_C':split_in_two(padded_hex(1,8)),
#           'GGSN_C':split_in_two(padded_hex(1,8)),
#           'SGSN_U':split_in_two(padded_hex(1,8)),
#           'GGSN_U':split_in_two(padded_hex(1,8)),
#           'Teid_U':split_in_two(padded_hex(1,8)),
#           'Gblu':split_in_two(padded_hex(1,8)),
#           'Old_SGSN_C':split_in_two(padded_hex(1,8)),
#           'SessionStatus':split_in_two(padded_hex(1,8)),
#           'BearerId':split_in_two(padded_hex(1,8)),
#           'Ex_Call_low':split_in_two(padded_hex(1,8)),
#           'Ex_Call_high':split_in_two(padded_hex(1,8)),
#           'Blade_Id':split_in_two(padded_hex(1,8)),
#           'LinkId':split_in_two(padded_hex(1,8))
#           }

Word_Size={
           'Mask':['0x00','0x07','0xFF','0xFF'],
           'CallNumber':split_in_two(padded_hex(11,8)),
           'StartTime':['%s'],
           'StartTimeMicrosec':split_in_two(padded_hex(11,8)),
           'EndTime':['%s'],
           'EndTimeMicrosec':split_in_two(padded_hex(11,8)),
           'CallType':split_in_two(padded_hex(12,8)),
           'SGSN_C':split_in_two(padded_hex(22,8)),
           'GGSN_C':split_in_two(padded_hex(15,8)),
           'SGSN_U':split_in_two(padded_hex(14,8)),
           'GGSN_U':split_in_two(padded_hex(162,8)),
           'Teid_U':split_in_two(padded_hex(123,8)),
           'Gblu':split_in_two(padded_hex(142,8)),
           'Old_SGSN_C':split_in_two(padded_hex(11,8)),
           'SessionStatus':split_in_two(padded_hex(51,8)),
           'BearerId':split_in_two(padded_hex(52,8)),
           'Ex_Call_low':split_in_two(padded_hex(53,8)),
           'Ex_Call_high':split_in_two(padded_hex(54,8)),
           'Blade_Id':split_in_two(padded_hex(55,8)),
           'LinkId':split_in_two(padded_hex(56,8))
           }




Word_Size_Array=[
           'CallNumber',
           'StartTime',
           'StartTimeMicrosec',
           'EndTime',
           'EndTimeMicrosec',
           'CallType',
           'SGSN_C',
           'GGSN_C',
           'SGSN_U',
           'GGSN_U',
           'Teid_U',
           'Gblu',
           'Old_SGSN_C',
           'SessionStatus',
           'BearerId',
           'Ex_Call_low',
           'Ex_Call_high',
           'Blade_Id',
           'LinkId',]


Short_Size={
           
           'Mask':['0x20','0x07','0xFF','0xFF'],
           'EqId': split_in_two(padded_hex(11,4)),
           'ProcessorId':split_in_two(padded_hex(11,4)),
           'Xdroption':split_in_two(padded_hex(11,4)),
           'NSAPI':split_in_two(padded_hex(11,4)),
           'GtpVersion':split_in_two(padded_hex(11,4)),
           'Lat_RAT':split_in_two(padded_hex(11,4)),
           'GbluFlag':split_in_two(padded_hex(11,4)),
           'CellId':split_in_two(padded_hex(11,4)),
           'App Protocol':split_in_two(padded_hex(11,4)),
           'Sorce Port':split_in_two(padded_hex(11,4)),
           'Dest port':split_in_two(padded_hex(11,4)),
           'SubscriberInfo':split_in_two(padded_hex(11,4)),
           'CGI':split_in_two(padded_hex(11,4)),
           'MSIP Active':split_in_two(padded_hex(11,4)),
           'Splitting info':split_in_two(padded_hex(11,4)),
           'Initial Rat':split_in_two(padded_hex(1,4)),
           'Detach Type':split_in_two(padded_hex(11,4)),
	   'SourceNodeType':split_in_two(padded_hex(10,4)),
           'DestinationNodeType':split_in_two(padded_hex(60,4))
           }

Short_Size_Array=[
           'EqId',
           'ProcessorId',
           'Xdroption',
           'NSAPI',
           'GtpVersion',
           'Lat_RAT',
           'GbluFlag',
           'CellId',
           'App Protocol',
           'Sorce Port',
           'Dest port',
           'SubscriberInfo',
           'CGI',
           'MSIP Active',
           'Splitting info',
           'Initial Rat',
           'Detach Type',
	   'SourceNodeType',
	'DestinationNodeType'
                  ]
Variable_Size={
           'Mask':['0x47','0xFE','0xFF','0xFF'],
           'SourceIP':['0x04']+ ip('1.2.3.4'),
           'Dest IP':['0x04']+ ip('192.168.193.6'),
           'Mobile Ip':['0x04']+ ip('9.8.7.6'),
           'RAI':['0x00'],
           'userAgent':['0x09']+string_to_binary('userAgent'),
           'IMSI':['0x0a']+string_to_binary('1234567890'),
           'IMEISv':['0x0a']+string_to_binary('1234567891'),
           'MSISDN':['0x0b']+string_to_binary('aaab5678910'),
           'FirstPTMSI':['0x0a']+string_to_binary('FirstPTMSI'),
           'LastPTMSI':['0x09']+string_to_binary('LastPTMSI'),
           'APN':['0x03']+string_to_binary('APN'),
           'MappedReqQOS':['0x0c']+string_to_binary('MappedReqQOS'),
           'MappedNegQOS':['0x0c']+string_to_binary('MappedNegQOS'),
           'URL':['0x0b']+string_to_binary('www.aap.com'),
           'bsc':['0x0b']+string_to_binary('www1aap1com'),
           'SgsnName':['0x0b']+string_to_binary('SgsnNAme123'),
           'UserName':['0x07']+string_to_binary('Rishabh'),
           'ECGI':['0x09']+string_to_binary('123456789'),
           'GUTI':['0x07']+string_to_binary('GUTI123'),
           'TAI':['0x06']+string_to_binary('TAI123'),
           'Tunnel End1':['0x01','0x0b']+string_to_binary('TunEnd1-123'),
           'Tunnel End2':['0x01','0x0b']+string_to_binary('TunEnd2-123'),
           'SubscriberMccMnc':['0x09']+string_to_binary('MccMnc123'),
           'UA Profile':['0x08']+string_to_binary('UAPro123'),
           'User Agents':['0x03','0x00','0x06']+string_to_binary('UserA1')+['0x00','0x0a']+string_to_binary('userAgent2')+['0x01','0x01']+string_to_binary('userAgentisoflength257---userAgentisoflength257---userAgentisoflength257---userAgentisoflength257---userAgentisoflength257---userAgentisoflength257---userAgentisoflength257---userAgentisoflength257---userAgentisoflength257---userAgentisoflength257---the end'),
           'EnodeB Ip list':['0x02','0x04'] + ip('1.2.3.4') + ['0x10'] + ip6('aaaa::1')
           }


Variable_Size_Array=['SourceIP',
           'Dest IP',
           'Mobile Ip',
           'RAI',
           'userAgent',
           'IMSI',
           'IMEISv',
           'MSISDN',
           'FirstPTMSI',
           'LastPTMSI',
           'APN',
           'MappedReqQOS',
           'MappedNegQOS',
           'URL',
           'bsc',
           'SgsnName',
           'dummy',
           'UserName',
           'ECGI',
           'GUTI',
           'TAI',
           'Tunnel End1',
           'Tunnel End2',
           'SubscriberMccMnc',
           'UA Profile',
           'User Agents',
           'EnodeB Ip list']




Extended_Variable_Size={
           'Mask':['0x80','0x00','0x27','0xFC'],
           'Network Interface Type':['0x0c']+string_to_binary('NetInType123'),
           'Last CGI':['0x0a']+string_to_binary('LAstCGI123'),
           'Last SAI':['0x0a']+string_to_binary('LastSAI123'),
           'IMEI':['0x07']+string_to_binary('IMEI123'),
           'PairedMSIP':['0x0d']+string_to_binary('PairedMSIP123'),
           'Initial RAI':['0x0c']+string_to_binary('IntialRAI123'),
           'Initial CGI':['0x0c']+string_to_binary('IntialCGI123'),
            'Initial SAI':['0x0c']+string_to_binary('IntialSAI123'),
            'LAI':['0x06']+string_to_binary('LAI123'),
            'PGW IP':['0x14']+ip('1.2.3.4')+ip6('aaaa::1')
            
            
                        }

Extended_Variable_Size_Array=['dummy',
                              'dummy',
                              'Network Interface Type',
           'Last CGI',
           'Last SAI',
           'IMEI',
           'PairedMSIP',
           'Initial RAI',
           'Initial CGI',
            'Initial SAI',
            'LAI',
            'dummy',
            'dummy',
            'PGW IP']





Variable_Section={
                  'Length':['%s'],
                  'Num_of_fields':split_in_two(padded_hex(int(options.var),4)),
                  'Format_Id':['0x00','0x00'],
                  }



Variable_Content={
                  'Data_Id':{1:['0xA0','0x01'],2:['0xA0','0x02'],3:['0xA0','0x03'],4:['0xA0','0x04'],5:['0xA0','0x05'],6:['0xA0','0x06'],7:['0xA0','0x07'],8:['0xA0','0x08']},
                  'BitMask':['0x80'],
                  'Length_of_Data':['0x01'],
                  'Data':['0x32']
                            
                  }


TekIEPart={
           'Length':['%s'],
           'BitMask':['0xFF','0xFF','0xFF','0x00'],
           
           }

CpTrafficVolume={
                 'Mask':['0x00','0x00','0x00','0x3F'],
                 'Packets_Uplink':split_in_two(padded_hex(10000,8)),
                 'Packets_Downlink':split_in_two(padded_hex(10001,8)),
                 'Packts_Unknown':split_in_two(padded_hex(10002,8)),
                 'Bytes_Uplink':split_in_two(padded_hex(10003,8)),
                 'Bytes_Downlink':split_in_two(padded_hex(10004,8)),
                 'Bytes_Unknown':split_in_two(padded_hex(10005,8))
                 }
CpTrafficVolume_Array=['Packets_Uplink',
                 'Packets_Downlink',
                 'Packts_Unknown',
                 'Bytes_Uplink',
                 'Bytes_Downlink',
                 'Bytes_Unknown']


GiXDRKey={
          'Mask':['0xFF'],
          'ProtocolId':split_in_two(padded_hex(11,8)),
          'DestIP':split_in_two(padded_hex(4)) +ip('3.3.3.3'),
          'DestPort':split_in_two(padded_hex(4000,8)),
          'SourcePort':split_in_two(padded_hex(5000,8)),
          'Host':split_in_two(padded_hex(16)) + string_to_binary('www.djpunjab.com'),
          'BearerId':split_in_two(padded_hex(111,8)),
          'MsIp':split_in_two(padded_hex(4)) + ip('2.2.2.2'),
          'ExtendedBitMask':['0xFF','0xFF','0xFF','0xFF']+split_in_two(padded_hex(21,8)) + split_in_two(padded_hex(221,8))
         # 'ApplicationId' and 'Transport Proto' included in the extended bit mask only
          
          }

GiXDRKey_Array=['ProtocolId',
          'DestIP',
          'DestPort',
          'SourcePort',
          'Host',
          'BearerId',
          'MsIp',
          'ExtendedBitMask',
          'ApplicationId',
          'Transport Proto']
GTPULI={
	'Mask':['0x00','0x00','0x00','0xFF'],
	'Rat':split_in_two(padded_hex(1,4)),
	'LenRAI':split_in_two(padded_hex(3,2)),
	'RAI':['0xFF','0xFF','0xFF'],
	'LenCGI':split_in_two(padded_hex(3,2)),
        'CGI':['0x0F','0x0F','0x0F'],
	'LenSAI':split_in_two(padded_hex(3,2)),
        'SAI':['0x0F','0x0F','0x0F']
	}

GTPULI_Array=['Rat',
	      'LenRAI',
	      'RAI',
              'LenCGI',
	      'CGI',
	      'LenSAI',
	      'SAI']

GiTrafficVolumeInfo={
                     'Mask':['0x1F','0xFF'],
                     'PUplink':split_in_two(padded_hex(11,8)),
                     'PDownlink':split_in_two(padded_hex(12,8)),
                     'BUplink':split_in_two(padded_hex(random.choice([200,2000,20000]),8)),
                     'BDownlink':split_in_two(padded_hex(random.choice([100,1000,10000]),8)),
                     'ResponseTime':split_in_two(padded_hex(15,8)),
                     'ServerRTime':split_in_two(padded_hex(16,8)),
                     'ClientRTime':split_in_two(padded_hex(17,8)),
                     'Flow_Duration':split_in_two(padded_hex(18,8)),
                     'Effective_Uplink':split_in_two(padded_hex(19,8)),
                     'Effective_Downlink':split_in_two(padded_hex(20,8)),
                     'Tunnel_Uplink':split_in_two(padded_hex(21,8)),
                     'Tunnel_Downlink':split_in_two(padded_hex(22,8)),
                     'Number_Flows':split_in_two(padded_hex(23,8))
                     
                     }

GiTrafficVolumeInfo_Array=['PUplink',
                     'PDownlink',
                     'BUplink',
                     'BDownlink',
                     'ResponseTime',
                     'ServerRTime',
                     'ClientRTime',
                     'Flow_Duration',
                     'Effective_Uplink',
                     'Effective_Downlink',
                     'Tunnel_Uplink',
                     'Tunnel_Downlink',
                     'Number_Flows']

#COUNT HANDLE KRNA PENA
GiThroughputSample={
                    'Reserved':['0x00'],
                    'Counter':['0x01'],
                    'Mask':['0x00','0x00','0x00','0x0F'],
                    'transfer_time':split_in_two(padded_hex(123456,16)),
                    'payload_bytes':split_in_two(padded_hex(123457,16)),
                    'protocol':split_in_two(padded_hex(123458,8)),
                    'transaction_type':split_in_two(padded_hex(12345679,8))}
GiThroughputSample_Array=['transfer_time',
                    'payload_bytes',
                    'protocol',
                    'transaction_type']
GiFlowDuration={
                'Mask':['0x00','0x00','0x00','0x03'],
                'Flow_uplink':split_in_two(padded_hex(2222,16)),
                'Flow_downlink':split_in_two(padded_hex(3333,16))}

GiFlowDuration_Array=['Flow_uplink',
                      'Flow_downlink']

GiOutOfSequence={
                'Mask':['0x00','0x00','0x00','0x03'],
                'Packets_up':split_in_two(padded_hex(111,8)),
                'packets_down':split_in_two(padded_hex(444,8))}


GiOutOfSequence_Array=['Packets_up',
                       'packets_down']

GiXdrInfoTime={
               'Mask':['0x00','0x03'],
               'start_time':split_in_two(padded_hex(6127772434118420000,16)),
                'end_time':split_in_two(padded_hex(6127772434118880000,16))
               }


GiXdrInfoTime_Array=[
               'start_time',
                'end_time']
GiProtocolInfo={
                'Mask':['0x00','0x03'],
                'UserAgentIndex':['0x00','0x00'],
                'Length+Content':['0x03','0x74','0x65','0x78'],   # 0x746578742F6A617661736372697074
                }

GiProtocolInfo_Array=[
                'UserAgentIndex',
                'Length+Content',
                
                ]

GiTcpExtInfoTime={
                  'Mask':['0x3F'],
                  'pack_uplink':split_in_two(padded_hex(321,8)),
                  'pack_downlink':split_in_two(padded_hex(322,8)),
                  'bytes_up':split_in_two(padded_hex(333,8)),
                  'bytes_down':split_in_two(padded_hex(334,8)),
                  'success_tcp':split_in_two(padded_hex(335,8)),
                  'fail_tcp':split_in_two(padded_hex(336,8))}


GiTcpExtInfoTime_Array=['pack_uplink',
                  'pack_downlink',
                  'bytes_up',
                  'bytes_down',
                  'success_tcp',
                  'fail_tcp',
]
GiTransactionInfoNew={
                      'Counter':['0x01'],
                      'Mask':['0x00','0x0F'],
                      'TCSAL':split_in_two(padded_hex(337,8))+split_in_two(padded_hex(338,8))+split_in_two(padded_hex(339,8))+split_in_two(padded_hex(340,8))+split_in_two(padded_hex(341,8)),
                      'Time':split_in_two(padded_hex(1234567890,16)),
                      'Protocol':split_in_two(padded_hex(346,8)),
                      'FirstTransfer':split_in_two(padded_hex(347,8))
                      }



GiTransactionInfoNew_Array=['TCSAL',
                      'Time',
                      'Protocol',
                      'FirstTransfer'
                      ]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((options.ip, int(options.port)))
#sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

csv_dict=dict()

def tek_rec(data_dict,currtime,sock):
 count=0
 '''
 while (count <len(data_dict.keys())):
  imeiv,imei,upbytes,dnbytes,pgwip,destinationIp,msisdn,imsi,username,Last_Rat,Initial_Rat,protocol_id,application_id,transportprotocol,destport,host,tai,last_rai,last_sai,Content_type,useragent=data_dict[total][-1]
 '''
 for num_packets in range(0,len(data_dict.keys())):
 #for num_packets in range(0,1):     
    #print data_dict[num_packets][-1]
    imeiv,imei,upbytes,dnbytes,pgwip,destinationIp,msisdn,imsi,username,Last_Rat,Initial_Rat,protocol_id,application_id,transportprotocol,destport,host,tai,last_rai,last_sai,Content_type,useragent=data_dict[num_packets][-1].split(",",20)
    #print imeiv,imei,upbytes,dnbytes,pgwip,destinationIp,msisdn,imsi,username,Last_Rat,Initial_Rat,protocol_id,application_id,transportprotocol,destport,host,tai,last_rai,last_sai,Content_type,useragent
    final_mesg=[]
    header=[]
    mesg=[]
    var_mesg=[]
    var_mesg2=[]
    
    for i in header_array:
        header.extend(header_dictionary[i])
    #print 'HEADER'     
    #print header
    
    
    
        
    for k in range(0,int(options.rec)):
	mesg=[]
	var_mesg=[]
        for i in Fixed_data_array:
            mesg.extend(Fixed_data_dictionary[i])
	if Last_Rat:
		Short_Size['Mask']=['0x20','0x07','0xFF','0xFF']
		Short_Size['Lat_RAT']=split_in_two(padded_hex(int(Last_Rat),4))
	else:
		Short_Size['Mask']=['0x20','0x07','0xFF','0xDF']
       	Short_Size['Initial Rat']=split_in_two(padded_hex(int(Initial_Rat),4)) 	
	apn = string_to_binary('Sushfone' + str(random_with_N_digits(1)))
	Variable_Size['APN']=split_in_two(padded_hex(len(apn),2)) + apn
	Variable_Size['UserName']=split_in_two(padded_hex(len(username),2))+string_to_binary(username)	
	if msisdn:
		Variable_Size['MSISDN']=['0x0b']+string_to_binary('51'+str(msisdn))
		#print "MSISDN",Variable_Size['MSISDN']
	else:
		Variable_Size['MSISDN']=['0x00']+string_to_binary("")
	if imsi:
		Variable_Size['IMSI']=['0x0a']+string_to_binary(imsi)
		#print "IMSI",Variable_Size['IMSI']
	else:
		Variable_Size['IMSI']=['0x00']+string_to_binary("")
	if tai:
		tai_list=list()
		for i in range(0,len(tai),2):
			tai_val='0x'+tai[i:i+2]
			tai_list.append(tai_val)
		Variable_Size['TAI']=split_in_two(padded_hex(len(tai)/2,2)) + tai_list
	else:
		Variable_Size['TAI']=['0x00']+string_to_binary('')
	if last_rai:
		last_rai_list=list()
		for i in range(0,len(last_rai),2):
			last_rai_val='0x'+last_rai[i:i+2]
			last_rai_list.append(last_rai_val)
		Variable_Size['RAI']=split_in_two(padded_hex(len(last_rai)/2,2)) + last_rai_list
	else:
		Variable_Size['RAI']=['0x00']+string_to_binary('')
	if last_sai:
		last_sai_list=list()
		for i in range(0,len(last_sai),2):
			last_sai_val='0x'+last_sai[i:i+2]
			last_sai_list.append(last_sai_val)
		Extended_Variable_Size['Last SAI']=split_in_two(padded_hex(len(last_sai)/2,2)) + last_sai_list
	else:
		Extended_Variable_Size['Last SAI']=['0x00']+string_to_binary('')
	if useragent:
		ua = string_to_binary(useragent.rstrip("\n"))
		Variable_Size['User Agents']=['0x01'] + split_in_two(padded_hex(len(ua),4)) + ua
	else:
		ua = string_to_binary('')
		Variable_Size['User Agents']=['0x01'] + split_in_two(padded_hex(len(ua),4)) + ua

	if imeiv:
		add_factor=16-len(imeiv)
		imeiv_string=imeiv+"9"*add_factor
		imeiv_bin = string_to_binary(imeiv_string)
		Variable_Size['IMEISv']=split_in_two(padded_hex(len(imeiv_bin),2))+imeiv_bin
	else:
		Variable_Size['IMEISv']=['0x00']+string_to_binary('')
	if imei:
		imei_bin = string_to_binary(imei)
		Extended_Variable_Size['IMEI']=split_in_two(padded_hex(len(imei_bin),2)) + imei_bin
	else:
		Extended_Variable_Size['IMEI']=['0x00']+string_to_binary('')
	#print "TAI","LAST_RAI","LAST_SAI",Variable_Size['TAI'],Variable_Size['RAI'],Extended_Variable_Size['Last SAI']
	#print "USERAGENT",Variable_Size['User Agents']
	#print "IMEISv",Variable_Size['IMEISv']
	#print 'IMEI',Extended_Variable_Size['IMEI']
	pgwip4,pgwip6=pgwip.split("|")
	#print "pgwip4","pgwip4",pgwip4,pgwip6
	if (pgwip4) and (pgwip6):
		Extended_Variable_Size['PGW IP']=['0x14']+ip(pgwip4.strip())+ip6(pgwip6.strip())
		#print "PGWIP",Extended_Variable_Size['PGW IP']
	elif (pgwip4) and (not pgwip6):
		Extended_Variable_Size['PGW IP']=['0x04']+ip(pgwip4.strip())
	elif (not pgwip4) and (pgwip6):
		Extended_Variable_Size['PGW IP']=['0x10']+ip6(pgwip6.strip())
	elif (not pgwip4) and (not pgwip6):
		Extended_Variable_Size['PGW IP']=['0x00']
	
	GiTrafficVolumeInfo['BUplink']=split_in_two(padded_hex(int(upbytes),8))
	GiTrafficVolumeInfo['BDownlink']=split_in_two(padded_hex(int(dnbytes),8))
	#print 'BUplink',GiTrafficVolumeInfo['BUplink']
	#print 'BDownlink',GiTrafficVolumeInfo['BDownlink']
	#print "PGWIP",Extended_Variable_Size['PGW IP']
        if Num_ElementID_mask==4:
            Inserting_element_masks(mesg,Word_Size_Array, Word_Size,0,19)
            Inserting_element_masks(mesg,Short_Size_Array, Short_Size,0,19)
	    #print '.......................................'
            Inserting_element_masks(mesg,Variable_Size_Array, Variable_Size,0,27)
            Inserting_element_masks(mesg,Extended_Variable_Size_Array, Extended_Variable_Size,2,14)
                
        if Num_ElementID_mask==3:
	    Inserting_element_masks(mesg,Word_Size_Array, Word_Size,0,19)
            Inserting_element_masks(mesg,Short_Size_Array, Short_Size,0,19)
            Inserting_element_masks(mesg,Variable_Size_Array, Variable_Size,0,27)
           
            
        if Num_ElementID_mask==2:
            Inserting_element_masks(mesg,Word_Size_Array, Word_Size,0,19)
            Inserting_element_masks(mesg,Short_Size_Array, Short_Size,0,19)
           
            
        if Num_ElementID_mask==1:
            Inserting_element_masks(mesg,Word_Size_Array, Word_Size,0,19)
    
            
        if Num_ElementID_mask==0:
            pass
                
    # PADDING
    #3 each for start time and end time and 6 bytes of the fixed part to be reduced            
        length_of_element=int(len(mesg)+3+3-6)
#	#print 'length of fixed part'
#	#print length_of_element
	padding_bytes=0
	if length_of_element%4 !=0:
        	padding_bytes= 4-(length_of_element%4)
	length_of_element+=padding_bytes
	#print padding_bytes
        while padding_bytes >0:
            mesg.extend(['0x00'])
            padding_bytes=padding_bytes-1
        #print '.................................................................................'    
        #length_of_element+=padding_bytes
	#print length_of_element
        length_of_element=length_of_element/4
	#print length_of_element 
        #print 'FIXED PART OF MESG '
	#print mesg 
        #var_mesg.extend(Variable_Section['Length'])
        var_mesg.extend(Variable_Section['Num_of_fields'])
        var_mesg.extend(Variable_Section['Format_Id'])
        
        id1=2
        for num in range (0,int(options.var)):
            var_mesg.extend(Variable_Content['Data_Id'][id1])
            var_mesg.extend(Variable_Content['BitMask'])
            var_mesg.extend(Variable_Content['Length_of_Data']) 
            var_mesg.extend(Variable_Content['Data'])
            
            #TekIE
            if id1 == 1:
                var_mesg.extend(split_in_two(padded_hex(32,4)))
                var_mesg.extend(['0x00','0x00','0x01','0x00'])
                Inserting_element_masks(var_mesg,CpTrafficVolume_Array, CpTrafficVolume,0,6)
                #print len(var_mesg)

                id1=2
		continue
            if id1 ==2:
                #var_mesg.extend(split_in_two(padded_hex(2872,4)))
	#	var_mesg.extend(split_in_two(padded_hex(290,4)))
               # var_mesg.extend(['0x00','0x00','0x07','0x9F'])
                #print 'id2'
		if destinationIp:
			GiXDRKey['Mask']=['0xFF']
			GiXDRKey['DestIP']=split_in_two(padded_hex(4)) +ip(destinationIp)
		else:
			GiXDRKey['Mask']=['0xFD']
		#print 'DestIP',GiXDRKey['DestIP']	
		if protocol_id:
			GiXDRKey['Mask']=['0xFF']
			GiXDRKey['ProtocolId']=split_in_two(padded_hex(int(protocol_id),8))
		else:
			GiXDRKey['Mask']=['0xFE']
		#print 'ProtocolId',GiXDRKey['ProtocolId']
		GiXDRKey['DestPort']=split_in_two(padded_hex(int(destport),8))
		#print 'DestPort',GiXDRKey['DestPort']
		if application_id:
			tt=int(application_id)
			tp=int(transportprotocol)
			GiXDRKey['ExtendedBitMask']=['0xFF','0xFF','0xFF','0xFF']+split_in_two(padded_hex(tt,8)) + split_in_two(padded_hex(tp,8))
		else:
			GiXDRKey['ExtendedBitMask']=['0xFF','0xFF','0xFF','0xFE']+split_in_two(padded_hex(tp,8))
		#print 'ExtendedBitMask',GiXDRKey['ExtendedBitMask']
		url = string_to_binary(host)

		GiXDRKey['Host']= split_in_two(padded_hex(len(url))) + url

		#print 'Host',GiXDRKey['Host']
		content_type=string_to_binary(Content_type)
		GiProtocolInfo['Length+Content']= split_in_two(padded_hex(len(Content_type.rstrip("\n")))) + content_type
		#print 'Length+Content',GiProtocolInfo['Length+Content']
		currTime=currtime
		#endXDR= curr - 17
		#startXDR= curr - 300 + 17 
		startXDR=currTime-currTime%300+270
		endXDR=currTime-currTime%300+280
		#print curr,startXDR,endXDR
		GiXdrInfoTime['start_time']=split_in_two(padded_hex(startXDR,8)) + ['0x00','0x00','0x00','0x00']	
                GiXdrInfoTime['end_time']=split_in_two(padded_hex(endXDR,8)) + ['0x00','0x00','0x00','0x00']

		Inserting_element_masks(var_mesg2,GiXdrInfoTime_Array, GiXdrInfoTime,0,2)
		#print len(var_mesg)
                Inserting_element_masks(var_mesg2,GiProtocolInfo_Array, GiProtocolInfo,0,3)
                #print len(var_mesg)
                Inserting_element_masks(var_mesg2,GiXDRKey_Array, GiXDRKey,0,8)
		#print len(var_mesg)
                Inserting_element_masks(var_mesg2,GiTrafficVolumeInfo_Array, GiTrafficVolumeInfo,0,13)
		#print len(var_mesg)
                Inserting_element_masks(var_mesg2,GiTcpExtInfoTime_Array, GiTcpExtInfoTime,0,6)
		#print len(var_mesg)
                Inserting_element_masks_withCount(var_mesg2,GiTransactionInfoNew_Array, GiTransactionInfoNew,0,4)
		#print len(var_mesg)
                Inserting_element_masks(var_mesg2,GiOutOfSequence_Array, GiOutOfSequence,0,2)
		#print len(var_mesg)
                Inserting_element_masks_withCount(var_mesg2,GiThroughputSample_Array, GiThroughputSample,0,4)
		#print len(var_mesg)
                Inserting_element_masks(var_mesg2,GiFlowDuration_Array, GiFlowDuration,0,2)
		#print len(var_mesg)
# 		Inserting_element_masks(var_mesg2,GTPULI_Array, GTPULI,0,6)
                #print len(var_mesg2)
		var_mesg.extend(split_in_two(padded_hex(len(var_mesg2)+4,4)))
                var_mesg.extend(['0x00','0x00','0x07','0x9F'])
		var_mesg.extend(var_mesg2)
               
                
                #id1=1
            
        #print 'variable mesg'
	#print var_mesg 
	padding_bytes=0
	if (len(var_mesg)+2)%4 !=0:       
        	padding_bytes= 4-(len(var_mesg)+2)%4
#	print 'length of variable section'
#	print (len(var_mesg)+2+padding_bytes)/4
#	print padding_bytes
        mesg.extend(split_in_two(padded_hex((len(var_mesg)+2+padding_bytes)/4,4)))
        mesg.extend(var_mesg)
                
        
        while padding_bytes >0:
            mesg.extend(['0x00'])
            padding_bytes=padding_bytes-1    
            
        len_var_mesg=int(len(var_mesg)+padding_bytes+2)/4
        
        #len_DR=(8+4*len_var_mesg+4*length_of_element)/4
        len_DR=(8+len(mesg))/4 
                
                
                
             
            
        len_DR=   str(split_in_two(padded_hex(len_DR,4))).replace('[','').replace(']','').replace("'","")
        len_of_element=  str( split_in_two(padded_hex(length_of_element,4))).replace('[','').replace(']','').replace("'","")   
        #print 'len DR %s      len_element %s' %(len_DR,len_of_element)
        
        
        
        
        currTime=currtime
        start_time= str(split_in_two(padded_hex((currTime-currTime%300+260),8))).replace('[','').replace(']','').replace("'","")
        end_time= str(split_in_two(padded_hex((currTime-currTime%300+290),8))).replace('[','').replace(']','').replace("'","")
        #print curr 
         
        mesg= str(mesg).replace("'","")
        mesg=mesg%(start_time,end_time)
        mesg=mesg%(len_DR,len_of_element)
	mesg=mesg.replace('[','').replace(']','').split(',')
        final_mesg+=mesg       
        
   
    #print final_mesg
    buffer=[]
    header.extend(final_mesg)       
    len_blob=split_in_two(padded_hex(len(header)-1,8))
    #print 'LENGTH OF BLOB %s'%len_blob
    buffer.extend(len_blob)
    del header[0]
    buffer.extend(header)
        
    
         
           
           
    #print buffer       
    
    mess=[int(i,16) for i in buffer]
    byte_array = array('B',mess)
    sock.send(byte_array)
    #sock.sendto( byte_array, (UDP_IP, UDP_PORT) )
    #sys.exit(10)
    #time.sleep(4)           
                 
def call_process(csv_dict,currtime):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((options.ip, int(options.port)))
    #global sock
    currtime=currtime
    tek_rec(csv_dict,currtime,sock)
                    
def getCSVdata(data_dict):
        count=0
        try:
                f=open(options.file_name,'rU')
        except Exception:
                sys.exit(10)
        lines =csv.reader(f,dialect=csv.excel_tab)
	for row in lines:
                csv_dict[count]=row
                count+=1                

                 
if __name__ == '__main__':
	'''
	dictParseConfig = dict()
	dictExporterInpFiles = {'http-content':'http-content','bearer-imei':'bearer-imei','ipProtocolList':'ipProtocolList','http-host': 'http-host_pref' ,'http-user-agent':'http-user-agent_pref', 'http-info':'http-info','ProtocolSignature':'ProtocolSignature_pref'}
	pi = ParseConfig(dictExporterInpFiles)
	dictParseConfig = pi.parseConfig(dictParseConfig)
	'''
        st_struc=time.strptime(options.StartTime,"%Y-%m-%d-%H")
        ed_struc=time.strptime(options.EndTime,"%Y-%m-%d-%H")
        st_epoc=int(time.mktime(st_struc))
        ed_epoc=int(time.mktime(ed_struc))
        getCSVdata(csv_dict)
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
