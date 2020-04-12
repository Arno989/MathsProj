import logging
import pickle
import socket
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import pandas as pd
from tkinter import ttk 
import numpy as np

#import os
#print(os.getcwd())

#import sys
#sys.path.insert(0, "../")
#from data.movie import Stopafstand, ByGenre

from movie import Stopafstand
from movie import ByGenre

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
        for F in (HomePage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)
        
        

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    
class HomePage(tk.Frame):

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


        # Make connection
        self.makeConnnectionWithServer()

        Title = tk.Label(self, text="Search By Genre", font=LARGE_FONT)
        Title.pack()

        label = tk.Label(self, text="Genre:")
        label.pack()

        self.entry_genre = tk.Entry(self)
        self.entry_genre.pack()
    

        btnSearch = tk.Button(self, text="Search",
                            command=self.searchByGenre)
        btnSearch.pack()

        btnClear = tk.Button(self, text="Clear",
                            command=self.clearTreeview)
        btnClear.pack()

        btnHome = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        btnHome.pack()

        #Show treeview na het klikken op de knop
        self.tk_table = ttk.Treeview(self)
        self.tk_table.pack()

        #Scroll Horizontal -> treeview
        scroll = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.tk_table.xview)
        scroll.pack(fill = 'x')

        self.tk_table.configure(xscrollcommand=scroll.set)         



    def __del__(self):
        self.close_connection()

    def clearTreeview(self):
        try:
            for i in self.tk_table.get_children():
                self.tk_table.delete(i)


        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("byGenre - foutmelding", "Something has gone wrong...")
    
        
    
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
            messagebox.showinfo("byGenre - foutmelding", "Something has gone wrong...")
    
    def searchByGenre(self):
        try:
            #send BYGENRE to clienthandler
            pickle.dump("BYGENRE", self.my_writer_obj)

            
            genre = str(self.entry_genre.get())
            print(genre)
           
            #Voef genre toe aan klasse 
            search = ByGenre(genre)
            pickle.dump(search, self.my_writer_obj)
            self.my_writer_obj.flush()

            # waiting for answer
            search = pickle.load(self.my_writer_obj)
            print(search.result.columns)

            self.tk_table['height'] = 20
            
            ## display columns
            self.tk_table['columns'] = search.result.columns

            indexx = 1 # niet 0 omdat je de eerte kolom niet kunt gebruiken 
            for col in search.result.columns:
                self.tk_table.heading(f"#{indexx}", text=col)
                indexx += 1  

        
            # Display rows 
            for each_rec in range(len(search.result.columns)):
                self.tk_table.insert("", tk.END, values=list(search.result.values[each_rec]))

                  
            

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("byGenre", "Something has gone wrong...")

    def close_connection(self):
        try:
            logging.info("Close connection with server...")
            pickle.dump("C", self.my_writer_obj)
        
            self.my_writer_obj.flush()
            self.socket_to_server.close()
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("byGenre", "Something has gone wrong...")



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
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()

        button2 = tk.Button(self, text="Bereken",
                            command=self.calculateStopafstand)
        button2.pack()

        self.label_result = tk.Label(self, anchor='w')
        self.label_result.pack()

    
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
            self.label_result['text'] = "{0}".format(berekening.stopafstand)
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
