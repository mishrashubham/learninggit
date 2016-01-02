"""
    @package  Tethering Data Generator
    @copyright    2006-2012, GUAVUS Inc.
    @version      GIT: $Id: TMEGenerator.py,v 1.0 2013/03/07 10:00:00
    @author: Rahul bagai
    
    @internal Revisions:
    """

import time
class Time:
    ''' Access to all time related functions and their conversions. '''
    def getIntCurrTime(self):
        ''' Get the current time in Integer format. (in UTC)'''
        tupleCurrTime = time.gmtime()
        intCurrTime = int(time.mktime(tupleCurrTime))
        return intCurrTime
    
    def getStrCurrTime(self):
        ''' Get the current time in String format. (in UTC)'''
        ''' Format: June 07 00:00:00 2012 '''
        return time.strftime("%B %d %H:%M:%S %Y", time.gmtime())
    
    def getIntTimeOffset(self, intTime, offset):
        ''' Get the offset on Int time passed on to this function, and returned the time in Int.
            
            Input::
            intTime :: time passed in Integer format.
            offset :: Integer value (+ve or -ve in seconds) with which the time passed is to be offset.
            
            Output::
            Return the offsetted time in integer format.
            '''
        return intTime + offset
    
    def getStringTimeOffset(self, strTime, offset):
        ''' Get the Offset on String time passed on to this function, and return time time in String.
            
            Input::
            strTime :: time passed in String format. (Format: June 07 00:00:00 2012)
            offset :: Integer value (+ve or -ve in seconds) with which the time passed is to be offset.
            
            Output::
            Return the offsetted time in String format.
            '''
        tupleTime = time.strptime(strTime, "%B %d %H:%M:%S %Y")
        intTime = int(time.mktime(tupleTime))
        offsetIntTime = intTime + offset
        tupleOffsetTime = time.localtime(offsetIntTime)
        strOffsetTime = time.strftime("%B %d %H:%M:%S %Y",tupleOffsetTime)
        
        return strOffsetTime
    
    def getIntTime(self, strTime):
        '''
            Convert the string time into integer format.
            '''
        tupleTime = time.strptime(strTime, "%B %d %H:%M:%S %Y")
        intTime = int(time.mktime(tupleTime))
        return intTime
    
    def getTimeInFormat(self, formatt, intTime):
        '''
            This gets the string of time in a defined format as passed by the parameter
            formatt.
            
            Input::
            formatt :: String Format of the date.
            intTime :: integer time which is to be converted to format "formatt"
            
            Output ::
            Return the date in format "formatt"
            '''
        return time.strftime(formatt,time.localtime(intTime))
class FileFormat:
    
    '''
        # File Formats
        # <file-name format of incoming files. Date and time keywords must be configured as below: >
        # %YYYY or %YY    - Year as numeric (eg. 2012 or 12)
        # %Mmm or %MM     - Month as case-insensitive string (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec)
        #           or MM as numeric   (01-12)
        # %DD             - Day as numeric     (01-31)
        # %hh             - Hour as numeric    (00-23)
        # %mm             - Minutes as numeric (00-59)
        # %ss             - Seconds as numeric (00-59)
        # For example : ab.cde_fgh.%YYYY%MM%DD_%hh%mm%ss.RC.txt.gz
        
        Note: Ignore any * or special case characters for regular expression. (Give Only exact file formats with date-time keywords only).
        
        FlowFileFormat = edrFLOW_%Mmm_%DD_%hh_%mm_%ss_%YYYY.csv
        HttpFileFormat = edrHTTP_%Mmm_%DD_%hh_%mm_%ss_%YYYY.csv
        '''
    
    def __init__(self):
        self.t = Time()
        
        # Dictionary that maintains the mapping of date-time formats passed to python specific date-time formats
        # with key as config file date-time format, and value as python specific date-time format
        self.dictTimeConversion = {'%YYYY':'%Y','%YY':'%y', '%Mmm':'%b', '%MM':'%m', '%DD':'%d', '%hh':'%H', '%mm':'%M', '%ss':'%S'}
    
    def getFileFormat(self, fileFormat, intTime):
        '''
            Replace the fileFormat received from Config file to python specific date-time format,
            and then pass it to Time.getTimeInFormat() function to get the desired file name converted
            to its time.
            '''
        
        # Convert the fileFormat into python-specific date-time format.
        for configFormat in self.dictTimeConversion.keys():
            fileFormat = fileFormat.replace(configFormat, self.dictTimeConversion[configFormat], 1)
        
        # Convert the fileFormat in accordance with intTime after Conversion.
        fileFormatAfterConv = self.t.getTimeInFormat(fileFormat, intTime)
    
        return fileFormatAfterConv

