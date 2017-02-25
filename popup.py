from Tkinter import Label, Tk
root = Tk()
w = 400 # width for the Tk root
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
prompt = 'Hello'
label1 = Label(root, text=prompt,font=("Helvetica",32 ), width=len(prompt))
label1.config(anchor='center',pady=70)
label1.pack()

def close_after_2s():
    root.destroy()

root.after(1000, close_after_2s)
root.mainloop()
