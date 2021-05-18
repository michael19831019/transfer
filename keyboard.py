from ccbkeyboard import Ccbkeyboard
class Keyboard:
    def __init__(self,w,h,bank):
        self.w = w
        self.h = h
        self.bank = bank
    def put(self):
        if self.bank == "CCB":
            bank_keyboard = Ccbkeyboard(self.w,self.h)
            bank_keyboard.setdisplay()
            return bank_keyboard.set_c_pos()
            
            
    