import random
class GenerateRecords:
    def __init__(self):
        '''
            This class facilitates generation of Records for a particular user/use-case by recieving
            few input parameters.
            It receives the sample record which constitutes of a particular use-case to cater, with "startTime", "endTime", "usageType" (high/low/medium)
            and generate few records based on "nOfRecords".
            
            Input to GenerateRecords:
            startTime: startTime boundary in integer format (Any random time would be picked b/w startTime & endTime)
            endTime: endTime boundary in integer format (Any random time would be picked b/w startTime & endTime)
            subcrId: radius_calling_station_id
            sampleRecord: Get the sample record and return the desired record
            recordType: http / flow (Http File Record / Http File Record)
            usageType: (high / medium / low) High Tonnage, Medium Tonnage, Low Tonnage
            nOfRecordsLL: No. of records to be generated for this record (Lower Limit)
            nOfRecordsHL: No. of records to be generated for this record (Higher Limit)
            
            #startTime, endTime, subcrId, tonnages could be anything when received in sampleRecord, it would be converted to desired values as provided
            #in input arguments
            
            Format of sample_flow_record:
            #sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
            
            Format of sample_http_record:
            #sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,http-user-agent
            
            
            MemberInstances:
            self.startTime, self.endTime, self.subcrId, self.sampleRecord, self.recordType, self.usageType, self.nOfRecords
            self.sampleFlowHeaderList, self.sampleHttpHeaderList
            self.recordsList == Stores All the records in text separated by '\n'
            HeaderIndexes == self.startTimeIndexInFlowHeader, self.endTimeIndexInFlowHeader, self.subcrIdIndexInFlowHeader, self.upbytesIndexInFlowHeader
            self.downbytesIndexInFlowHeader, self.snflowStartTimeIndexInFlowHeader, self.snflowEndTimeIndexInFlowHeader
            self.startTimeIndexInHttpHeader, self.endTimeIndexInHttpHeader, self.subcrIdIndexInHttpHeader, self.upbytesIndexInHttpHeader, self.downbytesIndexInHttpHeader
            '''
        self.flowHeaderList = 'sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id'.split(',')
        self.httpHeaderList = 'sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,bearer-3gpp imei,http-user-agent'.split(',')
        
        
        # Don't Choose multiplier less than 1/15, because we have tonnages equal to 15. Less than 1/15 like 1/20 or something, will lead to 0 tonnage.
        self.tonnage_multiplier_list = [10, 20, 30, 1.0/10, 1.0/5, 1.0/15, 1]
        self.multiplier = 1
        
        self.flowCount_multiplier_list = [1, 2, 3, 4]
        self.multiplier_flowCount = 1
        
        self.hitDuration_adder_list = [10, 20, 30, 40]
        self.adder_hitDuration = 0
        
        ''' Do Sub-Tasks '''
        self.setIndexes()
    
    def getAggrHttpInfo(self):
        return (self.subcrId, self.tot_downbytes, self.tot_upbytes)
    
    def getRecordList(self):
        return self.recordsList
    
    def setIndexes(self):
        self.startTimeIndexInFlowHeader = self.flowHeaderList.index('sn-start-time')
        self.endTimeIndexInFlowHeader = self.flowHeaderList.index('sn-end-time')
        self.subcrIdIndexInFlowHeader = self.flowHeaderList.index('radius-calling-station-id')
        self.upbytesIndexInFlowHeader = self.flowHeaderList.index('sn-volume-amt-ip-bytes-uplink')
        self.downbytesIndexInFlowHeader = self.flowHeaderList.index('sn-volume-amt-ip-bytes-downlink')
        self.snflowStartTimeIndexInFlowHeader = self.flowHeaderList.index('sn-flow-start-time')
        self.snflowEndTimeIndexInFlowHeader = self.flowHeaderList.index('sn-flow-end-time')
        
        self.startTimeIndexInHttpHeader = self.httpHeaderList.index('sn-start-time')
        self.endTimeIndexInHttpHeader = self.httpHeaderList.index('sn-end-time')
        self.subcrIdIndexInHttpHeader = self.httpHeaderList.index('radius-calling-station-id')
        self.upbytesIndexInHttpHeader = self.httpHeaderList.index('transaction-uplink-bytes')
        self.downbytesIndexInHttpHeader = self.httpHeaderList.index('transaction-downlink-bytes')
    
    def getRandomValue(self, start, end, multiplier = 1 , adder = 0):
        '''Generic function that takes arguments below to generate a random value
            
            Input:::
            start, end :: Provide the range for random value generator
            multiplier :: Multiplier. Default Value = 1
            adder :: Adder. Default Value= 0
            
            Output:::
            Generates random value within the range "start" to "end", multiplied by "multiplier"
            and added to "adder".
            '''
        randomVal = adder + multiplier * random.randint(start, end)
        return randomVal
    
    def generateRecords(self, startTime, endTime, subcrId, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tot_downbytes = None, tot_upbytes = None):
        
        self.subcrId = subcrId
        self.recordsList = list()
        
        finalRecord = ''
        sampleRecordList = sampleRecord.split(',')
        
        # Declare downbytes and upbytes as 0, when it not called for aggregated of http-records. (i.e. it is called for generation of http/flow records)
        if usageType != 'aggr':
            self.tot_downbytes = 0
            self.tot_upbytes = 0
        
        start_time_offset = int (sampleRecordList[self.startTimeIndexInHttpHeader]) + self.adder_hitDuration
        end_time_offset = int (sampleRecordList[self.endTimeIndexInHttpHeader]) + self.adder_hitDuration
        
        nOfRecords = self.multiplier_flowCount * self.getRandomValue(start = nOfRecordsLL, end = nOfRecordsHL)
        for i in xrange(nOfRecords):
            if usageType == 'aggr':
                startTime_t = startTime
                endTime_t = endTime - 1
            else:
                startTime_t = self.getRandomValue(start = startTime, end = endTime-1)
                endTime_t = self.getRandomValue(start = startTime, end = endTime-1)
            
            if recordType == 'flow':
                headerList = self.flowHeaderList
            
            elif recordType == 'http':
                headerList = self.flowHeaderList
            
            else:
                raise Exception('Incorrect RecordType Provided.')
            
            if usageType == 'aggr':
                uplinkBytes =  self.tot_upbytes
                downlinkBytes = self.tot_downbytes
            else:
                uplinkBytes = int(self.multiplier * self.generateRandomValForTonnage(usageType))
                downlinkBytes = int(self.multiplier * self.generateRandomValForTonnage(usageType))
            
            if recordType == 'flow':
                sampleRecordList[self.startTimeIndexInFlowHeader] = str(startTime_t-900)
                sampleRecordList[self.endTimeIndexInFlowHeader] = str(endTime_t-900)
                sampleRecordList[self.startTimeIndexInFlowHeader] = str(startTime + start_time_offset)
                sampleRecordList[self.endTimeIndexInFlowHeader] = str(startTime + end_time_offset)
                sampleRecordList[self.subcrIdIndexInFlowHeader] = str(self.subcrId)
                sampleRecordList[self.upbytesIndexInFlowHeader] = str(uplinkBytes)
                sampleRecordList[self.downbytesIndexInFlowHeader] = str(downlinkBytes)
                sampleRecordList[self.snflowStartTimeIndexInFlowHeader] = str(startTime + start_time_offset)
                sampleRecordList[self.snflowEndTimeIndexInFlowHeader] = str(startTime + end_time_offset)
            elif recordType == 'http':
                sampleRecordList[self.startTimeIndexInHttpHeader] = str(startTime + start_time_offset)
                sampleRecordList[self.endTimeIndexInHttpHeader] = str(startTime + end_time_offset)
                sampleRecordList[self.subcrIdIndexInHttpHeader] = str(self.subcrId)
                sampleRecordList[self.upbytesIndexInHttpHeader] = str(uplinkBytes)
                sampleRecordList[self.downbytesIndexInHttpHeader] = str(downlinkBytes)
                
                self.tot_downbytes += downlinkBytes
                self.tot_upbytes += uplinkBytes
            
            finalRecord = ','.join(sampleRecordList) + '\n'
                    self.recordsList.append(finalRecord)

    def generateRandomValForTonnage(self, usageType):
       return usageType
