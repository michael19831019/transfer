import os
import time
from xml.dom.minidom import parse
import xml.dom.minidom
from ccbkeyboard import Ccbkeyboard
from adbcmd import Adbcmd

def ccb_parse_xml(resource,text_button,index=0):
    DOMTree = xml.dom.minidom.parse("window_dump.xml")
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
            #tap_pos(click_pos_x,click_pos_y)
adb_obj = Adbcmd()
device_list = adb_obj.getdevicelist()
result = {"bank":"CCB","deviceid":"8HT4DEQODUAQNFMJ","password":"861690"}

w = adb_obj.getW(result['deviceid'])
h = adb_obj.getH(result['deviceid'])
ck = Ccbkeyboard(w,h)
keyboard_pos = ck.set_c_pos()
waked = adb_obj.isAwaked(result['deviceid'])

adb_obj.touch_xml(result['deviceid'])
ccb_parse_xml("close","关闭",2)
adb_obj.touch_xml(result['deviceid'])
ccb_parse_xml("main_home_smart_transfer_text","转账")
adb_obj.touch_xml(result['deviceid'])
ccb_parse_xml("tv_function","转账")
adb_obj.touch_xml(result['deviceid'])

password = "861690"
for c in password:
    print(c)
    for p in keyboard_pos:
        if c == p:
            adb_obj.tap_pos(result['deviceid'],keyboard_pos[p][0],keyboard_pos[p][1])
            break
    

        
        



