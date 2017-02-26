from Tkinter import *
a = []
def callback():
    a.append(E1.get())
    a.append(E2.get())
    a.append(E3.get())

    top.destroy()

top = Tk()

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

print a[0]
