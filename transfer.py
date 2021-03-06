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
import _thread
#oauth2
#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
sn = "BRST0003"
username = "ybsj"
global runninglist
runninglist = []
print("------###sn:"+sn+"###------")
print("------###username:"+username+"###------")
myredis = redis.StrictRedis(host="143.92.60.148",port="6379",password="20190321lei",decode_responses=True)
adb_obj = Adbcmd("none")
def end_transfer(result):
    global runninglist
    try:
        myredis.set(result['deviceid']+"transfering","n")
        myredis.expire(result['deviceid']+"transfering",60*8)
        runninglist.remove(result['deviceid'])
    except:
        pass
def start_transfer(result):
    global runninglist
    print("thread start",result)
    # check and setting mobile is busying
    transfering = myredis.get(result['deviceid']+"transfering")
    if transfering == "y":
        print("mobile is running!")
        #myredis.set(result['deviceid']+"transfering","n")
        return
    try:
        if result['deviceid'] in runninglist:
            print("runninglist has ",result['deviceid'])
            return
    except:
        pass
    print("transfering is running......")
    myredis.set(result['deviceid']+"transfering","y")
    myredis.expire(result['deviceid']+"transfering",60*15)
    
    #tansfering......status
    url_transfering = "https://nb.brst.space/api/transfer/changestatus"
    data_transfering  = {'username':username,'status':1,'id':result['id'],'failedreason':'Transfer Success!'}
    httpRequest(url_transfering,data_transfering)
    #checking end
    #check isfirstTransfer
    firstTransfer = myredis.get(result['deviceid']+"isfirstTransfer")
    if firstTransfer !="no":
        print("ft is True,fristTransfer is not no")
        ft = True
    else:
        print("ft is false,firstTransfer is no")
        ft = False
    bank = result['bank_']
    module = importlib.import_module(bank+"."+bank)
    adb_obj_class = getattr(module,bank)
    bank_class = adb_obj_class(result)
    tresult = bank_class.transfer(ft)
    
    if tresult == "101":
        end_transfer(result)
        print("------###No device found!###------")
    if tresult == "102":
        url2 = "https://nb.brst.space/api/transfer/changestatus"
        print(bank_class.errmsg)
        data2 = {'username':username,'status':3,'id':result['id'],'failedreason':bank_class.errmsg}
        httpRequest(url2,data2)
        end_transfer(result)
    if tresult == "10000":
        url_success = "https://nb.brst.space/api/transfer/changestatus"
        data_success  = {'username':username,'status':2,'id':result['id'],'failedreason':'Transfer Success!'}
        httpRequest(url_success,data_success)
        end_transfer(result)
    if tresult == "20000":
        url_success = "https://nb.brst.space/api/transfer/changestatus"
        data_success  = {'username':username,'status':8,'id':result['id'],'failedreason':'??????'}
        httpRequest(url_success,data_success)
        end_transfer(result)
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

while True:
    time.sleep(5)
    try:
        ###############################################
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
                httpdata= {'username':username,'tsn':name}
                result_ = httpRequest(url,httpdata)
                result = result_['data']
                
                #result = {"id":"111","code":1,"bank_":"CITIC","password":"vip17965290","money":"2","cardnumber":"6222020402044197158","hm":"?????????","deviceid":"YST4VKSWEU5D5TSK","mobile":"15383110077"}
                
                if result['code'] ==0:
                    print("------###No transferorder found! Pulling order...in 3 seconds###------")
                else:
                    _thread.start_new_thread( start_transfer, (result, ) )
                    runninglist.append(result['deivceid'])
    except Exception as e:
        print(str(e))
    ###############################################
    


        



