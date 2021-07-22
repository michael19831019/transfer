class Citickeyboard:
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
            self.device_support = True
        if self.h ==1600:
            self.num_line = 1175
            self.q_line = 1260
            self.a_line = 1360
            self.z_line = 1455
            self.my_x = 633
            self.my_y = 1535
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
        npass={}
        npass["0"] = [360,1548]
        npass["1"] = [119,1262]
        npass["2"] = [359,1262]
        npass["3"] = [602,1262]
        npass["4"] = [119,1358]
        npass["5"] = [359,1358]
        npass["6"] = [602,1358]
        npass["7"] = [119,1456]
        npass["8"] = [359,1456]
        npass["9"] = [602,1456]
        return npass