#if usageType == 'low':
#    return self.getRandomValue(start = 1000, end = 2000)
#elif usageType == 'medium':
#    return self.getRandomValue(start = 10000, end = 20000)
#elif usageType == 'high':
#    return self.getRandomValue(start = 100000, end = 200000)
import random
import commands
import gzip
class Generator:
    def __init__(self, strStartTime, strEndTime, recordInfoList, flowFileFormat, httpFileFormat, gzipOn, server_ip, server_username, server_http_directory, server_flow_directory,dateformat):
        '''
            This facilitates generation of records from startTime to endTime.
            Input ::
            strStartTime == Start Time of the Generator in str format
            strEndTime == End Time of the Generator in str format
            recordInfoList == list of tuple (subcrId, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL)
            flowFileFormat == flow File Format
            httpFileFormat == http file format
            '''
        t = Time()
        self.ff = FileFormat()
        
        self.startTime = t.getIntTime(strStartTime)
        self.endTime = t.getIntTime(strEndTime)
        self.recordInfoList = recordInfoList
        self.flowFileFormat = flowFileFormat
        self.httpFileFormat = httpFileFormat
        self.gzipOn = gzipOn
        
        self.server_ip = server_ip
        self.server_username = server_username
        self.server_http_directory = server_http_directory
        self.server_flow_directory = server_flow_directory
        
        self.listRecordsHttp = list()
        self.listRecordsFlow = list()
        self.dateformat=dateformat
        
        ''' Do Sub-Tasks '''
        self.generateRecords()
    
    def fileWrite(self, fileName, gzipOn, recordType):
        
        fileName = 'data/' + fileName
        
        # If gzip is turned on, then open the file in gzipped mode,
        # else write the file in normal text format
        if gzipOn == 'yes':
            fileHandle = gzip.open(fileName, 'w', compresslevel = 1)
        elif gzipOn == 'no':
            fileHandle = open(fileName, 'w')
        
        if recordType == 'http':
            self.listRecordsHttp = ['#sn-start-time,sn-end-time,radius-calling-station-id,transaction-uplink-bytes,transaction-downlink-bytes,ip-subscriber-ip-address,ip-server-ip-address,http-host,http-content type,http-url,voip-duration,traffic-type,transaction-downlink-packets,transaction-uplink-packets,bearer-3gpp rat-type,radius-called-station-id,tcp-os-signature,bearer-3gpp imei,http-user-agent\n'] + self.listRecordsHttp
            fileHandle.writelines(self.listRecordsHttp)
            fileHandle.close()
            commands.getstatusoutput('scp %s %s@%s:%s'%(fileName, self.server_username, self.server_ip, self.server_http_directory))
        
        elif recordType == 'flow':
            self.listRecordsFlow = ['#sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id\n'] + self.listRecordsFlow
            fileHandle.writelines(self.listRecordsFlow)
            fileHandle.close()
            commands.getstatusoutput('scp %s %s@%s:%s'%(fileName, self.server_username, self.server_ip, self.server_flow_directory))
        
        commands.getstatusoutput('rm -f %s'%(fileName))
        
    print 'File Written Successfully: %s'%(fileName)

