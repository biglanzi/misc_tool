#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import sys
import requests
import time
import os
import commands
import pdb

Web_URL="http://192.168.4.111:8080"

class EasyHttp:
    def get(self, url, para):
        try:
            return requests.get(Web_URL+url,params=para,timeout=(5,10))
        except requests.exceptions.RequestException as e:
            print(e)
            exit(1)
    def post(self, url, data):
        try:
            return requests.post(Web_URL+url,json=data,timeout=(5,10))
        except requests.exceptions.RequestException as e:
            print(e)
            exit(1)
def getAllServiceInfo():
    return
def getHostName():
    with open("/etc/hostname",'r') as f:
        return f.read()
def getProcInfo(pid):
    info={"ProcessId":pid}
    (status, dummy) = commands.getstatusoutput("ps -q "+str(pid)+" -o euser=,%mem=")
    output=dummy.split()
    info["User"]=output[0]
    info["Memory"]=output[1]
    (status, output) = commands.getstatusoutput("ls -l /proc/"+str(pid)+"/fd |wc -l")
    info["Tcp"]=int(output)
    (status, output) = commands.getstatusoutput("sypath=$(readlink /proc/"+str(pid)+"/cwd);cd $sypath;cd ..;du -shc *|tail -n 1|cut -f 1")
    info["Disk"]=output 
    return info
    
def main():
    reportInfo = {}
    hostname=getHostName()
    httpApi = EasyHttp()
    res =httpApi.get("/ServiceList",{"host":hostname})
    reportInfo["host"]=hostname
    reportInfo["time"]=int(time.time())
    (status, output) = commands.getstatusoutput("top -bn 1|grep '%Cpu'|cut -d ':' -f 2|cut -d ',' -f 4|cut -d ' ' -f 2")
    reportInfo["Cpu"]=round(100-float(output),1)
    (status, output) = commands.getstatusoutput("free|grep Mem|tr -s ' '|cut -d ' ' -f 2,3")
    output=output.split()
    reportInfo["Memory"]=round(float(output[1])/int(output[0])*100,1)
    (status, output) = commands.getstatusoutput("netstat -ant|wc -l")
    reportInfo["TCP"]=int(output)
    (status, output) = commands.getstatusoutput("df --output=size|awk -F ' ' '{if(NR>1)sum+=$1;}END{print sum;}'")
    alldisksize=float(output)
    (status, output) = commands.getstatusoutput("df --output=used|awk -F ' ' '{if(NR>1)sum+=$1;}END{print sum;}'")
    useddisksize=float(output)
    reportInfo["Disk"]=round(useddisksize/alldisksize*100,1)
    reportInfo["Service"]=[]
    for info in res.json()["Service"]:
        procname=str(info["ServiceId"])+"_"+str(info["ZoneId"])
        (status, output) = commands.getstatusoutput("pidof "+procname)
        if status != 0:
            print("process dead")
            (status, output) = commands.getstatusoutput("systemctl restart "+procname)
        else:
            each= getProcInfo(output)
            each["ServiceId"]=info["ServiceId"]
            each["ZoneId"]=int(info["ZoneId"])
            reportInfo["Service"].append(each)
    print(reportInfo)
    httpApi.post("/Monitor/Data",reportInfo)
    
if __name__ == "__main__":
    main()
