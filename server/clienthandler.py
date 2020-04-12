import threading
import logging
import pickle
import pandas as pd
import numpy as np

debug = True
print(__name__)

dataset = pd.read_csv("server/movies.csv", encoding="ISO-8859-1")


class ClientHandler(threading.Thread):
    numbers_clienthandlers = 0

    def __init__(self, socketclient, messages_queue):
        threading.Thread.__init__(self)
        self.socket_to_client = socketclient
        self.messages_queue = messages_queue
        self.id = ClientHandler.numbers_clienthandlers
        ClientHandler.numbers_clienthandlers += 1

    def run(self):
        writer_obj = self.socket_to_client.makefile(mode="rwb")

        self.print_gui_message("Waiting for inputs...")
        operation = pickle.load(writer_obj)
        print(operation)

        # Search by genre
        while operation != "C":
            while operation == "BYGENRE":
                byGenre = pickle.load(writer_obj)
                search = str(byGenre.genre).capitalize
                try:
                    byGenre.result = dataset[search]
                except Exception as e:
                    self.print_gui_message(f"Error from query: {e}")
                self.print_gui_message(f"{byGenre.result}")

                # stuur genre door
                pickle.dump(byGenre.result, writer_obj)
                writer_obj.flush()
                self.print_gui_message(f"Sending operation results")

                operation = pickle.load(writer_obj)

            while operation == "BYCOMPANY":
                byCompany = pickle.load(writer_obj)
                search = str(byCompany.genre).capitalize
                try:
                    result = dataset[search]
                except Exception as e:
                    self.print_gui_message(f"Error from query: {e}")
                self.print_gui_message(f"{byCompany.result}")

                # stuur resultaat door
                pickle.dump(byCompany.result, writer_obj)
                writer_obj.flush()
                self.print_gui_message(f"Sending operation results")

                operation = pickle.load(writer_obj)

        self.print_gui_message(f"Connection closed")
        self.socket_to_client.close()

    def print_gui_message(self, message):
        self.messages_queue.put(f"CLH {self.id}:> {message}")
