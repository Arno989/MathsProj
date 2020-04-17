import logging
import sys
import os
from threading import Thread
from tkinter import *

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
sys.path.insert(0, BASE_DIR)

from server_gui import ServerWindow


def Stop():
    logging.info("Deleting window")
    try:
        root.destroy()
        sys.exit()  # stop code run after window deletion ----- threads moeten gestopt worden
        logging.info("Deleted window, this should not show up")
    except Exception as ex:
        logging.error("Start.py :> Exception during stop " + str(ex))

try:
    root = Tk()
    root.geometry("400x600")
    gui = ServerWindow(root)
    root.protocol("WM_DELETE_WINDOW", Stop)
except Exception as ex:
    logging.error(f"Start.py in prep :> {ex}")

try:
    root.mainloop()
except Exception as ex:
    logging.error(f"Start.py :> Unhandled exception in main loop: {ex}")
    Stop()
