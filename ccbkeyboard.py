class Ccbkeyboard:
    def __init__(self,w,h):
        self.w = w
        self.h = h
    def setdisplay(self):
        if self.h == 1544:
            self.num_line = 1186
            self.q_line = 1289
            self.a_line = 1385
            self.z_line = 1490
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
