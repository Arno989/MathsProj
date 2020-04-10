import threading
import logging
import pickle


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

        while operation != "C":
            berekening = pickle.load(writer_obj)

            pickle.dump(berekening, writer_obj)
            writer_obj.flush()

            self.print_gui_message(f"Sending operation results")

            operation = pickle.load(writer_obj)

        self.print_gui_message(f"Connection closed")
        self.socket_to_client.close()

    def print_gui_message(self, message):
        self.messages_queue.put(f"CLH {self.id}:> {message}")
