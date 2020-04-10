from tkinter import *

import tkinter as tk

import logging
import socket
import pickle



from tkinter import messagebox


from stopafstand import Stopafstand


LARGE_FONT= ("Verdana", 12)


class Movies(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Voeg elke pagina hieraan toe 
        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        
        

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="HOME", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        btnByGenre = tk.Button(self, text="By Genre",
                            command=lambda: controller.show_frame(PageOne))
        btnByGenre.pack()

        btnByCountry = tk.Button(self, text="By Country",
                            command=lambda: controller.show_frame(PageTwo))
        btnByCountry.pack()

    



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Title = tk.Label(self, text="Search By Genre", font=LARGE_FONT)
        Title.pack(pady=10,padx=10)

        label = tk.Label(self, text="Genre:")
        label.pack()

        entry_genre = tk.Entry(self, width=40)
        entry_genre.pack()
    

        btnSearch = tk.Button(self, text="Search",
                            command=self.searchByGenre)
        btnSearch.pack()

        btnHome = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        btnHome.pack()


        labelResultaat = tk.Label(self, text="resultaat")
        labelResultaat.pack()

        self.label_resultaat = tk.Label(self, anchor='w')
        self.label_resultaat.pack()


    def searchByGenre(self):

        self.label_resultaat['text'] = "Gelukt !!!"



class PageTwo(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Make connection
        self.makeConnnectionWithServer()

        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        self.entry_snelheid = tk.Entry(self, width=40)
        self.entry_snelheid.pack()

        self.entry_reactietijd = tk.Entry(self, width=40)
        self.entry_reactietijd.pack()

        self.entry_wegdek = tk.Entry(self, width=40)
        self.entry_wegdek.pack()


        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Bereken",
                            command=self.calculateStopafstand)
        button2.pack()

        self.label_resultaat = tk.Label(self, anchor='w')
        self.label_resultaat.pack()

    
    def __del__(self):
        self.close_connection()
    
    def makeConnnectionWithServer(self):
        try:
            logging.info("Making connection with server...")
            # get local machine name
            host = socket.gethostname()
            port = 9999
            self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connection to hostname on the port.
            self.socket_to_server.connect((host, port))
            self.my_writer_obj = self.socket_to_server.makefile(mode='rwb')
            logging.info("Open connection with server succesfully")
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("Stopafstand - foutmelding", "Something has gone wrong...")
    
    def calculateStopafstand(self):
        try:
            pickle.dump("STOPAFSTAND", self.my_writer_obj)

            snelheid = int(self.entry_snelheid.get())
            reactietijd = int(self.entry_reactietijd.get())
            wegdek = str(self.entry_wegdek.get())
            
            berekening = Stopafstand(snelheid,reactietijd,wegdek)
            pickle.dump(berekening, self.my_writer_obj)
            self.my_writer_obj.flush()


            # waiting for answer
            berekening = pickle.load(self.my_writer_obj)
            self.label_resultaat['text'] = "{0}".format(berekening.stopafstand)
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("Stopafstand", "Something has gone wrong...")

    def close_connection(self):
        try:
            logging.info("Close connection with server...")
            pickle.dump("C", self.my_writer_obj)
        
            self.my_writer_obj.flush()
            self.socket_to_server.close()
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("stopafstand", "Something has gone wrong...")

logging.basicConfig(level=logging.INFO)

app = Movies()
app.mainloop()