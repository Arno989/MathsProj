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
    logging.info("Deleting window")
    try:
        root.destroy()
        logging.info("root destroyed but program still running, have to close threads")
        sys.exit()
        logging.info("closed threads and stopped program, this should not show up")
    except Exception as ex:
        logging.error("Start.py :> Exception during stop " + str(ex))


logging.info(f"Start.py :> Server running")
try:
    root = ServerWindow()
    root.geometry("400x600")
    #gui = ServerWindow(root)
    root.protocol("WM_DELETE_WINDOW", Stop)
except Exception as ex:
    logging.error(f"Start.py in prep :> {ex}")

try:
    while True:
        try:
            root.mainloop()
        except Exception as ex:
            logging.error(f"Start.py :> Unhandled exception in main loop: {ex}")
            Stop()

except KeyboardInterrupt:
    print("Interrupted, calling Stop().")
    Stop()
