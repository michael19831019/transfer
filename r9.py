import serial
import time
import urllib.request
char_sleep = 0.1
tongduan_code = 0.05
ser = serial.Serial("/dev/ttyAMA0", 9600)
def esc():
    time.sleep(char_sleep)
    ser.write(b'\x76')
    time.sleep(tongduan_code)
    ser.write(b'\xf0')
    ser.write(b'\x76')
def three():
    time.sleep(char_sleep)
    ser.write(b'\x26')
    time.sleep(tongduan_code)
    ser.write(b'\xf0')
    ser.write(b'\x26')
def one():
    time.sleep(char_sleep)
    ser.write(b'\x16')
    time.sleep(tongduan_code)
    ser.write(b'\xf0\x16')
def five():
    time.sleep(char_sleep)
    ser.write(b'\x2e')
    time.sleep(tongduan_code)
    ser.write(b'\xf0\x2e')
def zero():
    time.sleep(char_sleep)
    ser.write(b'\x45')
    time.sleep(tongduan_code)
    ser.write(b'\xf0\x45')
def enter():
    time.sleep(char_sleep)
    ser.write(b'\x5A')
    time.sleep(tongduan_code)
    ser.write(b'\xf0\x5A')
def eight():
    time.sleep(char_sleep)
    ser.write(b'\x3e')
    time.sleep(tongduan_code)
    ser.write(b'\xf0\x3e')
def right():
    time.sleep(char_sleep)
    ser.write(b'\xe0\x74')
    time.sleep(tongduan_code)
    ser.write(b'\xe0\xf0\x74')
def f2():
    time.sleep(char_sleep)
    ser.write(b'\x06')
    time.sleep(tongduan_code)
    ser.write(b'\xf0\x06')
def f5():
    time.sleep(char_sleep)
    ser.write(b'\x03')
    time.sleep(tongduan_code)
    ser.write(b'\xf0\x03')
result = urllib.request.urlopen("http://143.92.60.134/1.txt")
contents = result.read().decode('UTF-8')
f = open("result.txt",'w')
f.write(contents)
f.close()
count_i = 0
group = 0
time.sleep(5)
esc()
time.sleep(1)
zero()
time.sleep(0.5)
eight()
time.sleep(1)
bei = 5
for line in open("result.txt"):
    count_i = count_i +1
    for c in line:
        if c=="3":
            print("(3)")
            #print("three")
            three()
        if c=="1":
            print("(1)")
            one()
            #print("one")
        if c=="0":
            print("(0)")
            #print("zero")
            zero()
        if c=="*":
            print("*")
            #print("right")
            right()
    
    print("==========")
    if count_i%5==0:
        group+=1
        if bei == 1:
            print("bei1:",bei)
            pass
        else:
            time.sleep(0.5)
            print("bei:",bei)
            f5()
            
            time.sleep(0.5)
            five()
            time.sleep(0.5)
            #zero()
            enter()
        
            enter()
        time.sleep(1)
        print("group:",group)
    if count_i>=2400:
        print("payper none......")
        time.sleep(180)
    #print(line)

