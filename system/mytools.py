import base64
from PIL import Image
import os
import time
import requests
import redis
import json
class Mytools:
    def cutimagecode(self,deviceid,left,top,right,bottom):
        os.system("adb -s "+deviceid+" shell rm /sdcard/"+deviceid+"code.jpg")
        time.sleep(1)
        cmd = "adb -s "+deviceid+" shell screencap -p "+deviceid+"code.jpg"
        os.syetem(cmd)
        cmd = "adb -s "+deviceid+" pull "+deviceid+"code.png"
        img2 = Image.open(deviceid+"code.jpg")
        cropped = img2.crop(left,top,right,bottom)
        cropped.save(deviceid+"imagecode.jpg")
    def set_first_transferFlag(self,deviceid,flag):
        myredis = redis.StrictRedis(host="143.92.60.148",port="6379",password="20190321lei",decode_responses=True)
        myredis.set(deviceid+"isfirstTransfer",flag)
        myredis.expire(deviceid+"isfirstTransfer",60)
        
    def base64_api(self,img,deviceid):
        with open(img,'rb') as f:
            base64_data = base64encode(f.read(deviceid+"code.jpg"))
            b64 = base64_data.decode()
        data = {"username":"a13680018640","password":"mlgb12345","image":b64}
        result = json.loads(requests.post("http://api.ttshitu.com/base64",json=data).text)
        if result['success']:
            return result['data']['result']
        else:
            return result["message"]
    def getsms(self,mobile):
        myredis = redis.StrictRedis(host="143.92.60.148",port="6379",password="20190321lei",decode_responses=True)
        count = 0
        smscode = "123456"
        while True:
            count+=1
            print("smscode waiting ",count," seconds")
            if count>120:
                break
            smscode = myredis.get(mobile+"sms")
            if smscode is not None:
                myredis.set(mobile+"sms","")
                myredis.expire(mobile+"sms",6)
                break
            time.sleep(1)
        return smscode
    def test(self):
        data={"content":"【邮储银行】验证码：043782（序号7151），您向孟峰峰尾号4340账户转账20.50元。任何人索要验证码均为诈骗，请勿泄露！","mobile":"123"}
        result = json.loads(requests.post("http://143.92.60.134/public/api/index/getsms",json=data).text)
        print(result)