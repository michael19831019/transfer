import os
import time
from xml.dom.minidom import parse
import xml.dom.minidom
from CCB.ccbkeyboard import Ccbkeyboard
from system.adbcmd import Adbcmd
from system.mytools import Mytools
import importlib

class CCB:
    def __init__(self,result):
        self.result = result
        self.adb_obj = Adbcmd()
        self.my_tool = Mytools()
        self.errmsg = "";
    def transfer(self):
        device_list = self.adb_obj.getdevicelist()
        if self.result['deviceid'] not in device_list:
            return "101"
        w = self.adb_obj.getW(self.result['deviceid'])
        h = self.adb_obj.getH(self.result['deviceid'])
        ck = Ccbkeyboard(w,h)
        if ck.device_support is False:
            self.errmsg = "Not support mobile!"
            return "102"
        self.keyboard_pos = ck.set_c_pos()
        waked = self.adb_obj.isAwaked(self.result['deviceid'])
        #close app
        self.adb_obj.closeapp(self.result['deviceid'],'com.chinamworld.main')
        time.sleep(5)
        #start app
        self.adb_obj.startapp(self.result['deviceid'],'com.chinamworld.main')
        time.sleep(20)
        
        # find ad1
        if self.adb_obj.touch_xml(self.result['deviceid']):
            self.ccb_parse_xml(self.result['deviceid'],"close","关闭",2)
        # find ad2
        if self.adb_obj.touch_xml(self.result['deviceid']):
            self.ccb_parse_xml(self.result['deviceid'],"close","关闭",2)
            
        # transfer button 1
        z = self.adb_obj.touch_xml(self.result['deviceid'])
        if z:
            t = self.ccb_parse_xml(self.result['deviceid'],"main_home_smart_transfer_text","转账")
            if t is not True:
                self.errmsg = "Transfer button not found01!"
                return "102"
        else:
            self.errmsg = "Transfer button not found02!"
            return "102"
        # transfer button 2
        z = self.adb_obj.touch_xml(self.result['deviceid'])
        if z:
            t = self.ccb_parse_xml(self.result['deviceid'],"tv_function","转账")
            if t is not True:
                self.errmsg = "Transfer button not found03!"
                return "102"
        else:
            self.errmsg = "Transfer button not found04!"
            return "102"
        # tap password
        z = self.adb_obj.touch_xml(self.result['deviceid'])
        if z:
            t = self.ccb_find_element(self.result['deviceid'],"btn_confirm","登录")
        if t:
            self.tappassword()
        else:
            self.errmsg = "Login page not found!"
            return "102"
        #click login
        self.ccb_parse_xml(self.result['deviceid'],"btn_confirm","登录")
        time.sleep(3)
        z = self.adb_obj.touch_xml(self.result['deviceid'])
        if z:
            t = self.ccb_parse_xml(self.result['deviceid'],"et_cash_name","请输入收款户名")
            if t:
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
        else:
            self.errmsg = "Not found the right page!"
            return "102"
        # input cardnumber
        t = self.ccb_parse_xml(self.result['deviceid'],"et_collection_account","请输入收款账号或手机号")
        cmd = "adb -s "+self.result['deviceid']+" shell input text "+self.result['cardnumber']
        os.system(cmd)
        #input money
        t = self.ccb_parse_xml(self.result['deviceid'],"et_tran_amount","请输入转账金额")
        time.sleep(3)
        cmd = "adb -s "+self.result['deviceid']+" shell input text "+self.result['money']
        os.system(cmd)
        #press next button
        #hidden keyboard
        self.adb_obj.tap_pos(self.result['deviceid'],ck.ok_x,ck.ok_y)
        time.sleep(1)
        self.ccb_parse_xml(self.result['deviceid'],"btn_right1","下一步")
        # touch sms xml
        z = self.adb_obj.touch_xml(self.result['deviceid'])
        if z:
            t = self.ccb_find_element(self.result['deviceid'],"dlg_right_tv","继续")
            if t:  
                self.ccb_parse_xml(self.result['deviceid'],"dlg_right_tv","继续")
        z = self.adb_obj.touch_xml(self.result['deviceid'])
        if z:
            self.ccb_parse_xml(self.result['deviceid'],"et_code","",6)
            sms = self.my_tool.getsms(self.result['mobile'])
            if sms =="123456":
                self.errmsg = "sms error!"
                return "102"
            cmd = "adb -s "+self.result['deviceid']+" shell input text "+sms
            os.system(cmd)
            self.ccb_parse_xml(self.result['deviceid'],"btn_confirm","确定",8)
            time.sleep(3)
        #touch imgcode page
        z = self.adb_obj.touch_xml(self.result['deviceid'])
        t = self.ccb_find_element(self.result['deviceid'],"ccb_title_right_btn","完成")
        if t:
            self.errmsg ="Transfer success!"
            return "10000"
        t = self.ccb_find_element(self.result['deviceid'],"tv_title","请输入账户取款密码")
        if t:
            self.tapspassword(self.result,ck.abc_x,ck.abc_y)
            code_value = self.findimgcode(self.result['deviceid'],"native_graph_iv","")
            if code_value == "":
                self.errmsg = "ImgCode Not found!"
                return "102"
            tcode = self.ccb_parse_xml(self.result['deviceid'],"native_graph_et","请输入右侧图片的字符")
            time.sleep(0.5)
            cmd = "adb -s "+self.result['deviceid']+" shell input text "+code_value
            os.system(cmd)
            time.sleep(0.5)
            #hiden keyboard
            self.adb_obj.tap_pos(self.result['deviceid'],ck.ok_x,ck.ok_y)
            time.sleep(1)
            # last step
            self.ccb_parse_xml(self.result['deviceid'],"btn_confirm","确定")
            print("Transfer success!")
            return "10000"
        z = self.adb_obj.touch_xml(self.result['deviceid'])
        if z:
            t = self.ccb_find_element(self.result['deviceid'],"ccb_title_right_btn","完成")
            if t:
                print("Transfer success!")
        return "10000"
    
    
    
    def tappassword(self):
        password = self.result['password']
        for c in password:
            print(c)
            for p in self.keyboard_pos:
                if c == p:
                    self.adb_obj.tap_pos(self.result['deviceid'],self.keyboard_pos[p][0],self.keyboard_pos[p][1])
                    break
    def tapspassword(self,res,x,y):
        self.adb_obj.tap_pos(res['deviceid'],x,y)
        password = self.result['spassword']
        for c in password:
            print(c)
            for p in self.keyboard_pos:
                if c == p:
                    self.adb_obj.tap_pos(self.result['deviceid'],self.keyboard_pos[p][0],self.keyboard_pos[p][1])
                    break
    def ccb_parse_xml(self,deviceid,resource,text_button,index=0):
        finded = False
        DOMTree = xml.dom.minidom.parse("window_dump_"+deviceid+".xml")
        nodes = DOMTree.getElementsByTagName("node")
        
        for n in nodes:
            node_att = n.getAttribute("text")
            if index == 0 or index ==1:
                node_att = n.getAttribute("text")
            if index == 2:
                node_att = n.getAttribute("content-desc")
            if n.getAttribute("resource-id")=="com.chinamworld.main:id/"+resource and node_att ==text_button:
                print(n.getAttribute("bounds"))
                pos = n.getAttribute("bounds")
                pos = pos[1:-1].replace("][",",").split(",")
                click_pos_x = (int(pos[2])-int(pos[0]))/2+int(pos[0])
                click_pos_y = (int(pos[3])-int(pos[1]))/2+int(pos[1])
                self.adb_obj.tap_pos(self.result['deviceid'],click_pos_x,click_pos_y)
                finded = True
        return finded
    def findimgcode(self,deviceid,resource,text_button,index=1):
        DOMTree = xml.dom.minidom.parse("window_dump_"+deviceid+".xml")
        nodes = DOMTree.getElementsByTagName("node")
        for n in nodes:
            node_att = n.getAttribute("text")
            if n.getAttribute("resource-id")=="com.chinamworld.main:id/"+resource and node_att ==text_button:
                return n.getAttribute("content-desc")

    # find element in xml
    def ccb_find_element(self,deviceid,resource,text_button,index=0):
        finded = False
        DOMTree = xml.dom.minidom.parse("window_dump_"+deviceid+".xml")
        nodes = DOMTree.getElementsByTagName("node")
        for n in nodes:
            node_att = n.getAttribute("text")
            if index == 0 or index ==1 or index==6 or index==8:
                node_att = n.getAttribute("text")
            if index == 2:
                node_att = n.getAttribute("content-desc")
            if n.getAttribute("resource-id")=="com.chinamworld.main:id/"+resource and node_att ==text_button:
                finded = True
        return finded