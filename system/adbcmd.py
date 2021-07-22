import os
from xml.dom.minidom import parse
import xml.dom.minidom
class Adbcmd:
    def __init__(self,package):
        os.system("adb devices")
        self.package = package
    # devicelist
    def getdevicelist(self):
        result_list=[]
        result = os.popen("adb devices").readlines()
        if len(result)==1:
            print("no devices")
        else:
            for index,value in enumerate(result):
                if index !=0 and "device" in value:
                    result_list.append(os.popen("adb devices").readlines()[index].replace("\t","").replace("device","").replace("\n",""))
            return result_list
    # get device width
    def getW(self,devicesid):
        result_list = os.popen("adb -s "+devicesid+" shell dumpsys window displays |grep 'DisplayFrames'").readline()
        w = result_list.split(" ")[3][2:]
        return int(w)
    # get device height
    def getH(self,devicesid):
        result_list = os.popen("adb -s "+devicesid+" shell dumpsys window displays |grep 'DisplayFrames'").readline()
        h = result_list.split(" ")[4][2:]
        return int(h)
    # device is awaked or not
    def isAwaked(self,deviceid):
        if deviceid == '':
            cmd = 'adb shell dumpsys window policy'
        else:
            cmd = 'adb -s ' + deviceid + ' shell dumpsys window policy'
        screenAwakevalue = 'mAwake=true'
        allList=""
        allList = os.popen(cmd).readlines()
        for strs in allList:
            if screenAwakevalue in strs:
                return True
        screenAwakevalue2 = "SCREEN_STATE_ON"
        for strs in allList:
            if screenAwakevalue2 in strs:
                return True
        cmd = 'adb -s '+deviceid+' shell input keyevent 26'
        os.popen(cmd)
        return False
    # startapp
    def startapp(self,deviceid,apppackage):
        cmd = 'adb -s '+deviceid+' shell monkey -p '+apppackage+' -c android.intent.category.LAUNCHER 1'
        os.system(cmd)
    # close app
    def closeapp(self,deviceid,apppackage):
        cmd = 'adb -s '+deviceid+' shell am force-stop '+apppackage
        os.system(cmd)
    # change adbkeyboard
    def change_adbkeyboard(self,deviceid):
        cmd = 'adb -s '+deviceid+ ' shell ime set com.android.adbkeyboard/.AdbIME'
        os.system(cmd)
    # change sougou
    def change_sogou(self,deviceid):
        cmd = 'adb -s '+deviceid+ 'shell ime set com.sohu.inputmethod.sogou.vivo/.SogouIME'
        os.system(cmd)
    # input chinese
    def input_ch(self,str,deviceid):
        cmd = 'adb -s '+deviceid+' shell am broadcast -a ADB_INPUT_TEXT --es msg '+str
        os.system(cmd)
    # remove,create and get xml
    def touch_xml(self,deviceid):
        wk = self.isAwaked(deviceid)
        os.system("adb -s "+deviceid+" shell rm /sdcard/window_dump_"+deviceid+".xml")
        os.system("sudo adb -s "+deviceid+" shell uiautomator dump /sdcard/window_dump_"+deviceid+".xml")
        count = 0
        while True:
            count +=1
            result = os.system("adb -s "+deviceid+" pull /sdcard/window_dump_"+deviceid+".xml")
            if result ==0:
                DOMTree = xml.dom.minidom.parse("window_dump_"+deviceid+".xml")
                nodes = DOMTree.getElementsByTagName("node")
                for n in nodes:
                    if n.getAttribute("package")==self.package:
                        return True
            if count >100:
                return False
            os.system("sudo adb -s "+deviceid+" shell uiautomator dump /sdcard/window_dump_"+deviceid+".xml")
    # click pos on device
    def tap_pos(self,deviceid,x,y):
        os.system("adb -s "+deviceid+" shell input tap "+str(x)+" "+str(y))
        