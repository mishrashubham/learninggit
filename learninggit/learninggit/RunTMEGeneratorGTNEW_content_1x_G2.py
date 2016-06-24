
"""
@package  Tethering Data Generator
@copyright    2006-2012, GUAVUS Inc.
@version      GIT: $Id: RunTMEGeneartor.py,v 1.0 2013/03/07 10:00:00 
@author: Rahul bagai 

@internal Revisions:
"""

from TMEGeneratorGTNEW_USPacific import *
from optparse import OptionParser


parser = OptionParser()
parser.add_option("--st",dest="start_time",
                    help="Start Time for data,eg:-December 19 14:25:00 2015")
parser.add_option("--et",dest="end_time",
                    help="End Time for data,eg:-December 19 14:25:00 2015")
parser.add_option("--ip", dest="ip",
                  help="destination IP")
parser.add_option("--g", dest="gzip",
                                  default="yes",
                                 help="You want to compress the file?(yes/no)")
parser.add_option("--uname", dest="user_name",
                                   help="username for  the destination server")
parser.add_option("--http", dest="server_http_directory",
                                 default="/data/collector/edrhttp/",
                                 help="collector directory in which you want to write http data")
parser.add_option("--flow", dest="server_flow_directory",
                                 default="/data/collector/edrflow/",help="collector directory in which you want to write flow data")
