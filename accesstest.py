#!/usr/bin/python

import sys
import socket
import requests
import time

ite = 10

output="result.txt"
args = sys.argv



lstUrl = open(args[1], "r")
line = lstUrl.readline()
while line:
  line=line.replace('\n','')
  line=line.replace('\r','')
  if line:
    try:
       addrs=socket.getaddrinfo(line,80,0,socket.SOCK_STREAM)
    except socket.gaierror:
       outStr =  "# cannot resolve " + line
       f = open(output,'a')
       f.write(outStr+'\n')
       f.close()
       addrs = [] 
    for addr in addrs:
       total = 0.0
       try:
         for i in range(0,ite):
           if addr[0] == socket.AF_INET6: 
             response = requests.request('GET','http://['+addr[4][0]+']/',timeout=5) 
             af="ipv6" 
           else:
             response = requests.request('GET','http://'+addr[4][0]+'/',timeout=5)  
             af="ipv4"
           total += response.elapsed.total_seconds()
       except:
         try:  
           for i in range(0,ite):
             if addr[0] == socket.AF_INET6:
               response = requests.request('GET','https://['+addr[4][0]+']/',timeout=5)
               af="ipv6"
             else:
               response = requests.request('GET','https://'+addr[4][0]+'/',timeout=5)
               af="ipv4"
             total += response.elapsed.total_seconds()
         except requests.exceptions.ConnectTimeout:
           outStr = "# connection timeout " + line + " " + addr[4][0]
           f = open(output,'a')
           f.write(outStr+'\n')
           f.close() 
           break
         except requests.exceptions.ReadTimeout:
           outStr = "# read timeout " + line + " " + addr[4][0]
           f = open(output,'a')
           f.write(outStr+'\n')
           f.close()
           break
         except requests.exceptions.ConnectionError:
           outStr = "# connection error " + line + " " + addr[4][0]
           f = open(output,'a')
           f.write(outStr+'\n')
           f.close()
           break         
       outStr = line+','+af+','+addr[4][0] +','+ str(total/ite) +','+ str(len(response.content))
       f = open(output,'a') 
       f.write(outStr+'\n')
       f.close()

  line = lstUrl.readline()


 
