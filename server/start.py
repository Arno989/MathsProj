import logging
import sys
import os
from threading import Thread
from tkinter import *

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
sys.path.insert(0, BASE_DIR)

from server.server_gui import ServerWindow

#try:
#    root = ServerWindow()
#    root.geometry("400x600")
    #gui = ServerWindow()
#    root.protocol("WM_DELETE_WINDOW", Stop)
#except Exception as ex:
#    logging.error(f"Start.py in prep :> {ex}")

def Stop():
    logging.info("Start> Deleting window")
    try:
        root.destroy()
        logging.info("Start> window destroyed, calling system exit")
        sys.exit()
    except Exception as ex:
        logging.error(f"Start> Exception during stop {ex}")


logging.info(f"Start> Server online")
root = ServerWindow()
try:
    root.geometry("400x600")
    #gui = ServerWindow(root)
    root.protocol("WM_DELETE_WINDOW", Stop)
except Exception as ex:
    logging.error(f"Start.py> {ex}")

try:
    while True:
        try:
            root.mainloop()
        except Exception as ex:
            logging.error(f"Start> Unhandled exception in main loop: {ex} \n       Calling stop")
            Stop()

except KeyboardInterrupt:
    print("Start> Interrupted, calling Stop.")
    Stop()
