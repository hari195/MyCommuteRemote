import numpy as np
import cv2
import zbar
import Image
import time
import os
from getpass import getpass
import PIL
import serial

#ser=serial.Serial('/dev/ttyACM1',9600)
#ser.write('T')



scanner = zbar.ImageScanner()
scanner.parse_config('enable')
username = raw_input("Username: ")
password = getpass()

cap = cv2.VideoCapture(0)
data = "NULL"
previous_data = "NULL2"

#Send get request with U/P as payload
#Extract token from response
#Use that token for further communications


while(True):

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
		   #If not valid, sound alarm
		   #os.system("/usr/bin/canberra-gtk-play --id='system-ready'")
   		   #os.system("/usr/bin/canberra-gtk-play --id='alarm-clock-elapsed'")

		   print symbol.data
		   os.system("notify-send -t 900 \"WELCOME!!\" \"NAME\"")
        previous_data = symbol.data
    del(img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()