parser.add_option("--format",dest="date_format",
                  help="you want to change the format.use 1 for epoch time format and 2 for (%Y/%m/%H/%M) time format"


(options, args) = parser.parse_args()
############################################### Common Configurations ################################################

# FileFormat
# <file-name format of incoming files. Date and time keywords must be configured as below: >
# %YYYY or %YY    - Year as numeric (eg. 2012 or 12)
# %Mmm or %MM     - Month as case-insensitive string (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec)
#           or MM as numeric   (01-12)
# %DD             - Day as numeric     (01-31)
# %hh             - Hour as numeric    (00-23)
# %mm             - Minutes as numeric (00-59)
# %ss             - Seconds as numeric (00-59)
# For example : ab.cde_fgh.%YYYY%MM%DD_%hh%mm%ss.RC.*.txt.gz
# Note: Ignore any * or special case characters for regular expression. (Give Only exact file formats with date-time keywords only).
flowFileFormat = 'GMPLAB3_MURAL-edr_flow_format_%MM%DD%YYYY%hh%mm%ss_golden.gz'
httpFileFormat = 'GMPLAB3_MURAL-edr_http_format_%MM%DD%YYYY%hh%mm%ss_golden.gz'

#flowFileFormat = 'MURAL_edr-flow_%MM%DD%YYYY%hh%mm%ss_1_2.gz'
#httpFileFormat = 'MURAL_edr-http_%MM%DD%YYYY%hh%mm%ss_1_2.gz'

# StartTime of the exporter format June 07 00:00:00 2012
print options.start_time
strStartTime =options.start_time
dateformat=options.date_format
print strStartTime

# EndTime of the exporter format June 07 00:00:00 2012
strEndTime = options.end_time
print strEndTime
# GZipOn? yes/no
gzipOn =options.gzip 



# Server Details
server_ip =options.ip
server_username =options.user_name

server_http_directory =options.server_http_directory
server_flow_directory =options.server_flow_directory

#server_http_directory = '/data/collector/GMPLAB3/edr/'
#server_flow_directory = '/data/collector/GMPLAB3/edr/'

#####################################################################################################################
##### Declaration####
recordInfoList = list()
#####################################################################################################################


#Http
#User: 3000000001
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000001'
sampleRecord = '10,20,3000000001,1000000,1000000,1.1.1.1,27.2.248.155,images.badoo.com,text/javascript,images.badoo.com,11,,60,1,1,Sushfone-1,48|128|1|65535|1260|0|1010,35245206-0100-65,GET,305 Use Proxy,"""Mozilla/5.0 (iPad Simulator; U; CPU iPhone OS 3_2 like Mac OS X; en_us) AppleWebKit/525.18.1 (KHTML, like Gecko)"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',1000000,100,100,'Yes','48|128|1|65535|1260|0|1010','1','35245206-0100-65')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000001
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000001'
sampleRecord = '10,20,3000000001,137,,1000000,1000000,182,36,,27.9.126.155,1,1,FromMobile,,1,35245206-0100-65,2.2.2.1,27.23.157.1,20,10,Sushfone-1,231-10-1073-10064,43769,101,rb31,48|128|1|65535|1260|0|1010,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',1000000,100,100,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000002
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000002'
sampleRecord = '10,21,3000000002,900000,900000,1.1.1.1,27.2.248.155,www.eharmony.com,application/javascript,www.eharmony.com,11,,60,1,2,Sushfone-2,,35326707-0100-65,GET,400 Bad Request,"""Mozilla/5.0 (iPad; U; CPU iPhone OS 4_2 like Mac OS X; en_us) AppleWebKit/525.18.1 (KHTML, like Gecko)"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',900000,98,98,'Yes','','0','35326707-0100-65')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000002
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000002'
sampleRecord = '10,21,3000000002,70000,50,900000,900000,182,36,,27.9.126.155,2,1,FromMobile,,0,35326707-0100-65,2.2.2.1,27.23.157.2,21,10,Sushfone-2,231-10-1073-10065,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',900000,98,98,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000003
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000003'
sampleRecord = '10,22,3000000003,800000,800000,1.1.1.1,27.2.248.155,a1179.phobos.apple.com,image/gif,a1179.phobos.apple.com,11,,60,1,1,Sushfone-1,48|128|1|65535|1260|0|1010,35881501-0100-66,GET,402 Payment Required,"""Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',800000,96,96,'Yes','48|128|1|65535|1260|0|1010','1','35881501-0100-66')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000003
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000003'
sampleRecord = '10,22,3000000003,70000,29,800000,800000,182,36,,27.9.126.155,1,1,FromMobile,,1,35881501-0100-66,2.2.2.2,27.23.157.1,22,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,48|128|1|65535|1260|0|1010,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',800000,96,96,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000004
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000004'
sampleRecord = '10,23,3000000004,700000,700000,1.1.1.1,27.2.248.155,gmail.google.com,text/html,gmail.google.com,11,,60,1,2,Sushfone-2,,01216400-0100-66,GET,406 Not Acceptable,"""Mozilla/5.0 (iPad; U; CPU iPhone OS 4_2 like Mac OS X; en_us) AppleWebKit/525.18.1 (KHTML, like Gecko)"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',700000,94,94,'No','','0','01216400-0100-66')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000004
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000004'
sampleRecord = '10,23,3000000004,70000,29,700000,700000,182,36,FaceBook,27.9.126.155,2,1,FromMobile,,0,01216400-0100-66,2.2.2.2,27.23.157.2,23,10,Sushfone-2,231-10-1073-10065,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',700000,94,94,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000005
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000005'
sampleRecord = '10,24,3000000005,600000,600000,1.1.1.1,27.2.248.155,img.youtube.com,application/x-shockwave-flash,img.youtube.com,11,,60,1,1,Sushfone-1,,,GET,409 Conflict,"""Mozilla/5.0 (Linux; U; Android 2.3.4; es-es; HTC_Sensation-orange-LS Build/GRJ22) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',600000,92,92,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000005
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000005'
sampleRecord = '10,24,3000000005,70000,29,600000,600000,182,36,facebook,27.9.126.155,1,1,FromMobile,,1,,2.2.2.1,27.23.157.1,24,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',600000,92,92,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000006
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000006'
sampleRecord = '10,25,3000000006,500000,500000,1.1.1.1,27.2.248.155,nflx.i.4257506b.x.lcdn.nflximg.com,application/x-javascript,nflx.i.4257506b.x.lcdn.nflximg.com,11,,60,1,2,Sushfone-2,,,GET,411a long,"""MOT-DROID2/Blur_Version.2.2.20.A955.Verizon.en.US Mozilla/5.0 (Linux; U; Android 2.2; en-us; DROID2 Build/VZW) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',500000,90,90,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000006
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000006'
sampleRecord = '10,25,3000000006,70000,29,500000,500000,182,36,AppleJuice,27.9.126.155,2,1,FromMobile,,0,,2.2.2.1,27.23.157.2,25,10,Sushfone-2,231-10-1073-10065,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',500000,90,90,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000007
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000007'
sampleRecord = '10,26,3000000007,400000,400000,1.1.1.1,27.2.248.155,hurricanesports.cstv.com,application/octet-stream,hurricanesports.cstv.com,11,,60,1,1,Sushfone-1,,,GET,413 Request Entity Too Large,"""Mozilla/5.0 (Linux; U; Android 4.0; SCH-I535 4G Build/ IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',400000,88,88,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000007
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000007'
sampleRecord = '10,26,3000000007,70000,29,400000,400000,182,36,bItToRrEnT,27.9.126.155,1,1,FromMobile,,1,,2.2.2.2,27.23.157.1,26,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',400000,88,88,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000008
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000008'
sampleRecord = '10,27,3000000008,300000,300000,1.1.1.1,27.2.248.155,feeds.foxsports.com,image/png,feeds.foxsports.com,11,,60,1,2,Sushfone-2,48|128|1|65535|1260|0|3010,35397605-0201-65,GET,416 Requested Range Not Satisfiable,"""Mozilla/5.0 (Linux; U; Android 4.0; SCH-I535 4G Build/ IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',300000,86,86,'Yes','48|128|1|65535|1260|0|3010','0','35397605-0201-65')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000008
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000008'
sampleRecord = '10,27,3000000008,70000,29,300000,300000,182,36,ciTrix,27.9.126.155,2,1,FromMobile,,0,35397605-0201-65,2.2.2.2,27.23.157.2,27,10,Sushfone-2,231-10-1073-10065,43769,1985,rb31,48|128|1|65535|1260|0|3010,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',300000,86,86,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000009
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000009'
sampleRecord = '10,28,3000000009,200000,200000,1.1.1.1,27.2.248.155,htc.accuweather.com,application/json,htc.accuweather.com,11,,60,1,1,Sushfone-1,,,GET,418 Im a teapot,"""Dalvik/1.4.0 (Linux; U; Android 2.3; HTC Sensation 4G Build/GRI40)"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',200000,84,84,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000009
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000009'
sampleRecord = '10,28,3000000009,70000,29,200000,200000,182,36,crossfire,27.9.126.155,1,1,FromMobile,,1,,2.2.2.1,27.23.157.1,28,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',200000,84,84,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000010
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000010'
sampleRecord = '10,29,3000000010,100000,100000,1.1.1.1,27.2.248.155,wxdata.weather.com,text/plain,wxdata.weather.com,11,,60,1,2,Sushfone-2,,,GET,420 Method Failure,"""Dalvik/1.2.0 (Linux; U; Android 2.2; DROID2 GLOBAL Build/S273)"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',100000,82,82,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000010
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000010'
sampleRecord = '10,29,3000000010,70000,29,100000,100000,182,36,ClubPenguiN,27.9.126.155,2,1,FromMobile,,0,,2.2.2.1,27.23.157.2,29,10,Sushfone-2,231-10-1073-10065,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',100000,82,82,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000011
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000011'
sampleRecord = '10,30,3000000011,55000,55000,1.1.1.1,27.2.248.155,wxdata.weather.com,text/html,wxdata.weather.com,11,,60,1,1,Sushfone-1,,,GET,424 Failed Dependency,"""Dalvik/1.2.0 (Linux; U; Android 2.2; DROID2 GLOBAL Build/S273)"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',55000,80,80,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000011
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000011'
sampleRecord = '10,30,3000000011,70000,29,55000,55000,182,36,Citrix,27.9.126.155,1,1,FromMobile,,1,,2.2.2.2,27.23.157.1,30,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',55000,80,80,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000012
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000012'
sampleRecord = '10,31,3000000012,50000,50000,1.1.1.1,27.2.248.155,assets.tumblr.com,text/css,assets.tumblr.com,11,,60,1,2,Sushfone-2,,,GET,425 Unordered Collection,"""Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Mobile/7A341,Apple"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',50000,78,78,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000012
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000012'
sampleRecord = '10,31,3000000012,70000,29,50000,50000,182,36,dofus,27.9.126.155,2,1,FromMobile,,0,,2.2.2.2,27.23.157.2,31,10,Sushfone-2,231-10-1073-10065,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',50000,78,78,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000013
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000013'
sampleRecord = '10,32,3000000013,45000,45000,1.1.1.1,27.2.248.155,img.mocospace.com.edgesuite.net,application/javascript,img.mocospace.com.edgesuite.net,11,,60,1,1,Sushfone-1,,35652104-0201-65,GET,428 Precondition Required,"""MOT-GATW_/00.62 UP.Browser/6.2.3.4.c.1.106 (GUI) MMP/2.0"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',45000,76,76,'No','','1','35652104-0201-65')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000013
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000013'
sampleRecord = '10,32,3000000013,70000,29,45000,45000,182,36,gamekit,27.9.126.155,1,1,FromMobile,,1,35652104-0201-65,2.2.2.1,27.23.157.1,32,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',45000,76,76,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000014
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000014'
sampleRecord = '10,33,3000000014,40000,40000,1.1.1.1,27.2.248.155,www.adobe.com,image/png,www.adobe.com,11,,60,1,2,Sushfone-2,,,GET,449 Retry With,"""Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; DROID RAZR 4G Build/6.5.1-73_DHD-11_M1-29) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',40000,74,74,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000014
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000014'
sampleRecord = '10,33,3000000014,70000,29,40000,40000,182,36,funshion,27.9.126.155,2,1,FromMobile,,0,,2.2.2.1,27.23.157.2,33,10,Sushfone-2,231-10-1073-10065,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',40000,74,74,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000015
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000015'
sampleRecord = '10,34,3000000015,35000,35000,1.1.1.1,27.2.248.155,tuner.pandora.com,audio/mpeg,tuner.pandora.com,11,,60,1,1,Sushfone-1,48|128|1|65535|1260|0|2010,35375004-0101-65,GET,494 Request Header Too Large,"""BlackBerry9650/5.0.0.345 Profile/MIDP-2.1 Configuration/CLDC-1.1 VendorID/105"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',35000,72,72,'Yes','48|128|1|65535|1260|0|2010','1','35375004-0101-65')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000015
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000015'
sampleRecord = '10,34,3000000015,70000,29,35000,35000,182,36,facetime,27.9.126.155,1,1,FromMobile,,1,35375004-0101-65,2.2.2.2,27.23.157.1,34,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,48|128|1|65535|1260|0|2010,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',35000,72,72,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000016
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000016'
sampleRecord = '10,35,3000000016,30000,30000,1.1.1.1,27.2.248.155,vision.youtube.com,video/x-flv,vision.youtube.com,11,,60,1,2,Sushfone-2,,,GET,496 No Cert,"""Mozilla/5.0 (BlackBerry; U; BlackBerry 9650; en-US) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.280 Mobile Safari/534.1+"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',30000,70,70,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000016
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000016'
sampleRecord = '10,35,3000000016,70000,29,30000,30000,182,36,feidian,27.9.126.155,2,1,FromMobile,,0,,2.2.2.2,27.23.157.2,35,10,Sushfone-2,231-10-1073-10065,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',30000,70,70,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000017
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000017'
sampleRecord = '10,36,3000000017,25000,25000,1.1.1.1,27.2.248.155,30for30.espn.com,video/x-flv,30for30.espn.com,11,,60,1,1,Sushfone-1,,,GET,500 Internal Server Error,"""Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',25000,68,68,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000017
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000017'
sampleRecord = '10,36,3000000017,70000,29,25000,25000,182,36,gtalk,27.9.126.155,1,1,FromMobile,unclassified,1,,2.2.2.1,27.23.157.1,36,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',25000,68,68,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000018
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000018'
sampleRecord = '10,37,3000000018,20000,20000,1.1.1.1,27.2.248.155,royals.mlb.com,video/mp4,royals.mlb.com,11,,60,1,2,Sushfone-2,,,GET,504 Gateway Timeout,"""Mozilla/5.0 (Linux; U; Android 2.2.1; en-us; pcdadr6350 Build/FRG83) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',20000,66,66,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000018
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000018'
sampleRecord = '10,37,3000000018,70000,29,20000,20000,182,36,iax,27.9.126.155,2,1,FromMobile,,0,,2.2.2.1,27.23.157.2,37,10,Sushfone-2,231-10-1073-10065,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',20000,66,66,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000019
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000019'
sampleRecord = '10,38,3000000019,15000,15000,1.1.1.1,27.2.248.155,images.craigslist.org,image/png,images.craigslist.org,11,,60,1,1,Sushfone-1,,,GET,506 Variant Also Negotiates,"""Dalvik/1.6.0 (Linux; U; Android 4.0.3; Galaxy Nexus Build/ICL53F)"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',15000,64,64,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000019
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000019'
sampleRecord = '10,38,3000000019,70000,29,15000,15000,182,36,gadugadu,27.9.126.155,1,1,FromMobile,,1,,2.2.2.2,27.23.157.1,38,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',15000,64,64,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000020
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000020'
sampleRecord = '10,39,3000000020,10000,10000,1.1.1.1,27.2.248.155,thumbs2.ebaystatic.com,image/jpeg,thumbs2.ebaystatic.com,11,,60,1,2,Sushfone-2,,,GET,509 Bandwidth Limit Exceeded,"""Dalvik/1.2.0 (Linux; U; Android 2.2; ADR6350 Build/FRG83D)"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',10000,62,62,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000020
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000020'
sampleRecord = '10,39,3000000020,70000,29,10000,10000,182,36,gmail,27.9.126.155,2,1,FromMobile,,0,,2.2.2.2,27.23.157.2,39,10,Sushfone-2,231-10-1073-10065,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',10000,62,62,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000021
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000021'
sampleRecord = '10,40,3000000021,8000,8000,1.1.1.1,27.2.248.155,profile.ak.fbcdn.net,image/gif,profile.ak.fbcdn.net,11,,60,1,1,Sushfone-1,,,GET,305 Use Proxy,"""BlackBerry9330/5.0.0.782 Profile/MIDP-2.1 Configuration/CLDC-1.1 VendorID/105"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',8000,60,60,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000021
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000021'
sampleRecord = '10,40,3000000021,70000,29,8000,8000,182,36,imo,27.9.126.155,1,1,FromMobile,,1,,2.2.2.1,27.23.157.1,40,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',8000,60,60,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000022
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000022'
sampleRecord = '10,41,3000000022,7500,7500,1.1.1.1,27.2.248.155,pics.plentyoffish.com,image/gif,pics.plentyoffish.com,11,,60,1,2,Sushfone-2,,,GET,400 Bad Request,"""Mozilla/5.0 (BlackBerry; U; BlackBerry 9330; en-US) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.280 Mobile Safari/534.1+"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',7500,58,58,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000022
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000022'
sampleRecord = '10,41,3000000022,70000,29,7500,7500,182,36,jabber,27.9.126.155,2,1,FromMobile,,0,,2.2.2.1,27.23.157.2,41,10,Sushfone-2,231-10-1073-10065,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',7500,58,58,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000023
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000023'
sampleRecord = '10,42,3000000023,7000,7000,1.1.1.1,27.2.248.155,playerservices.streamtheworld.com,image/png,playerservices.streamtheworld.com,11,,60,1,1,Sushfone-1,,,GET,402 Payment Required,"""Mozilla/5.0 (Linux; U; Android 2.1-update1; en-us; SCH-I400 Build/ECLAIR) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',7000,56,56,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000023
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000023'
sampleRecord = '10,42,3000000023,70000,29,7000,7000,182,36,nimbuzz,27.9.126.155,1,1,FromMobile,,1,,2.2.2.2,27.23.157.1,42,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',7000,56,56,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000024
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000024'
sampleRecord = '10,43,3000000024,6500,6500,1.1.1.1,27.2.248.155,worldstarhiphop.com,application/xml,worldstarhiphop.com,11,,60,1,2,Sushfone-2,,,GET,406 Not Acceptable,"""Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; SCH-I510 4G Build/FP1) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',6500,54,54,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000024
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000024'
sampleRecord = '10,43,3000000024,70000,29,6500,6500,182,36,msn,27.9.126.155,2,1,FromMobile,video,0,,2.2.2.2,27.23.157.2,43,10,Sushfone-2,231-10-1073-10065,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',6500,54,54,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000025
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000025'
sampleRecord = '10,44,3000000025,6000,6000,1.1.1.1,27.2.248.155,profootballtalk.nbcsports.com,text/html,profootballtalk.nbcsports.com,11,,60,1,1,Sushfone-1,,,GET,409 Conflict,"""Mozilla/5.0 (Linux; U; Android 2.1; en-us; ADR6300 Build/ERD79) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',6000,52,52,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000025
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000025'
sampleRecord = '10,44,3000000025,70000,29,6000,6000,182,36,skype,27.9.126.155,1,1,FromMobile,,1,,2.2.2.1,27.23.157.1,44,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',6000,52,52,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000026
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000026'
sampleRecord = '10,45,3000000026,5500,5500,1.1.1.1,27.2.248.155,cbssports.nfl.com,application/x-shockwave-flash,cbssports.nfl.com,11,,60,1,2,Sushfone-2,,,GET,411a long,"""Mozilla/5.0 (Linux; U; Android 2.2.1; en-us; ADR6400L 4G Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',5500,50,50,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000026
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000026'
sampleRecord = '10,45,3000000026,70000,29,5500,5500,182,36,yahoo,27.9.126.155,2,1,FromMobile,,0,,2.2.2.1,27.23.157.2,45,10,Sushfone-2,231-10-1073-10065,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',5500,50,50,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000027
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000027'
sampleRecord = '10,46,3000000027,5000,5000,1.1.1.1,27.2.248.155,images.craigslist.org,text/html,images.craigslist.org,11,,60,1,1,Sushfone-1,,,GET,413 Request Entity Too Large,"""Mozilla/5.0 (Linux; U; Android 2.2.1; en-us; ADR6400L Build/FRG83D) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',5000,48,48,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000027
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000027'
sampleRecord = '10,46,3000000027,21,,5000,5000,182,36,,27.9.126.155,1,1,FromMobile,,1,,2.2.2.2,27.23.157.1,46,10,Sushfone-1,231-10-1073-10064,43769,17,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',5000,48,48,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000028
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000028'
sampleRecord = '10,47,3000000028,4500,4500,1.1.1.1,27.2.248.155,simg.zedo.com,image/gif,simg.zedo.com,11,,60,1,2,Sushfone-2,,,GET,416 Requested Range Not Satisfiable,"""Mozilla/5.0 (iPod; U; CPU like Mac OS X; pl-pl) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',4500,46,46,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000028
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000028'
sampleRecord = '10,47,3000000028,21,7,4500,4500,182,36,,27.9.126.155,2,1,FromMobile,,0,,2.2.2.2,27.23.157.2,47,10,Sushfone-2,231-10-1073-10065,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',4500,46,46,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000029
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000029'
sampleRecord = '10,48,3000000029,4000,4000,1.1.1.1,27.2.248.155,premium.bangyoulater.com,application/json,premium.bangyoulater.com,11,,60,1,1,Sushfone-1,,,GET,418 Im a teapot,"""Mozilla/5.0 (iPod; U; CPU iPhone OS 3_1_2 like Mac OS X; en-us) AppleWebKit/525.18.1 (KHTML, like Gecko)"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',4000,44,44,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000029
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000029'
sampleRecord = '10,48,3000000029,53,,4000,4000,182,36,,27.9.126.155,1,1,FromMobile,,1,,2.2.2.1,27.23.157.1,48,10,Sushfone-1,231-10-1073-10064,43769,17,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',4000,44,44,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000030
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000030'
sampleRecord = '10,49,3000000030,3500,3500,1.1.1.1,27.2.248.155,img2.cliphunter.com,application/json,img2.cliphunter.com,11,,60,1,2,Sushfone-2,,,GET,420 Method Failure,"""Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; SCH-I405 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',3500,42,42,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000030
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000030'
sampleRecord = '10,49,3000000030,25,160,3500,3500,182,36,,27.9.126.155,2,1,ToMobile,,0,,2.2.2.1,27.23.157.2,49,10,Sushfone-2,231-10-1073-10065,110,6,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',3500,42,42,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000031
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000031'
sampleRecord = '10,50,3000000031,3000,3000,1.1.1.1,27.2.248.155,games.crossfit.com,application/json,games.crossfit.com,11,,60,1,1,Sushfone-1,,,GET,424 Failed Dependency,"""Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; SCH-I405 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',3000,40,40,'No','','11','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000031
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000031'
sampleRecord = '10,50,3000000031,5060,17,3000,3000,182,36,,27.9.126.155,1,1,FromMobile,,11,,2.2.2.2,27.23.157.1,50,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',3000,40,40,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000032
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000032'
sampleRecord = '10,51,3000000032,2500,2500,1.1.1.1,27.2.248.155,reviews.walgreens.com,application/javascript,reviews.walgreens.com,11,,60,1,2,Sushfone-2,,,GET,425 Unordered Collection,"""Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; DROID3 Build/5.5.1_84_D3G-55) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',2500,38,38,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000032
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000032'
sampleRecord = '10,51,3000000032,70000,18,2500,2500,182,36,,27.9.126.155,2,1,FromMobile,,0,,2.2.2.2,27.23.157.2,51,10,Sushfone-2,231-10-1073-10065,43769,17,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',2500,38,38,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000033
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000033'
sampleRecord = '10,52,3000000033,2000,2000,1.1.1.1,27.2.248.155,google.com,text/javascript,google.com,11,,60,1,1,Sushfone-1,,,GET,428 Precondition Required,"""GoogleAnalytics/1.1 (Linux; U; Android 2.2.1; en-us; SCH-I400; Build/FROYO)"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',2000,36,36,'No','','11','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000033
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000033'
sampleRecord = '10,52,3000000033,25,190,2000,2000,182,36,,27.9.126.155,1,1,FromMobile,,11,,2.2.2.1,27.23.157.1,52,10,Sushfone-1,231-10-1073-10064,143,6,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',2000,36,36,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000034
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000034'
sampleRecord = '10,53,3000000034,1500,1500,1.1.1.1,27.2.248.155,books.google.com,text/html,books.google.com,11,,60,1,2,Sushfone-2,,,GET,449 Retry With,"""Dalvik/1.4.0 (Linux; U; Android 2.3; SCH-I510 Build/GINGERBREAD)"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',1500,34,34,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000034
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000034'
sampleRecord = '10,53,3000000034,70000,20,1500,1500,182,36,,27.9.126.155,2,1,FromMobile,,0,,2.2.2.1,27.23.157.2,53,10,Sushfone-2,231-10-1073-10065,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',1500,34,34,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000035
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000035'
sampleRecord = '10,54,3000000035,1000,1000,1.1.1.1,27.2.248.155,youtube.com,image/png,youtube.com,11,,60,1,1,Sushfone-1,,,GET,494 Request Header Too Large,GoogleAnalytics/1.1 (Linux; U; Android 2.2.1; en-us; SCH-I400; Build/FROYO)'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',1000,32,32,'No','','11','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000035
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000035'
sampleRecord = '10,54,3000000035,70000,21,1000,1000,182,36,,27.9.126.155,1,1,FromMobile,,11,,2.2.2.2,27.23.157.1,54,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',1000,32,32,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000036
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000036'
sampleRecord = '10,55,3000000036,700,700,1.1.1.1,27.2.248.155,www.facebook.com,image/png,www.facebook.com,11,,60,1,2,Sushfone-2,,,GET,496 No Cert,"""Mozilla/5.0 (Linux; U; Android 2.2; en-us; Vortex Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',700,30,30,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000036
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000036'
sampleRecord = '10,55,3000000036,70000,38,700,700,182,36,,27.9.126.155,2,1,FromMobile,,0,,2.2.2.2,27.23.157.2,55,10,Sushfone-2,231-10-1073-10065,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',700,30,30,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000037
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000037'
sampleRecord = '10,56,3000000037,650,650,1.1.1.1,27.2.248.155,openwave.mocospace.com,application/x-shockwave-flash,openwave.mocospace.com,11,,60,1,1,Sushfone-1,,,GET,500 Internal Server Error,"""Mozilla/5.0 (Macintosh; Intel Mac OS X 10.5; rv:10.0) Gecko/20100101 Firefox/10.0"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',650,28,28,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000037
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000037'
sampleRecord = '10,56,3000000037,70000,22,650,650,182,36,,27.9.126.155,1,1,FromMobile,,1,,2.2.2.1,27.23.157.1,56,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',650,28,28,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000038
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000038'
sampleRecord = '10,57,3000000038,600,600,1.1.1.1,27.2.248.155,espn.go.com,video/mp4,espn.go.com,11,,60,1,2,Sushfone-2,,,GET,504 Gateway Timeout,"""Mozilla/5.0 (Linux; U; Android 2.1-update1; en-us; SCH-I500 Build/ECLAIR) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',600,26,26,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000038
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000038'
sampleRecord = '10,57,3000000038,20,,600,600,182,36,,27.9.126.155,2,1,FromMobile,,0,,2.2.2.1,27.23.157.2,57,10,Sushfone-2,231-10-1073-10065,43769,17,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',600,26,26,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000039
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000039'
sampleRecord = '10,58,3000000039,550,550,1.1.1.1,27.2.248.155,play.rhapsody.com,application/octet-stream,play.rhapsody.com,11,,60,1,1,Sushfone-1,,,GET,,"""Mozilla/5.0 (Linux; U; Android 2.1-update1; en-us; Ally Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',550,24,24,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000039
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000039'
sampleRecord = '10,58,3000000039,23,,550,550,182,36,,27.9.126.155,1,1,FromMobile,,1,,2.2.2.2,27.23.157.1,58,10,Sushfone-1,231-10-1073-10064,43769,17,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',550,24,24,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000040
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000040'
sampleRecord = '10,59,3000000040,500,500,1.1.1.1,27.2.248.155,www.perfectgirls.net,application/vnd.wap.mms-message,www.perfectgirls.net,11,,60,1,2,Sushfone-2,,,GET,,"""Mozilla/5.0 (Linux; U; Android 2.1-update1; en-us; Ally Build/ERE27) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',500,22,22,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000040
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000040'
sampleRecord = '10,59,3000000040,148,,500,500,182,36,,27.9.126.155,2,1,FromMobile,,0,,2.2.2.2,27.23.157.2,59,10,Sushfone-2,231-10-1073-10065,43769,17,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',500,22,22,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000041
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000041'
sampleRecord = '10,60,3000000041,450,450,1.1.1.1,27.2.248.155,cdns.xtube.com,application/vnd.wap.mms-message,cdns.xtube.com,11,,60,1,1,Sushfone-1,,,GET,,"""Mozilla/4.0 (compatible; MSIE 7.0; Windows Phone OS 7.0; Trident/3.1; IEMobile/7.0; HTC; mwp6985)"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',450,20,20,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000041
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000041'
sampleRecord = '10,60,3000000041,148,,450,450,182,36,,27.9.126.155,1,1,FromMobile,,1,,2.2.2.1,27.23.157.1,60,10,Sushfone-1,231-10-1073-10064,43769,6,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',450,20,20,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000042
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000042'
sampleRecord = '10,61,3000000042,400,400,1.1.1.1,27.2.248.155,allrecipes.com,image/png,allrecipes.com,11,,60,1,2,Sushfone-2,,,GET,,"""Mozilla/5.0 (Linux; U; Android 2.2; en-us; Vortex Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',400,18,18,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000042
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000042'
sampleRecord = '10,61,3000000042,218,,400,400,182,36,,27.9.126.155,2,1,FromMobile,,0,,2.2.2.1,27.23.157.2,61,10,Sushfone-2,231-10-1073-10065,43769,17,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',400,18,18,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000043
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000043'
sampleRecord = '10,62,3000000043,350,350,1.1.1.1,27.2.248.155,assets.bodybuilding.com,text/html,assets.bodybuilding.com,11,,60,1,1,Sushfone-1,,,GET,,"""Mozilla/5.0 (Linux; U; Android 2.2; en-us; Vortex Build/FRF91) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',350,16,16,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000043
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000043'
sampleRecord = '10,62,3000000043,218,,350,350,182,36,,27.9.126.155,1,1,FromMobile,,1,,2.2.2.2,27.23.157.1,62,10,Sushfone-1,231-10-1073-10064,43769,6,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',350,16,16,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000044
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000044'
sampleRecord = '10,63,3000000044,300,300,1.1.1.1,27.2.248.155,wiki.answers.com,text/plain,wiki.answers.com,11,,60,1,2,Sushfone-2,,,GET,,"""Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; SCH-I110 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',300,14,14,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000044
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000044'
sampleRecord = '10,63,3000000044,265,,300,300,182,36,,27.9.126.155,2,1,FromMobile,,0,,2.2.2.2,27.23.157.2,63,10,Sushfone-2,231-10-1073-10065,43769,6,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',300,14,14,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000045
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000045'
sampleRecord = '10,64,3000000045,250,250,1.1.1.1,27.2.248.155,flashcards.dictionary.com,text/plain,flashcards.dictionary.com,11,,60,1,1,Sushfone-1,,,GET,,"""Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; LG-VS700 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',250,12,12,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000045
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000045'
sampleRecord = '10,64,3000000045,360,,250,250,182,36,,27.9.126.155,1,1,FromMobile,,1,,2.2.2.1,27.23.157.1,64,10,Sushfone-1,231-10-1073-10064,43769,6,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',250,12,12,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000046
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000046'
sampleRecord = '10,65,3000000046,200,200,1.1.1.1,27.2.248.155,google.com,application/json,google.com,11,,60,1,2,Sushfone-2,,,GET,,GoogleAnalytics/1.1 (Linux; U; Android 2.2.1; en-us; SCH-I400; Build/FROYO)'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',200,10,10,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000046
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000046'
sampleRecord = '10,65,3000000046,360,,200,200,182,36,,27.9.126.155,2,1,FromMobile,,0,,2.2.2.1,27.23.157.2,65,10,Sushfone-2,231-10-1073-10065,43769,100,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',200,10,10,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000047
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000047'
sampleRecord = '10,66,3000000047,150,150,1.1.1.1,27.2.248.155,microsoft.com,application/x-javascript,microsoft.com,11,,60,1,1,Sushfone-1,,,GET,,Microsoft BITS/7.5'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',150,8,8,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000047
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000047'
sampleRecord = '10,66,3000000047,1599,,150,150,182,36,,27.9.126.155,1,1,FromMobile,,1,,2.2.2.2,27.23.157.1,66,10,Sushfone-1,231-10-1073-10064,43769,1981,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',150,8,8,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000048
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000048'
sampleRecord = '10,67,3000000048,100,100,1.1.1.1,27.2.248.155,photos-f.ak.fbcdn.net,image/png,photos-f.ak.fbcdn.net,11,,60,1,2,Sushfone-2,,,GET,,Dalvik/1.1.0 (Linux; U; Android 2.1; SCH-I500 Build/ECLAIR)'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',100,6,6,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000048
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000048'
sampleRecord = '10,67,3000000048,1599,,100,100,182,36,,27.9.126.155,2,1,FromMobile,,0,,2.2.2.2,27.23.157.2,67,10,Sushfone-2,231-10-1073-10065,43769,,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',100,6,6,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000049
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000049'
sampleRecord = '10,68,3000000049,50,50,1.1.1.1,27.2.248.155,photos-f.ak.fbcdn.net,image/png,photos-f.ak.fbcdn.net,11,,60,1,1,Sushfone-1,,98005800-120371-03,GET,,Dalvik/1.1.0 (Linux; U; Android 2.1; SCH-I500 Build/ECLAIR)'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',50,4,4,'No','','1','98005800-120371-03')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000049
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000049'
sampleRecord = '10,68,3000000049,5060,,50,50,182,36,,27.9.126.155,1,1,Unknown,,1,,2.2.2.2,27.23.157.1,68,10,Sushfone-1,231-10-1073-10064,5060,6,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',50,4,4,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000050
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000050'
sampleRecord = '10,69,3000000050,75,75,1.1.1.1,27.2.248.155,wap.cellufun.com,application/vnd.wap.mms-message,wap.cellufun.com,11,,60,1,2,Sushfone-2,,35375004-120371-03,GET,,"Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; SCH-I800 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',75,29,29,'No','','0','35375004-120371-03')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000050
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000050'
sampleRecord = '10,69,3000000050,65534,33,75,75,182,36,,27.9.126.155,2,1,FromMobile,,0,35375004-120371-03,2.2.2.1,27.23.157.2,69,10,Sushfone-2,231-10-1073-10065,43769,1981,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',75,29,29,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000051
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000051'
sampleRecord = '10,70,3000000051,55,55,1.1.1.1,27.2.248.155,wap.cellufun.com,text/css,wap.cellufun.com,11,,60,1,1,Sushfone-1,,,GET,,'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',55,3,3,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000051
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000051'
sampleRecord = '10,70,3000000051,65534,33,55,55,182,36,,27.9.126.155,1,1,FromMobile,,1,35375004-120371-03,2.2.2.1,27.23.157.1,70,10,Sushfone-1,231-10-1073-10064,43769,1981,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',55,3,3,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000052
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000052'
sampleRecord = '10,71,3000000052,20,20,1.1.1.1,27.2.248.155,roamware.com,application/binary,roamware.com,11,,60,1,2,Sushfone-2,,,GET,426 Upgrade Required,Mozilla/4.0 (compatible; MSIE 7.0; Windows Phone OS 7.0; Trident/3.1; IEMobile/7.0; HTC; 7 Mozart)'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',20,3,3,'No','','0','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000052
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000052'
sampleRecord = '10,71,3000000052,65534,33,20,20,182,36,,27.9.126.155,2,1,FromMobile,,0,,2.2.2.2,27.23.157.2,71,10,Sushfone-2,231-10-1073-10065,43769,1981,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',20,1,1,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000053
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000053'
sampleRecord = '10,72,3000000053,15,15,1.1.1.1,27.2.248.155,sumologic.com,application/vnd.android.package-archive,sumologic.com,11,,60,1,1,Sushfone-1,,,GET,431 Request Header Fields Too Large,"Mozilla/5.0 (Linux; U; Android 2.2.2; en-us; DROID X2 Build/4.4.1_274_DTN-14.8) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',15,2,2,'No','','1','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000053
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000053'
sampleRecord = '10,72,3000000053,65534,33,30,30,182,36,,27.9.126.155,1,1,FromMobile,,1,,2.2.2.2,27.23.157.1,72,10,Sushfone-1,231-10-1073-10064,43769,1981,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',30,2,2,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000054
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000054'
sampleRecord = '10,73,3000000054,155,155,1.1.1.1,27.2.248.155,yatraABCD.com,application/vnd.android.package-archive,yatraABCD.com,11,,60,1,1,Sushfone-1,,2222222222-120348-71,GET,,'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',155,3,3,'No','','0','2222222222-120348-71')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000054
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000054'
sampleRecord = '10,73,3000000054,65534,33,155,155,182,36,,27.9.126.155,1,1,FromMobile,,0,,2.2.2.1,27.23.157.2,73,10,Sushfone-2,231-10-1073-10065,43769,1981,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',155,3,3,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000055
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000055'
sampleRecord = '10,74,3000000055,255,255,1.1.1.1,27.2.248.155,indiatimesABCD.com,application/vnd.android.package-archive,indiatimesABCD.com,11,,60,1,2,Sushfone-1,,,GET,,Thaalam FM'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',255,2,2,'No','','2','')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000055
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000055'
sampleRecord = '10,74,3000000055,65534,33,255,255,182,36,,27.9.126.155,2,1,FromMobile,,2,,2.2.2.1,27.23.157.1,74,10,Sushfone-2,231-10-1073-10064,43769,1981,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',255,2,2,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000056
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000056'
sampleRecord = '10,34,3000000056,35000,35000,1.1.1.1,27.2.248.155,asfhj.dfdfkh36.com,audio/mpeg,asfhj.dfdfkh36.com,11,,60,1,1,Sushfone-1,48|128|1|65535|1260|0|2010,35412601-0101-65,GET,501 Not Implemented,Mozilla/4.0 (ABC DEF)'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',35000,31,31,'Yes','48|128|1|65535|1260|0|2010','0','35412601-0101-65')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000056
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000056'
sampleRecord = '10,34,3000000056,70000,29,35000,35000,182,36,facetime,27.9.126.155,1,1,FromMobile,,0,35412601-0101-65,2.2.2.2,27.23.157.1,34,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,48|128|1|65535|1260|0|2010,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',35000,31,31,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000057
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000057'
sampleRecord = '10,32,3000000057,45000,45000,1.1.1.1,27.2.248.155,asfhj.dfdfkh37.com,text/html,asfhj.dfdfkh37.com,11,,60,1,1,Sushfone-1,,01161700-0201-65,GET,505 HTTP Version Not Supported,"""ABC DEF 1774133"""'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',45000,25,25,'No','','1','01161700-0201-65')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000057
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000057'
sampleRecord = '10,32,3000000057,70000,29,45000,45000,182,36,gamekit,27.9.126.155,1,1,FromMobile,,1,01161700-0201-65,2.2.2.1,27.23.157.1,32,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',45000,25,25,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################

