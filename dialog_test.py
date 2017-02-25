from Tkinter import *
from bwidget import *
t = Tk()
t.title('password')
def printMe(s):
        print s

b = Button(t, relief=LINK, text="Quit", command=t.destroy)
b.pack()

p = PasswordDialog(t, type="okcancel", labelwidth=10,
                command=lambda s='have pwd': printMe(s))
t.mainloop()
