import serial
import time
ser=serial.Serial('/dev/ttyACM1',9600)

while True:


    a=ser.readline()
    #print a
    if a[0]=='K':
        odo=ser.readline()
        print odo[0]
    time.sleep(3)
