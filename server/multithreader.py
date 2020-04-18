import logging
import socket
import threading
import sys

import pandas as pd
import numpy as np

from server.clienthandler import ClientHandler


class Movie_thread(threading.Thread):
    def __init__(self, host, port, message_queue):
        threading.Thread.__init__(self)
        self.connected = False
        self.host = socket.gethostname()
        self.port = port
        self.message_queue = message_queue

    @property
    def is_connected(self):
        return self.connected

    def init_server(self):
        # create a socket object
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((self.host, self.port))
        self.serversocket.listen(5)
        self.connected = True
        self.print_gui_message("SERVER STARTED")

    def close_server_socket(self):
        # remove the socket object
        self.print_gui_message("CLOSING SERVER")
        self.serversocket.close()
        self.connected = False

    # thread-klasse!
    def run(self):
        try:
            threads = 0
            clh = []
            while True:
                self.print_gui_message("MT> waiting for client...")

                # establish a connection
                socket_to_client, addr = self.serversocket.accept()
                self.print_gui_message(f"MT> Established connection with: {addr}")

                # initiate thread
                threads += 1
                clh.append(ClientHandler(socket_to_client, self.messages_queue, threads))
                try:
                    clh[threads].start()
                except (KeyboardInterrupt, SystemExit):
                    logging.info("MT> Interrupted, calling Stop.")
                    clh.stop()
                    sys.kill()

                self.print_gui_message(
                    f"Current thread count: {threads}" # threading.active_count()
                )
        except Exception as ex:
            logging.error(f"MT> {ex}")
            self.print_gui_message(f"MT Error: {ex}")

    def print_gui_message(self, message):
        self.message_queue.put(f"MT> {message}")
        logging.info(f"MT> {message}")

