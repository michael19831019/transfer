import os
import time
from xml.dom.minidom import parse
import xml.dom.minidom
import importlib
import redis
from system.adbcmd import Adbcmd
sn = "BRST0001"
username = "ybsj"
myredis = redis.StrictRedis(host="143.92.60.148",port="6379",password="20190321lei",decode_responses=True)
adb_obj = Adbcmd()
result = {"bank":"CCB","deviceid":"8HT4DEQODUAQNFMJ","password":"861690"}
while True:
    time.sleep(3)
    # deivce online set
    myredis.set(sn+"-status",1)
    myredis.expire(sn+"-status",50)
    #check mobile sn
    myredis.delete("device-"+sn)
    device_list = adb_obj.getdevicelist()
    for name in device_list: 
        myredis.hset("device-"+sn,name,1)
    #print(device_list)
    
    #bank = result['bank']
    #module = importlib.import_module(bank+"."+bank)
    #adb_obj_class = getattr(module,bank)
    #bank_class = adb_obj_class(result)
    #tresult = bank_class.transfer()
    #if tresult == "101":
        #print("no device found")
    
    

        
        



