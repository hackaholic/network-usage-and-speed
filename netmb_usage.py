import os
import re
import time
import subprocess

backtrack = {}

def calculate(i,flag,interface):
    k = re.findall("bytes:(\d+)",i)
    interface = interface.strip().split()[0]
    if flag == 0:
        backtrack[interface] = [k[0],k[1]]
        return "\t  Total Recived: " + str(float(k[0])/1024/1024) + "Mb \t" + "Total sent: " + str(float(k[1])/1024/1024) + " Mb"
        
    else:
       download_speed,upload_speed = (float(k[0])-float(backtrack[interface][0]))/1024, (float(k[1])-float(backtrack[interface][1]))/1024
       backtrack[interface] = [k[0],k[1]]
       return "\t  Total Recived: " + (str(float(k[0])/1024/1024) + " Mb").ljust(30) + "Total sent: " + str(float(k[1])/1024/1024) + " Mb\n\t  Download speed:" + (str(download_speed) + " kb/s").ljust(30) + "Upload speed: " + str(upload_speed)+ " kb/s"

def net_usage(flag):
    child = subprocess.Popen('ifconfig',stdout=subprocess.PIPE)
    output,err = child.communicate()
    if err:
        print err
        exit
    output = output.split('\n\n')
    for x in output:
        x=x.split('\n')
        if not x[0].strip().startswith('lo'):
            print x[0]
            for i in x:
                if i.strip().startswith('RX bytes'):
                    print calculate(i,flag,x[0]) + "\n"
    print "Press Ctrl+C to Stop"
    time.sleep(1)
    print "\033c"

if __name__ == '__main__':
    net_usage(0)
    try:
        while True:
           net_usage(1)
    except KeyboardInterrupt as e:
        print "\nStoped By user"
        exit
