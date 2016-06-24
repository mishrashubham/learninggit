import time
import commands
from optparse import OptionParser
from multiprocessing import process
parser = OptionParser(usage="usage: %prog [options]",
                          version="%prog 1.0")


parser.add_option("--outdir", dest="output_directory",
                  help="output directory in which data needs to be copied")


parser.add_option("--indir", dest="input_directory",
                  help="input directory from where data needs to be copied")

parser.add_option("--instartTime",
                  dest="Input_StartTime",
                  default="2015-08-10-10",
                  help="Start Time for input data (Default = 2015-08-10-10-00)")
parser.add_option("--inendTime",
                  dest="Input_EndTime",
                  default="2015-08-10-10",
                  help="End Time for input data (Default = 2015-08-10-10-00)")
parser.add_option("--OutStartTime",
                  dest="Output_Startime",
                  default="2015-08-10-10",
                  help="Start Time for output data (Default = 2015-08-10-10-00)")
parser.add_option("--OutEndTime",
                  dest="Output_Endtime",
                  default="2015-08-10-10",
                  help="End Time for output data (Default = 2015-08-10-10-00)")
(options, args) = parser.parse_args()
def dhcp(input_start_time,input_end_time,output_start_time,output_end_time,input_directory,output_directory):
     input_directory=input_directory
     output_directory=output_directory
     z=input_start_time
     o=input_end_time
     x=output_start_time
     y=output_end_time
     in_st_struc=time.strptime(z,"%Y-%m-%d-%H-%M")
     in_st_epoc=int(time.mktime(in_st_struc))
     in_ed_struc=time.strptime(o,"%Y-%m-%d-%H-%M")
     in_ed_epoc=int(time.mktime(in_ed_struc))
     out_st_struc=time.strptime(x,"%Y-%m-%d-%H-%M")
     out_st_epoc=int(time.mktime(out_st_struc))
     out_ed_struc=time.strptime(y,"%Y-%m-%d-%H-%M")
     out_ed_epoc=int(time.mktime(out_ed_struc))
     print "data copy started..."     
     copy(input_directory,output_directory,in_st_epoc,in_ed_epoc,out_st_epoc,out_ed_epoc)

       



def copy(input_directory,output_directory,in_st_epoc,in_ed_epoc,out_st_epoc,out_ed_epoc):
    print 'x'
    input_directory=input_directory
    output_directory=output_directory
    in_st_epoc=in_st_epoc
    in_ed_epoc=in_ed_epoc
    out_ed_epoc=out_ed_epoc
    out_st_epoc=out_st_epoc
    for i in range(in_st_epoc,in_ed_epoc,300):
         k=time.strftime('%Y/%m/%d/%H/%M',time.gmtime(i)) 
         q=time.strftime('%Y/%m/%d/%H/%M',time.gmtime(out_st_epoc))
         status,output=commands.getstatusoutput('hadoop dfs -mkdir -p %s/%s'%(input_directory,q))
         for y in range(8):
	    print 'hadoop dfs -cp %s/%s/WIRED.DHCP.%s.%s  %s/%s/WIRED.DHCP.%s.%s'%(input_directory,k,i,y,output_directory,q,out_st_epoc,y)
            status,output=commands.getstatusoutput('hadoop dfs -cp %s/%s/WIRED.DHCP.%s.%s  %s/%s/WIRED.DHCP.%s.%s'%(input_directory,k,i,y,output_directory,q,out_st_epoc,y))
         status,output=commands.getstatusoutput('hadoop dfs -cp %s/%s/WIRED.DHCP.%s._DONE  %s/%s/WIRED.DHCP.%s._DONE'%(input_directory,k,i,output_directory,q,out_st_epoc))
         out_st_epoc+=300
    while (out_st_epoc<out_ed_epoc):
        copy(input_directory,output_directory,in_st_epoc,in_ed_epoc,out_st_epoc,out_ed_epoc)
if __name__=='__main__':
         input_directory=options.input_directory
         output_directory=options.output_directory
         input_start_time=options.Input_StartTime
         input_end_time=options.Input_EndTime
         output_start_time=options.Output_Startime
         output_end_time=options.Output_Endtime
         #cp_time=raw_input("enter the any hour's 5 min bin start_tme for which data needs to be replicated:")
         dhcp(input_start_time,input_end_time,output_start_time,output_end_time,input_directory,output_directory)
