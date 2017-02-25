from Tkinter import *

def callback():
    print("hi")
    print E1.get()
    print E2.get()
    print E3.get()
    top.destroy()
v="dfw"
top = Tk()
L1 = Label(top, text="User Name")
L1.grid(row=0, column=0)
E1 = Entry(top, bd = 5, textvariable=v)
E1.grid(row=0, column=1)
print E1.get()


L1 = Label(top, text="Password")
L1.grid(row=1, column=0)
E2 = Entry(top, bd = 5, show='*')
E2.grid(row=1, column=1)

L1 = Label(top, text="Bus Route")
L1.grid(row=2, column=0)
E3 = Entry(top, bd = 5)
E3.grid(row=2, column=1)


MyButton1 = Button(top, text="Submit", width=10, command=callback)
MyButton1.grid(row=4, column=1)

top.mainloop()