def generateRecords(self):
    sTime=self.startTime
    DatF=self.dateformat
        while sTime < self.endTime:
            genRecordsObj_flow = GenerateRecords()
            genRecordsObj_http = GenerateRecords()
            for recordInfo in self.recordInfoList:
                subcrId = recordInfo[0]
                sampleRecord = recordInfo[1]
                recordType = recordInfo[2]
                usageType = recordInfo[3]
                nOfRecordsLL = recordInfo[4]
                nOfRecordsHL = recordInfo[5]
                tcp_os_present_in_flow_after_aggregation = recordInfo[6]
                tcp_os_signature = recordInfo[7]
                
                if recordType == 'flow':
                    genRecordsObj_flow.generateRecords(sTime, sTime+300, subcrId, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL)
                    self.listRecordsFlow += genRecordsObj_flow.getRecordList()
                elif recordType == 'http':
                    genRecordsObj_http.generateRecords(sTime, sTime+300, subcrId, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL)
                    self.listRecordsHttp += genRecordsObj_http.getRecordList()
                    
                    # Aggregate Http Records into Flow.
                    (subcrId, tot_downbytes, tot_upbytes) = genRecordsObj_http.getAggrHttpInfo()
                    #sn-start-time,sn-end-time,radius-calling-station-id,sn-server-port,sn-app-protocol,sn-volume-amt-ip-bytes-uplink,sn-volume-amt-ip-bytes-downlink,sn-volume-amt-ip-pkts-uplink,sn-volume-amt-ip-pkts-downlink,p2p-protocol,ip-server-ip-address,bearer-3gpp rat-type,voip-duration,sn-direction,traffic-type,bearer-3gpp imei,bearer-3gpp sgsn-address,bearer-ggsn-address,sn-flow-end-time,sn-flow-start-time,radius-called-station-id,bearer-3gpp user-location-information,sn-subscriber-port,ip-protocol,sn-rulebase,tcp-os-signature,bearer-3gpp charging-id
                    start_time = sampleRecord.split(',')[0]
                    end_time = sampleRecord.split(',')[1]
                    if DatF==1:
                          start_time=time.strftime(%Y/%m/%H/%M ,time.gmtime(start_time))
                          end_time=time.strftime(%Y/%m/%H/%M ,time.gmtime(end_time))
                    if tcp_os_present_in_flow_after_aggregation == 'Yes':
                        sampleRecord = '%s,%s,SUBCR_ID,8080,5,UPLINK_BYTES,DOWNLINK_BYTES,182,36,,27.9.126.155,1,1,FromMobile,unclassified,,33686017,454532353,%s,%s,Sushfone-2,231-10-1073-10011,43769,6,rb31,%s,2'%(start_time, end_time, end_time, start_time,tcp_os_signature)
                    else:
                        sampleRecord = '%s,%s,SUBCR_ID,8080,5,UPLINK_BYTES,DOWNLINK_BYTES,182,36,,27.9.126.155,1,1,FromMobile,unclassified,,33686017,454532353,%s,%s,Sushfone-2,231-10-1073-10011,43769,6,rb31,,2'%(start_time, end_time, end_time, start_time)
                    recordType = 'flow'
                    usageType = 'aggr'
                    (nOfRecordsLL, nOfRecordsHL) = (1, 1)
                    genRecordsObj_http.generateRecords(sTime, sTime+300, subcrId, sampleRecord, recordType, usageType, nOfRecordsLL, nOfRecordsHL, tot_downbytes, tot_upbytes)
                    self.listRecordsFlow += genRecordsObj_http.getRecordList()
        
            random.shuffle(self.listRecordsFlow)
            random.shuffle(self.listRecordsHttp)
            
            time_offset = 0
            
            # Write Flow File
            fileName = self.ff.getFileFormat(self.httpFileFormat, sTime+time_offset)
            self.fileWrite(fileName, self.gzipOn, recordType = 'http')
            
            # Write Http File
            fileName = self.ff.getFileFormat(self.flowFileFormat, sTime+time_offset)
            self.fileWrite(fileName, self.gzipOn, recordType = 'flow')
            
            sTime += 300
            self.listRecordsFlow = list()
            self.listRecordsHttp = list()
