import os
import time
from xml.dom.minidom import parse
import xml.dom.minidom
import importlib
import redis
import json
from system.adbcmd import Adbcmd
import requests
from PIL import Image
import base64
sn = "BRST0003"
username = "ybsj"
print("------###sn:"+sn+"###------")
print("------###username:"+username+"###------")
myredis = redis.StrictRedis(host="143.92.60.148",port="6379",password="20190321lei",decode_responses=True)
adb_obj = Adbcmd()
def onlineSet(sn):
    # deivce online set
    print("------###Transfer device  online setting start!###------")
    myredis.set(sn+"-status",1)
    myredis.expire(sn+"-status",50)
    print("------###Transfer device online setting over!###------")
onlineSet(sn)
myredis.delete("device-"+sn)
def httpRequest(url,data):
    print("------###Network requesting!###------")
    requests.ReadTimeout = 60
    err_count = 0
    result_ = {'data':-1,'msg':-1,"code":0,'bank':'CCB'}
    while err_count<3:
        try:
            result_ = json.loads(requests.post(url,json = data,timeout = 60).text)
            break
        except Exception as e:
            print(str(e))
            print("http request error")
            time.sleep(1)
            err_count+=1
    print("------###Network requesting End!###------")
    return result_
url = "https://nb.brst.space/api/transfer/transferorder"
httpdata= {'username':username,'tsn':sn}
#result = {"bank":"CCB","deviceid":"8HT4DEQODUAQNFMJ","password":"861690"}
while True:
    time.sleep(3)
    result_ = httpRequest(url,httpdata)
    result = result_['data']
    print(result)
    # deivce online set
    onlineSet(sn)
    #check mobile sn
    myredis.delete("device-"+sn)
    device_list = adb_obj.getdevicelist()
    print(device_list)
    if len(device_list)<=0:
        print("###No mobile found!###")
    else:
        for name in device_list: 
            myredis.hset("device-"+sn,name,1)
        if result['code'] ==0:
            print("------###No transferorder found! Pulling order...in 3 seconds###------")
        else:
            bank = result['bank']
            module = importlib.import_module(bank+"."+bank)
            adb_obj_class = getattr(module,bank)
            bank_class = adb_obj_class(result)
            tresult = bank_class.transfer()
            
            if tresult == "101":
                print("------###No device found!###------")
            if tresult == "102":
                url2 = "https://nb.brst.space/api/transfer/changestatus"
                print(bank_class.errmsg)
                data2 = {'username':username,'status':3,'id':result['id'],'failedreason':bank_class.errmsg}
                httpRequest(url2,data2)
            if tresult == "10000":
                url_success = "https://nb.brst.space/api/transfer/changestatus"
                data_success  = {'username':username,'status':2,'id':result['id'],'failedreason':'Transfer Success!'}
                httpRequest(url_success,data_success)

        
        



