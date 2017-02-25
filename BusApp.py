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
from Tkinter import *


odo_delta = 0
scanner = zbar.ImageScanner()
scanner.parse_config('enable')
busUsername = raw_input("Username: ")
busPassword = getpass()
busRoute = raw_input("Route name: ")
url='http://192.168.43.14:8000/api/buslogin/'
#payload={"username":busUsername,"password":busPassword,"rname":"busRoute"}
payload={"username":"kl15aa2211","password":"lalalala","rname":"335E"}
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
                if str(symbol.data) != previous_data:
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

                    root = Tk()
                    w = 800 # width for the Tk root
                    h = 200 # height for the Tk root

                    # get screen width and height
                    ws = root.winfo_screenwidth() # width of the screen
                    hs = root.winfo_screenheight() # height of the screen

                    # calculate x and y coordinates for the Tk root window
                    x = (ws/2) - (w/2)
                    y = (hs/2) - (h/2)

                    # set the dimensions of the screen
                    # and where it is placed
                    root.geometry('%dx%d+%d+%d' % (w, h, x, y))



                    root.title("MyCommute")
                    prompt = response.read()
                    label1 = Label(root, text=prompt,font=("Helvetica",32 ), width=len(prompt))
                    label1.config(anchor='center',pady=70)
                    label1.pack()

                    def close_after_2s():
                        root.destroy()

                    root.after(2000, close_after_2s)
                    root.mainloop()

                    #os.system("notify-send -t 900 \"WELCOME!!\" \"NAME\"")
                    ser.write('T')
                    time.sleep(5)
                    previous_data = symbol.data
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
