import os
import time
from xml.dom.minidom import parse
import xml.dom.minidom
from system.adbcmd import Adbcmd
from system.mytools import Mytools
from PSBC.psbckeyboard import Psbckeyboard
import importlib

class PSBC:
    def __init__(self,result):
        self.result = result
        self.adb_obj = Adbcmd()
        self.my_tool = Mytools()
        self.errmsg = "";
        self.package = "com.yitong.mbank.psbc"
    def transfer(self):
        device_list = self.adb_obj.getdevicelist()
        if self.result['deviceid'] not in device_list:
            return "101"
        w = self.adb_obj.getW(self.result['deviceid'])
        h = self.adb_obj.getH(self.result['deviceid'])
        ck = Psbckeyboard(w,h)
        if ck.device_support is False:
            self.errmsg = "Not support mobile!"
            return "102"
        # wakeup screen
        waked = self.adb_obj.isAwaked(self.result['deviceid'])
        #close app
        self.adb_obj.closeapp(self.result['deviceid'],self.package)
        time.sleep(5)
        #start app
        self.adb_obj.startapp(self.result['deviceid'],self.package)
        time.sleep(20)
        
        #press transfer button
        p = self.adb_obj.touch_xml(self.result['deviceid'])
        if p:
            e = self.find_element("",'转账汇款',1)
            if e:
                self.parse_xml("",'转账汇款',1)
        #click password input com.yitong.mbank.psbc:id/etPasswd
        p = self.adb_obj.touch_xml(self.result['deviceid'])
        if p:
            e = self.find_element("com.yitong.mbank.psbc:id/etPasswd",'请输入登录密码',1)
            if e:
                self.parse_xml("com.yitong.mbank.psbc:id/etPasswd",'请输入登录密码',1)
        # tappassword
        p = self.adb_obj.touch_xml(self.result['deviceid'])
        if p:
            self.tappassword()
        # tap login button
        time.sleep(1)
        p = self.adb_obj.touch_xml(self.result['deviceid'])
        if p: 
            e = self.find_element_bySource("com.yitong.mbank.psbc:id/btnLogin")
            if e:
                self.adb_obj.tap_pos(self.result['deviceid'],self.click_pos_x,self.click_pos_y)
            else:
                self.errmsg = "not found login page!"
                return "102"
        time.sleep(30)
        # tap transfer in logined page
        p = self.adb_obj.touch_xml(self.result['deviceid'])
        if p:
            e = self.find_element_bySource("cardTrans")
            repeat = 0
            while True:
                repeat+=1
                if repeat>10:
                    break
                p = self.adb_obj.touch_xml(self.result['deviceid'])
                e = self.find_element_bySource("cardTrans")
                if e:
                    break
            if e:
                self.adb_obj.tap_pos(self.result['deviceid'],self.click_pos_x,self.click_pos_y)
            else:
                self.errmsg = "not found transfer2 button!"
                return "102"
        time.sleep(10)
        p = self.adb_obj.touch_xml(self.result['deviceid'])
        if p:
            e = self.find_element_bySource("PAYEE_NAME")
            if e:
                self.adb_obj.tap_pos(self.result['deviceid'],self.click_pos_x,self.click_pos_y)
                # change adbkeyboard
                time.sleep(1)
                self.adb_obj.change_adbkeyboard(self.result['deviceid'])
                time.sleep(2)
                # input name
                self.adb_obj.input_ch(self.result['hm'],self.result['deviceid'])
                time.sleep(0.5)
                # change sougou
                self.adb_obj.change_sogou(self.result['deviceid'])
                time.sleep(1)
        # tap cardnumber input
        p = self.adb_obj.touch_xml(self.result['deviceid'])
        if p:
            e = self.find_element_bySource("PAYEE_ACCT_NO")
            if e:
                self.adb_obj.tap_pos(self.result['deviceid'],self.click_pos_x,self.click_pos_y)
                cmd = "adb -s "+self.result['deviceid']+" shell input text "+self.result['cardnumber']
                os.system(cmd)
        # money
        p = self.adb_obj.touch_xml(self.result['deviceid'])
        if p:
            e = self.find_element_bySource("TRANS_AMT")
            if e:
                self.adb_obj.tap_pos(self.result['deviceid'],self.click_pos_x,self.click_pos_y)
                p2 = self.adb_obj.touch_xml(self.result['deviceid'])
                if p2:
                    self.tap_money()
        # confirm transfer order
        p = self.adb_obj.touch_xml(self.result['deviceid'])
        if p:
            e = self.find_element_bySource("confirm")
            if e:
                self.adb_obj.tap_pos(self.result['deviceid'],self.click_pos_x,self.click_pos_y)
        time.sleep(10)
        # spassword and sms code page
        p =self.adb_obj.touch_xml(self.result['deviceid'])
        if p:
            e = self.find_element_byText("交易密码:")
            if e:
                print(self.click_pos_x)
                self.click_pos_x+=300
                print("now:",self.click_pos_x)
                self.adb_obj.tap_pos(self.result['deviceid'],self.click_pos_x,self.click_pos_y)
                time.sleep(2)
                # keyboard appear
                p3 =self.adb_obj.touch_xml(self.result['deviceid'])
                if p3:
                    self.tappassword("spassword")
                else:
                    print("p3 not found! keyboard not appear")
                    self.errmsg="spassword not input"
                    return "102"
        # sms page
        p =self.adb_obj.touch_xml(self.result['deviceid'])
        e = self.find_element_byText("获取验证码")
        if e:
            self.adb_obj.tap_pos(self.result['deviceid'],self.click_pos_x,self.click_pos_y)
            time.sleep(2)
            sms = self.my_tool.getsms(self.result['mobile'])
            if sms =="123456":
                self.errmsg = "sms error!"
                return "102"
            p2 = self.find_element_bySource("mulTransDialogCode0")
            self.adb_obj.tap_pos(self.result['deviceid'],self.click_pos_x,self.click_pos_y)
            time.sleep(2)
            cmd = "adb -s "+self.result['deviceid']+" shell input text "+sms
            os.system(cmd)
        # confirm transfer
        print("press the transfer last button")
        e2 = self.find_element_bySource("dialogButton0")
        if e2:
            self.adb_obj.tap_pos(self.result['deviceid'],self.click_pos_x,self.click_pos_y)
        time.sleep(8)
        return "10000"
    def tap_money(self):
        passwordChar_c = ["0","1","2","3","4","5","6","7","8","9","."]
        money = self.result['money']
        
        print(money)
        for c in money:
            if c in passwordChar_c:
                time.sleep(0.5)
                self.parse_keyboard("",c)
                time.sleep(0.5)
        time.sleep(0.5)
        self.parse_keyboard("com.yitong.mbank.psbc:id/btnBoardCancel",'完成')
        time.sleep(0.5)
    # find element in xml
    def find_element(self,resource,text_button,index=0):
        deviceid = self.result['deviceid']
        finded = False
        DOMTree = xml.dom.minidom.parse("window_dump_"+deviceid+".xml")
        nodes = DOMTree.getElementsByTagName("node")
        for n in nodes:
            node_att = n.getAttribute("text")
            if index == 0 or index ==1 or index==6 or index==8:
                node_att = n.getAttribute("text")
            if index == 2:
                node_att = n.getAttribute("content-desc")
            if n.getAttribute("resource-id")==resource and node_att ==text_button:
                finded = True
        return finded
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
        return finded
    def find_element_bySource(self,resource):
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
        return finded
    # click
    def parse_xml(self,resource,text_button,index=0):
        deviceid = self.result['deviceid']
        finded = False
        DOMTree = xml.dom.minidom.parse("window_dump_"+deviceid+".xml")
        nodes = DOMTree.getElementsByTagName("node")
        
        for n in nodes:
            node_att = n.getAttribute("text")
            if index == 0 or index ==1:
                node_att = n.getAttribute("text")
            if index == 2:
                node_att = n.getAttribute("content-desc")
            if n.getAttribute("resource-id")==resource and node_att ==text_button:
                print(n.getAttribute("bounds"))
                pos = n.getAttribute("bounds")
                pos = pos[1:-1].replace("][",",").split(",")
                click_pos_x = (int(pos[2])-int(pos[0]))/2+int(pos[0])
                click_pos_y = (int(pos[3])-int(pos[1]))/2+int(pos[1])
                self.adb_obj.tap_pos(self.result['deviceid'],click_pos_x,click_pos_y)
                finded = True
        return finded
    def parse_keyboard(self,resource,text_button):
        time.sleep(1)
        finded = False
        deviceid = self.result['deviceid']
        p = True
        if p:  
            DOMTree = xml.dom.minidom.parse("window_dump_"+deviceid+".xml")
            nodes = DOMTree.getElementsByTagName("node")
            if resource=="":
                for n in nodes:
                    if n.getAttribute("text") ==text_button:
                        pos = n.getAttribute("bounds")
                        pos = pos[1:-1].replace("][",",").split(",")
                        click_pos_x = (int(pos[2])-int(pos[0]))/2+int(pos[0])
                        click_pos_y = (int(pos[3])-int(pos[1]))/2+int(pos[1])
                        self.adb_obj.tap_pos(self.result['deviceid'],click_pos_x,click_pos_y)
            else:
                for n in nodes:
                    if n.getAttribute("resource-id")==resource and n.getAttribute("text") ==text_button:
                        pos = n.getAttribute("bounds")
                        pos = pos[1:-1].replace("][",",").split(",")
                        click_pos_x = (int(pos[2])-int(pos[0]))/2+int(pos[0])
                        click_pos_y = (int(pos[3])-int(pos[1]))/2+int(pos[1])
                        self.adb_obj.tap_pos(self.result['deviceid'],click_pos_x,click_pos_y) 
        else:
            return finded
    # tap password
    def tappassword(self,pw = "password"):
        keyboardType = 0
        capslock = 0
        passwordChar_a = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        passwordChar_b = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        passwordChar_c = ["0","1","2","3","4","5","6","7","8","9"]
        if pw =="password":
            password = self.result['password']
        else:
            password = self.result['spassword']
        print(password)
        for c in password:
            print(c)
            if c in passwordChar_a:
                if keyboardType ==1:
                    self.parse_keyboard("com.yitong.mbank.psbc:id/btnNumBoardChangeAbc",'ABC')
                    self.adb_obj.touch_xml(self.result['deviceid'])
                    print("press btnNumBoardChangeAbc")
                    time.sleep(1)
                    keyboardType = 0
                    capslock =0
                if capslock==0:
                    self.parse_keyboard("",c)
                    print("press:",c)
                if capslock ==1:
                    self.parse_keyboard("com.yitong.mbank.psbc:id/btnAbcBoardUpperLowSwitch",'')
                    print("press UpperLowSwitch")
                    time.sleep(1)
                    self.parse_keyboard("",c)
                    print("press:",c)
                    capslock =0
            if c in passwordChar_b:
                if keyboardType ==1:
                    self.adb_obj.touch_xml(self.result['deviceid'])
                    self.parse_keyboard("com.yitong.mbank.psbc:id/btnNumBoardChangeAbc",'ABC')
                    print("btnNumBoardChangeAbc")
                    time.sleep(1)
                    keyboardType = 0
                    capslock = 0
                if capslock==0:
                    self.parse_keyboard("com.yitong.mbank.psbc:id/btnAbcBoardUpperLowSwitch",'')
                    print("press UpperLowSwitch")
                    time.sleep(1)
                    self.parse_keyboard("",c.lower())
                    print("press:",c)
                    self.parse_keyboard("com.yitong.mbank.psbc:id/btnAbcBoardUpperLowSwitch",'')
                    print("back press UpperLowSwitch")
                if capslock==1:
                    self.parse_keyboard("",c.lower())
                    print("press:",c)
            if c in passwordChar_c:
                if keyboardType==0:
                    if pw =="password":
                        self.parse_keyboard("com.yitong.mbank.psbc:id/btnAbcBoardChangeNumber",'123')
                    else:
                        self.parse_keyboard("com.yitong.mbank.psbc:id/btnAbcBoardChangeNumber",'')
                    print("press changeNumber")
                    time.sleep(1)
                    self.adb_obj.touch_xml(self.result['deviceid'])
                    keyboardType=1
                self.parse_keyboard("",c)
                time.sleep(1)
                print("press:",c)
        time.sleep(0.5)
        self.parse_keyboard("com.yitong.mbank.psbc:id/btnBoardCancel",'完成')
        time.sleep(0.5)
    