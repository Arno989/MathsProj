import logging
import sys
from threading import Thread
from tkinter import *

from server_gui import ServerWindow


def Stop():
    logging.info("Deleting window")
    try:
        print("1")
        root.destroy()
        print("2")
        sys.exit()  # stop code run after window deletion
        print("3")
        logging.info("Deleted window, this should not show up")
        print("4")
    except Exception as ex:
        logging.info("Start.py: " + str(ex))


def _destroy(event):
    logging.info("destroy")


try:
    root = Tk()
    root.geometry("400x600")
    gui = ServerWindow(root)
    root.protocol("WM_DELETE_WINDOW", Stop)
except Exception as ex:
    logging.error(f"Start.py: {ex}")

try:
    root.mainloop()
except Exception as ex:
    logging.error(f"Start.py: {ex}")
    Stop()
