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
    ser.write(b'xf0\x03')
result = urllib.request.urlopen("http://143.92.60.134/1.txt")
contents = result.read().decode('UTF-8')
f = open("result.txt",'w')
f.write(contents)
f.close()
count_i = 0
time.sleep(1)
for line in open("result.txt"):
    count_i = count_i +1
    for c in line:
        if c=="3":
            print("(3)")
            #print("three")
            three()
            right()
        if c=="1":
            print("(1)")
            one()
            right()
            #print("one")
        if c=="0":
            print("(0)")
            #print("zero")
            zero()
            right()
    #9
    three()
    right()
    #10
    zero()
    right()
    #11
    three()
    one()
    zero()
    right()
    #12
    three()
    one()
    right()
    #13
    three()
    #one()
    right()
    #14
    three()
    zero()
    #enter()
    #if count_i%5==0:
        #enter()
    enter()
    enter()
    #print(line)


