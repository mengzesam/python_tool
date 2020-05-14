#command line:
##python findcontinuetime.py key=4 time=2 date=1 continue=15 min=49.967 max=50.033 encoding=gb2312 data2.csv out.csv

import sys
import pandas

MAX_READLINE=2200000
srcfile='data.csv'
outfile='out.csv'
startrow=6
delimiter=','
src_encoding='gb2312'
key_col=3
time_col=1
date_col=0
value_min=49.967
value_max=50.033
mincontsecs=15

if __name__ == "__main__":
    argv=sys.argv
    argn=len(argv)
    if(argn>=3):
        srcfile=argv[-2]
        outfile=argv[-1]
        argv_dict=dict([argv[i].split('=') for i in range(1,argn-2)])
        keys=argv_dict.keys()
        if('start' in keys):
            startrow=int(1*argv_dict['start'])-1
        if('key' in keys):
            key_col=int(1*argv_dict['key'])-1
        if('time' in keys):
            time_col=int(1*argv_dict['time'])-1
        if('date' in keys):
            date_col=int(1*argv_dict['date'])-1
        if('continue' in keys):
            mincontsecs=int(1*argv_dict['continue'])
        if('min' in keys):
            value_min=float(1*argv_dict['min'])
        if('max' in keys):
            value_max=float(1*argv_dict['max'])
        if('encoding' in keys):
            src_encoding=argv_dict['encoding']
    data=pandas.read_csv(srcfile,
                    sep=delimiter,
                    encoding=src_encoding,
                    skipinitialspace=True,
                    skip_blank_lines=True,
                    skiprows=startrow,
                    header=None,
                    index_col=False,
                    nrows=MAX_READLINE
                )
    out_data=pandas.DataFrame()
    nrows,ncols=data.shape
    contsecs=1
    count=0
    pos=0
    off=0
    while(pos<nrows and data.iloc[pos,key_col]>=value_min and data.iloc[pos,key_col]<=value_max):
        pos+=1
    while(pos+off+1<nrows):
        dt=pandas.to_datetime(data.iloc[pos+off+1,date_col]+" "+data.iloc[pos+off+1,time_col])-pandas.to_datetime(data.iloc[pos+off,date_col]+" "+data.iloc[pos+off,time_col])
        seconds=dt.seconds
        if(seconds<=1 and (data.iloc[pos+off+1,key_col]>value_max or data.iloc[pos+off+1,key_col]<value_min)):
            if(seconds==1):
                contsecs+=1
            off+=1
        else:
            if(contsecs>=mincontsecs):
                count+=1            
                out_data=out_data.append(data.iloc[pos:pos+off+1])
            pos=pos+off+1      
            while(pos<nrows and data.iloc[pos,key_col]>=value_min and data.iloc[pos,key_col]<=value_max):
                pos+=1
            off=0
            contsecs=1
        if((pos+off)%1000==0):
            print(pos+off)     
    print('count={}'.format(count))
    if(count>0):
        out_data.to_csv(outfile,index=False,header=False)
