import threading
import logging
import pickle
import pandas as pd
import numpy as np


import sys

#sys.path.insert(0, "./")

dataset = pd.read_csv('./data/movies.csv', encoding='ISO-8859-1')
print(dataset)

#df = pd.read_csv(
#    "C:\Users\Ouassim Boutalliss\OneDrive - Hogeschool West-Vlaanderen\2deJaar\S4\Advanced Programming Maths\Project\MathsProj\server\movies.csv", encoding="ISO-8859-1"
#)

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

        # voorbeeld Stopafstand berekenen
        while (operation != "C") and (operation == "STOPAFSTAND"):
            berekening = pickle.load(writer_obj)

            # omzeting naar int
            snelheid = int(berekening.snelheid)
            reactietijd = int(berekening.reactietijd)

            #Omzetting van Km/u naar m/s
            snelheid = (snelheid / 3.6) 

            #remvertraging berekenen
            if berekening.wegdek == "Droog wegdek":
                remvertraging = 8
            if berekening.wegdek == "Nat wegdek":
                remvertraging = 5

            #Berekening
            berekening.stopafstand = snelheid * reactietijd + (snelheid*snelheid) / (2*remvertraging)
            

            pickle.dump(berekening, writer_obj)
            writer_obj.flush()

            self.print_gui_message(f"Sending operation results")

            operation = pickle.load(writer_obj)

        # Search by genre
        while (operation != "C") and (operation == "BYGENRE"):
            # je krijgt de genre binnen
            genre = pickle.load(writer_obj)

            search = str(genre.genre)

            ##########Fout ligt aan genre hierboven !!
            #genre.resultaat = dataset[dataset.genre == genre]

            #result(.-> vind je terug in map data -> movie -> opzoek naar element waar None bij staat  ))
            genre.resultaat = dataset[dataset.genre == search]
            self.print_gui_message(f"{genre.resultaat}")

            #stuur genre door
            pickle.dump(genre, writer_obj)
            writer_obj.flush()

            self.print_gui_message(f"Sending operation results")

            operation = pickle.load(writer_obj)

        self.print_gui_message(f"Connection closed")
        self.socket_to_client.close()

    def print_gui_message(self, message):
        self.messages_queue.put(f"CLH {self.id}:> {message}")
