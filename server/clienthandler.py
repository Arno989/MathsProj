import threading
import logging
import pickle


class ClientHandler(threading.Thread):

    numbers_clienthandlers = 0

    def __init__(self, socketclient,messages_queue):
        threading.Thread.__init__(self)
        #connectie with client
        self.socket_to_client = socketclient
        #message queue -> link to gui server
        self.messages_queue = messages_queue
        #id clienthandler
        self.id = ClientHandler.numbers_clienthandlers
        ClientHandler.numbers_clienthandlers += 1

    def run(self):
        my_writer_obj = self.socket_to_client.makefile(mode='rwb')

        self.print_bericht_gui_server("Waiting for inputs...")
        whatTodo = pickle.load(my_writer_obj)
        print(whatTodo)

        while (whatTodo != "C"):
            berekening = pickle.load(my_writer_obj)
            print(berekening)
          
      
            

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
            
            pickle.dump(berekening, my_writer_obj)
            my_writer_obj.flush()

            self.print_bericht_gui_server("Sending stopafstand %d back" % berekening.stopafstand)

            whatTodo = pickle.load(my_writer_obj)

        self.print_bericht_gui_server("Connection closed with client")
        self.socket_to_client.close()

    def print_bericht_gui_server(self, message):
        self.messages_queue.put("CLH %d:> %s" % (self.id, message))

