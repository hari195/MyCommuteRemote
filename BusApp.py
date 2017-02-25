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
import requests
import urllib2
import ast

scanner = zbar.ImageScanner()
scanner.parse_config('enable')
username = raw_input("Username: ")
password = getpass()
url='http://192.168.43.14:8000/api-token-auth/'
payload={"username":"kl15ab2233","password":"lalalala"}
#r=requests.post(url, data=json.dumps(payload))

req = urllib2.Request(url)
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(payload))
b =ast.literal_eval(response.read())
bustoken = b['token']



cap = cv2.VideoCapture(0)
data = "NULL"
previous_data = "NULL2"
#Setting up Serial connection with Arduino
#ser=serial.Serial('/dev/ttyACM1',9600)

#Send get request with U/P as payload
#Extract token from response
#url='https://www.google.com'
#payload={'some':'data'}
#r=requests.post(url, data=json.dumps(payload))

#Use that token for further communications


while(True):
    #trigger=ser.readline()
    #if trigger == "K":

    #    break
    # else:

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pil=PIL.Image.fromarray(gray)
    width,height = pil.size
    raw=pil.tostring()
    img=zbar.Image(width,height,'Y800',raw)


    cv2.imshow('frame',gray)
    scanner.scan(img)
    for symbol in img:
        if str(symbol.type) == "QRCODE":

		if str(symbol.data) !=  previous_data:
		   #Send POST request with data as payload and token from login


           #Check response for validity. If valid allow passenger and display pop up message

           #ser.write('T')
           #while ser.readline()!='D':
           #   time.sleep(0.5)


           #If not valid, sound alarm
		   #os.system("/usr/bin/canberra-gtk-play --id='system-ready'")
   		   #os.system("/usr/bin/canberra-gtk-play --id='alarm-clock-elapsed'")

		   print symbol.data
		   os.system("notify-send -t 900 \"WELCOME!!\" \"NAME\"")
        previous_data = symbol.data
    del(img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



        cv2.destroyAllWindows()
cap.release()
