import os
import time
from xml.dom.minidom import parse
import xml.dom.minidom
from CCB.ccbkeyboard import Ccbkeyboard
from system.adbcmd import Adbcmd
import importlib

class CCB:
    def __init__(self,result):
        self.result = result
        self.adb_obj = Adbcmd()
    def transfer(self):
        device_list = self.adb_obj.getdevicelist()
        if self.result['deviceid'] not in device_list:
            return "101"
        w = self.adb_obj.getW(self.result['deviceid'])
        h = self.adb_obj.getH(self.result['deviceid'])
        ck = Ccbkeyboard(w,h)
        self.keyboard_pos = ck.set_c_pos()
        waked = self.adb_obj.isAwaked(self.result['deviceid'])
        self.adb_obj.touch_xml(self.result['deviceid'])
        self.ccb_parse_xml(self.result['deviceid'],"close","关闭",2)
        self.adb_obj.touch_xml(self.result['deviceid'])
        self.ccb_parse_xml(self.result['deviceid'],"main_home_smart_transfer_text","转账")
        self.adb_obj.touch_xml(self.result['deviceid'])
        self.ccb_parse_xml(self.result['deviceid'],"tv_function","转账")
        self.adb_obj.touch_xml(self.result['deviceid'])
        self.tappassword()
        return "10000"
    def tappassword(self):
        password = self.result['password']
        for c in password:
            print(c)
            for p in self.keyboard_pos:
                if c == p:
                    self.adb_obj.tap_pos(self.result['deviceid'],self.keyboard_pos[p][0],self.keyboard_pos[p][1])
                    break
    def ccb_parse_xml(self,deviceid,resource,text_button,index=0):
        DOMTree = xml.dom.minidom.parse("window_dump_"+deviceid+".xml")
        nodes = DOMTree.getElementsByTagName("node")
        for n in nodes:
            if index == 0:
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