#Http
#User: 3000000058
#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-request method,http-reply code,http-user-agent
subcrid = '3000000058'
sampleRecord = '10,32,3000000058,45000,45000,1.1.1.1,27.2.248.155,asfhj.dfdfkh37.com,text/html,asfhj.dfdfkh37.com,11,,60,1,1,Sushfone-1,48|128|1|65535|1260|0|4010,35620604-0401-65,GET,507 Insufficient Storage,Android-GData-Calendar/1.4 (cdma_droid2 VZW); gzip'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei) = ('http',45000,15,15,'Yes','48|128|1|65535|1260|0|4010','0','35620604-0401-65')
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tcp_os_present_in_flow_after_aggregation, tcp_os_signature, tethered, bearer_3gpp_imei)]
##################################################################################################################################

#Flow
#User: 3000000058
#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,tethered,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
subcrid = '3000000058'
sampleRecord = '10,32,3000000058,70000,29,45000,45000,182,36,gamekit,27.9.126.155,1,1,FromMobile,,0,35620604-0401-65,2.2.2.1,27.23.157.1,32,10,Sushfone-1,231-10-1073-10064,43769,1985,rb31,48|128|1|65535|1260|0|4010,2'
(recordType, usageType, nOfRecordsLL, nOfRecordsHL,tcp_os_present_in_flow_after_aggregation, tcp_os_signature) = ('flow',45000,15,15,None,None)
recordInfoList += [(subcrid, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, None, None, None, None)]
##################################################################################################################################





################################ Generate Records ###################################################################
Generator(strStartTime, strEndTime, recordInfoList, flowFileFormat, httpFileFormat, gzipOn, server_ip, server_username, server_http_directory, server_flow_directory,dateformat)
#####################################################################################################################

