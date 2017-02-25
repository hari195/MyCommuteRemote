import numpy as np
import cv2
import zbar
import Image
import time
import os
from getpass import getpass
import PIL
import serial
import json
import urllib2
import ast
from Tkinter import Label, Tk


#root = Tk()

odo_delta = 0
scanner = zbar.ImageScanner()
scanner.parse_config('enable')
busUsername = raw_input("Username: ")
busPassword = getpass()
busRoute = raw_input("Route name: ")
url='http://192.168.43.14:8000/api/buslogin/'
#payload={"username":busUsername,"password":busPassword,"rname":"busRoute"}
payload={"username":"kl15ab2233","password":"lalalala","rname":"335E"}
req = urllib2.Request(url)
req.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(req, json.dumps(payload))
b =ast.literal_eval(response.read())
bustoken = b['token']
print bustoken


cap = cv2.VideoCapture(0)
data = "NULL"
previous_data = "NULL2"


#Setting up Serial connection with Arduino
ser=serial.Serial('/dev/ttyACM0',9600)

while True:
    if ser.inWaiting():
        trigger=ser.readline()
        print "port "
        print trigger
        if trigger[0] == 'K':

            odo_delta = ser.readline()
            print "Got K!!"
            print int(odo_delta)
            #cv2.destroyAllWindows()
            #send odo to server

            while ser.readline()[0] !='K':
                q=10
            print "Received stop trigger. resuming scan mode.."
            print "Odo sent to server"
            previous_data="NULL2"
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pil=PIL.Image.fromarray(gray)
    width,height = pil.size
    raw=pil.tostring()
    img=zbar.Image(width,height,'Y800',raw)
    cv2.namedWindow("frame", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("frame", cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
    cv2.imshow('frame',gray)
    scanner.scan(img)
    for symbol in img:
        if str(symbol.type) == "QRCODE":
                if str(symbol.data) !=  previous_data:
                    #Send POST request with data as payload and token from login
                    #Check response for validity. If valid allow passenger and display pop up message
                    print symbol.data
                    url='http://192.168.43.14:8000/api/readqr/'
                    #payload={"username":busUsername,"password":busPassword,"rname":"busRoute"}
                    payload={"userid":symbol.data,"reading":int(odo_delta)}
                    req = urllib2.Request(url)
                    req.add_header('Content-Type', 'application/json')
                    req.add_header('Authorization', 'Token ' + bustoken)
                    response = urllib2.urlopen(req, json.dumps(payload))
                    print response.read()

                    os.system("notify-send -t 900 \"WELCOME!!\" \"NAME\"")

                    previous_data = symbol.data

                    ser.write('T')
                    time.sleep(2)
                    print "Servo rotates"
                    #while ser.readline()[0]!='D':
                    #    q=10
                    #If not valid, sound alarm
                    #os.system("/usr/bin/canberra-gtk-play --id='system-ready'")
                    #os.system("/usr/bin/canberra-gtk-play --id='alarm-clock-elapsed'")

    del(img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cv2.destroyAllWindows()
cap.release()
