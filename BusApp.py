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

"""

a = []
def callback():
    a.append(E1.get())
    a.append(E2.get())
    a.append(E3.get())
    top.destroy()

top = Toplevel()

w = 400 # width for the Tk root
h = 200 # height for the Tk root

# get screen width and height
ws = top.winfo_screenwidth() # width of the screen
hs = top.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen
# and where it is placed
top.geometry('%dx%d+%d+%d' % (w, h, x, y))

top.title("MyCommute - Driver Login")
L1 = Label(top, text="User Name",anchor='center',pady=20,padx=50)
L1.grid(row=0, column=0)
E1 = Entry(top, bd = 5)
E1.grid(row=0, column=1)

L2 = Label(top, text="Password",anchor='center',pady=10)
L2.grid(row=1, column=0)
E2 = Entry(top, bd = 5, show='*')
E2.grid(row=1, column=1)

L3 = Label(top, text="Bus Route",anchor='center',pady=20)
L3.grid(row=2, column=0)
E3 = Entry(top, bd = 5)
E3.grid(row=2, column=1)

MyButton1 = Button(top, text="Submit", width=10, command=callback)
MyButton1.grid(row=4, column=1)

top.mainloop()

busUsername=a[0]
busPassword=a[1]
busRoute=a[2]
"""

url='http://192.168.43.14:8000/api/buslogin/'
payload={"username":busUsername,"password":busPassword,"rname":"busRoute"}
#payload={"username":"kl15aa2211","password":"lalalala","rname":"335E"}
req = urllib2.Request(url)
req.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(req, json.dumps(payload))
b =ast.literal_eval(response.read())
bustoken = b['token']



cap = cv2.VideoCapture(0)
data = "NULL"
previous_data = "NULL2"


#Setting up Serial connection with Arduino
ser=serial.Serial('/dev/ttyACM0',9600)

while True:
    if ser.inWaiting():
        trigger=ser.readline()


        if trigger[0] == 'K':

            odo_delta = ser.readline()

            #print int(odo_delta)
            #cv2.destroyAllWindows()
            #send odo to server

            while ser.readline()[0] !='K':
                q=10

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
                    #print symbol.data
                    url='http://192.168.43.14:8000/api/readqr/'
                    #payload={"username":busUsername,"password":busPassword,"rname":"busRoute"}
                    payload={"userid":symbol.data,"reading":int(odo_delta)}
                    req = urllib2.Request(url)
                    req.add_header('Content-Type', 'application/json')
                    req.add_header('Authorization', 'Token ' + bustoken)
                    flag = 0
                    try :
                        response = urllib2.urlopen(req, json.dumps(payload))

                    except:
                        response="Invalid QR Code"
                        flag =1
                    if flag == 1:
                        prompt = response
                        flag=0
                    else:
                        prompt = response.read()


                    root =Tk()
                    label1 = Label(root, text=prompt,font=("Helvetica",32 ), width=len(prompt))
                    label1.config(anchor='center',pady=70)
                    label1.pack()


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


                    def close_after_2s():
                        root.destroy()

                    root.after(2000, close_after_2s)
                    root.mainloop()
                    if response == "Invalid QR Code":
                        os.system("/usr/bin/canberra-gtk-play --id='alarm-clock-elapsed'")
                        previous_data=symbol.data
                    else :

                        os.system("/usr/bin/canberra-gtk-play --id='system-ready'")
                        #os.system("notify-send -t 900 \"WELCOME!!\" \"NAME\"")
                        ser.write('T')
                        time.sleep(2)
                        previous_data = symbol.data

                        #while ser.readline()[0]!='D':
                        #    q=10
                        #If not valid, sound alarm


    del(img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cv2.destroyAllWindows()
cap.release()
