from tkinter import *
from threading import Thread

import os
print(os.getcwd())

from server_gui import ServerWindow


def callback():
    print("callback")
    gui.close()
    root.destroy()


root = Tk()
root.geometry("600x500")
gui = ServerWindow(root)
root.protocol("WM_DELETE_WINDOW", callback)
root.mainloop()
