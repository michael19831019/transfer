import os
class Adbcmd:
    def __init__(self):
        os.system("adb devices")
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
        cmd = 'adb -s '+deviceid+' shell input keyevent 26'
        os.popen(cmd)
        return False
    def touch_xml(self,deviceid):
        os.system("adb -s "+deviceid+" shell rm /sdcard/window_dump.xml")
        os.system("sudo adb -s "+deviceid+" shell uiautomator dump")
        while True:
            result = os.system("adb -s "+deviceid+" pull /sdcard/window_dump.xml")
            if result ==0:
                break
            os.system("sudo adb -s "+deviceid+" shell uiautomator dump")
    def tap_pos(self,deviceid,x,y):
        os.system("adb -s "+deviceid+" shell input tap "+str(x)+" "+str(y))
        