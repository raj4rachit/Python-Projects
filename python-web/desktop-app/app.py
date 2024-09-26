from tkinter import *


def buttonpress(r):
    r = 6 * r
    Label(t, text=r, font=(60)).grid(row=5, column=2)


t = Tk()
t.geometry("800x600")
Label(t, text="MUO Tkinter tutorial", font=(60)).grid()
fileOptions = ["New", "open", "Save", "Save as"]
fileOptionsAfterseparator = ["Import", "Export", "Exit"]
viewOptions = ["Transform", "Edit", "Create"]
menuBar = Menu(t)
file = Menu(menuBar, tearoff=0)
for i in fileOptions:
    file.add_command(label=i, command=None)
file.add_separator()
for i in fileOptionsAfterseparator:
    file.add_command(label=i, command=None)
menuBar.add_cascade(label="File", menu=file)

View = Menu(menuBar, tearoff=0)
for i in viewOptions:
    View.add_command(label=i, command=None)
menuBar.add_cascade(label="View", menu=View)
t.config(menu=menuBar)

Omenu = StringVar()  # set the variable type of the options</strong>
Omenu.set("MUO")  # specify a default value for the menu icon</strong>
OptionMenu(t, Omenu, "MUO", "Amazon", "Tutorial").grid()

Checkbutton(t, text="Select option").grid()
t.title("HRMS")
t.mainloop()
