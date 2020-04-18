import logging
import socket
import threading
import sys

import pandas as pd
import numpy as np

from clienthandler import ClientHandler

logging.basicConfig(level=logging.INFO)


class Movie_thread(threading.Thread):
    def __init__(self, host, port, messages_queue):
        threading.Thread.__init__(self)
        self.__is_connected = False
        self.host = socket.gethostname()
        self.port = port
        # self.init_server()
        self.messages_queue = messages_queue

    @property
    def is_connected(self):
        return self.__is_connected

    def init_server(self):
        # create a socket object
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((self.host, self.port))
        self.serversocket.listen(5)
        self.__is_connected = True
        self.print_gui_message("SERVER STARTED")

    def close_server_socket(self):
        # remove the socket object
        self.print_gui_message("CLOSING SERVER")
        self.serversocket.close()
        self.__is_connected = False

    # thread-klasse!
    def run(self):
        try:
            while True:
                self.print_gui_message("waiting for clients...")

                # establish a connection
                socket_to_client, addr = self.serversocket.accept()
                self.print_gui_message(f"Established connection with: {addr}")

                # initiate thread
                clh = ClientHandler(socket_to_client, self.messages_queue)
                try:
                    clh.start()
                except (KeyboardInterrupt, SystemExit):
                    clh.stop()
                    sys.kill()

                self.print_gui_message(
                    f"Current thread count: {threading.active_count()}"
                )
        except Exception as ex:
            logging.error(f"Multithreader.py :> {ex}")
            self.print_gui_message(f"SOCKET CLOSED: {ex}")

    def print_gui_message(self, message):
        self.messages_queue.put(f"Server:>  {message}")
        logging.info(f"Multithreader:  {message}")

