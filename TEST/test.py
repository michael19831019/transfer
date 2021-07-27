from system.mytools import Mytools
class Test:
    def t(self):
        self.my_tool = Mytools()
        sms = self.my_tool.getsms("15383110077")
        if sms =="123456":
            print("sms error!")
        for c in sms:
            print(c)