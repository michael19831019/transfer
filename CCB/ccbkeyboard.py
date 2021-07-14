class Ccbkeyboard:
    def __init__(self,w,h):
        self.w = w
        self.h = h
        
        self.device_support = False
        self.setdisplay()
    def setdisplay(self):
        if self.h == 1544:
            self.num_line = 1186
            self.q_line = 1289
            self.a_line = 1385
            self.z_line = 1490
            self.codeLeft = 470
            self.codeTop = 860
            self.codeRight = 644
            self.codeBottom = 935
            self.ok_x = 640
            self.ok_y = 1086
            self.abc_x = 120
            self.abc_y = 1086
            self.device_support = True
        if self.h ==1600:
            self.num_line = 1231
            self.q_line = 1334
            self.a_line = 1432
            self.z_line = 1535
            self.codeLeft = 470
            self.codeTop = 860
            self.codeRight = 644
            self.codeBottom = 935
            self.ok_x = 642
            self.ok_y = 1140
            self.abc_x = 120
            self.abc_y = 1140
            self.device_support = True
    def set_c_pos(self):
        cpos={}
        num = ["1","2","3","4","5","6","7","8","9","0"]
        q = ["q","w","e","r","t","y","u","i","o","p"]
        a = ["shift","a","s","d","f","g","h","j","k","l"]
        z = ["z","x","c","v","b","n","m","backspace"]
        for index in range(len(num)):
            cpos[num[index]] = [self.w/10/2+index*self.w/10,self.num_line]
            cpos[q[index]] = [self.w/10/2+index*self.w/10,self.q_line]
            cpos[a[index]] = [self.w/10/2+index*self.w/10,self.a_line]
            if index <= 7:
                cpos[z[index]] = [(index+2)*self.w/10,self.z_line]
        return cpos
    def set_n_pos(self):
        pass
