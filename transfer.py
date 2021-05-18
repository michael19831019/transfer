import os
import time
from xml.dom.minidom import parse
import xml.dom.minidom
from keyboard import Keyboard

dict_cmd = {
    "adb":"adb devices",
    "display":"adb shell dumpsys window displays |grep 'DisplayFrames'",
    "rmxml":"adb shell rm /sdcard/window_dump.xml",
    "xmldump":"sudo adb shell uiautomator dump",
    "xmlpull":"adb pull /sdcard/window_dump.xml"
    }
def tap_pos(x,y):
    os.system("adb shell input tap "+str(x)+" "+str(y))
def touch_xml():
    os.system(dict_cmd['rmxml'])
    os.system(dict_cmd['xmldump'])
    while True:
        result = os.system(dict_cmd['xmlpull'])
        if result ==0:
            break
        os.system(dict_cmd['xmldump'])
def parse_xml(resource,text_button,index=0):
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
            tap_pos(click_pos_x,click_pos_y)

result = os.system(dict_cmd["adb"])
os.system(dict_cmd['display'])
obj = Keyboard(720,1544,"CCB")
keyboard_pos = obj.put()
touch_xml()
parse_xml("close","关闭",2)
touch_xml()
parse_xml("main_home_smart_transfer_text","转账")
touch_xml()
parse_xml("tv_function","转账")
touch_xml()
password = "861690"
for c in password:
    print(c)
    for p in keyboard_pos:
        if c == p:
            tap_pos(keyboard_pos[p][0],keyboard_pos[p][1])
            break
    

        
        



