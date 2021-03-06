import os
import time
from xml.dom.minidom import parse
import xml.dom.minidom
from CITIC.citickeyboard import Citickeyboard
from system.adbcmd import Adbcmd
from system.mytools import Mytools
import importlib
import redis
import json
class CITIC:
    def __init__(self,result):
        self.result = result
        self.adb_obj = Adbcmd("com.ecitic.bank.mobile")
        self.my_tool = Mytools()
        self.errmsg = "";
        self.package = "com.ecitic.bank.mobile";
    
    def login(self,ck):
            #close app
            self.adb_obj.closeapp(self.result['deviceid'],self.package)
            time.sleep(5)
            #start app
            self.adb_obj.startapp(self.result['deviceid'],self.package)
            time.sleep(20)
            self.click_text("我的",ck,None,0,0)
            self.click_text("转账",ck,1,0,0)
            time.sleep(10)
            self.click_text("请输入密码",ck,1,0,0)
            time.sleep(10)
            self.tappassword()
            time.sleep(10)
            self.click_text("登录",ck,1,0,0)
    def transfer(self,ft):
        device_list = self.adb_obj.getdevicelist()
        if self.result['deviceid'] not in device_list:
            return "101"
        w = self.adb_obj.getW(self.result['deviceid'])
        h = self.adb_obj.getH(self.result['deviceid'])
        ck = Citickeyboard(w,h)
        if ck.device_support is False:
            self.errmsg = "Not support mobile!"
            return "102"
        self.keyboard_pos = ck.set_c_pos()
        self.keyboard_npos = ck.set_n_pos()
        waked = self.adb_obj.isAwaked(self.result['deviceid'])
        print(waked)
        if ft is True:
            self.login(ck)
            print("login repeat ft is true")
        else:
            print("继续转账 no login")
            tc = self.click_text("继续转账",ck,1,0,0)
            if tc is False:
                print("tc is false!")
                self.login(ck)
        time.sleep(10)
        self.click_text("银行卡转账",ck,1,0,0)
        time.sleep(10)
        self.click_text("收款人",ck,1,200,0)
        time.sleep(1)
        self.adb_obj.change_adbkeyboard(self.result['deviceid'])
        time.sleep(2)
        # input name
        self.adb_obj.input_ch(self.result['hm'],self.result['deviceid'])
        time.sleep(0.5)
        # hidden others
        self.click_text("下一步",ck,1,0,0)
        # input cardnumber
        self.click_text("收款账号",ck,1,200,0)
        for s in self.result['cardnumber']:
            cmd = "adb -s "+self.result['deviceid']+" shell input text "+s
            os.system(cmd)
        # input money
        self.click_text("转账金额",ck,1,200,100)
        cmd = "adb -s "+self.result['deviceid']+" shell input text "+self.result['money']
        os.system(cmd)
        # hidden others
        self.click_text("下一步",ck,1,0,-50)
        time.sleep(1)
        self.adb_obj.restartsms(self.result['deviceid'],self.package)
        self.click_text("下一步",ck,1,0,0)
        # input sms
        
        self.click_text("获取验证码",ck,1,-200,0)
        sms = self.my_tool.getsms(self.result['mobile'])
        if sms =="123456" or sms is None:
            self.errmsg = "sms error!"
            return "102"
        for c in sms:
            print(c)
            for p in self.keyboard_npos:
                if c == p:
                    self.adb_obj.tap_pos(self.result['deviceid'],self.keyboard_npos[p][0],self.keyboard_npos[p][1])
                    break
            
        self.click_text("确定",ck,1,0,0)
        time.sleep(7)
        p = self.adb_obj.touch_xml(self.result['deviceid'])
        t = self.find_element_byText("转账成功")
        if t:
            try:
                print("转账成功")
                self.my_tool.set_first_transferFlag(self.result['deviceid'],"no")
            except:
                print("------------------------------------------------------error")
            return "10000"
        else:
            try:
                print("转账weizhi")
                self.my_tool.set_first_transferFlag(self.result['deviceid'],"yes")
            except:
                print("------------------------------------------------------error2")
            return "20000"
    def click_text(self,text,ck,bounds,m_x,m_y):
        p = self.adb_obj.touch_xml(self.result['deviceid'])
        if p:
            ad = self.click_resource("com.ecitic.bank.mobile:id/close_product_send",0,0)
            if ad:
                p = self.adb_obj.touch_xml(self.result['deviceid'])
            t = self.find_element_byText(text)
            if t:
                if bounds is None:
                    self.adb_obj.tap_pos(self.result['deviceid'],ck.my_x,ck.my_y)
                else:
                    self.adb_obj.tap_pos(self.result['deviceid'],self.click_pos_x+m_x,self.click_pos_y+m_y)
                print("clicked!")
                return True
            else:
                print("not found text")
                
                return False
        else:
            return False
    def click_resource(self,resource,m_x,m_y):
        hasad = False
        t = self.find_element_byResource(resource)
        if t:
            self.adb_obj.tap_pos(self.result['deviceid'],self.click_pos_x+m_x,self.click_pos_y+m_y)
            hasad = True
        return hasad
    def find_element_byResource(self,resource):
        self.click_pos_x=0
        self.click_pos_y=0
        deviceid = self.result['deviceid']
        finded = False
        DOMTree = xml.dom.minidom.parse("window_dump_"+deviceid+".xml")
        nodes = DOMTree.getElementsByTagName("node")
        for n in nodes:
            if n.getAttribute("resource-id")==resource:
                pos = n.getAttribute("bounds")
                pos = pos[1:-1].replace("][",",").split(",")
                self.click_pos_x = (int(pos[2])-int(pos[0]))/2+int(pos[0])
                self.click_pos_y = (int(pos[3])-int(pos[1]))/2+int(pos[1])
                finded = True
                break
        return finded
    def tappassword(self):
        time.sleep(1)
        password = self.result['password']
        for c in password:
            print(c)
            time.sleep(0.5)
            for p in self.keyboard_pos:
                if c == p:
                    self.adb_obj.tap_pos(self.result['deviceid'],self.keyboard_pos[p][0],self.keyboard_pos[p][1])
                    break
    def find_element_byText(self,text):
        self.click_pos_x=0
        self.click_pos_y=0
        deviceid = self.result['deviceid']
        finded = False
        DOMTree = xml.dom.minidom.parse("window_dump_"+deviceid+".xml")
        nodes = DOMTree.getElementsByTagName("node")
        for n in nodes:
            if n.getAttribute("text")==text:
                pos = n.getAttribute("bounds")
                pos = pos[1:-1].replace("][",",").split(",")
                self.click_pos_x = (int(pos[2])-int(pos[0]))/2+int(pos[0])
                self.click_pos_y = (int(pos[3])-int(pos[1]))/2+int(pos[1])
                finded = True
                break
        return finded
        