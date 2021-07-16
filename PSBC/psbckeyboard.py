class Psbckeyboard:
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