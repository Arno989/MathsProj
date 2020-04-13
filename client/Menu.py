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

from movie import Stopafstand, ByCompany, ByGenre
 

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
        for F in (HomePage, pageByGenre, pageByName,pageByCompany):

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
                            command=lambda: controller.show_frame(pageByGenre))
        btnByGenre.pack(side=LEFT)

        btnByName = tk.Button(self, text="By Name",
                            command=lambda: controller.show_frame(pageByName))
        btnByName.pack(side=LEFT)

        btnByCompany = tk.Button(self, text="By Company",
                            command=lambda: controller.show_frame(pageByCompany))
        btnByCompany.pack(side=LEFT)

        


    



class pageByGenre(tk.Frame):
    

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

            #search.result = pd.set_option('display.max_rows',None)
            #search.result = pd.set_option('display.max_columns',15)
            #search.result = pd.set_option('display.width',None)

            self.tk_table['height'] = 20

            self.tk_table['show'] = 'headings'
            
            ## display columns
            self.tk_table['columns'] = search.result.columns

            indexx = 1 # niet 0 omdat je de eerte kolom niet kunt gebruiken 
            for col in search.result.columns.values:
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



class pageByCompany(tk.Frame):
    

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        # Make connection
        self.makeConnnectionWithServer()

        Title = tk.Label(self, text="Search By Company", font=LARGE_FONT)
        Title.pack()

        label = tk.Label(self, text="Company:")
        label.pack()

        self.entry_company = tk.Entry(self)
        self.entry_company.pack()
    

        btnSearch = tk.Button(self, text="Search",
                            command=self.searchByCompany)
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
            messagebox.showinfo("byCompany - foutmelding", "Something has gone wrong...")
    
        
    
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
            messagebox.showinfo("byCompany - foutmelding", "Something has gone wrong...")
    
    def searchByCompany(self):
        try:
            #send BYCOMPANY to clienthandler
            pickle.dump("BYCOMPANY", self.my_writer_obj)

            
            company = str(self.entry_company.get())
            print(company)
           
            #add to  klasse 
            search = ByCompany(company)
            pickle.dump(search, self.my_writer_obj)
            self.my_writer_obj.flush()

            # waiting for answer
            search = pickle.load(self.my_writer_obj)
            print(search)
            print(search.result.values)

            self.tk_table['height'] = 20

            self.tk_table['show'] = 'headings'
            
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
            messagebox.showinfo("byCompany", "Something has gone wrong...")

    def close_connection(self):
        try:
            logging.info("Close connection with server...")
            pickle.dump("C", self.my_writer_obj)
        
            self.my_writer_obj.flush()
            self.socket_to_server.close()
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("byCompany", "Something has gone wrong...")

class pageByName(tk.Frame):
    

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        # Make connection
        self.makeConnnectionWithServer()

        Title = tk.Label(self, text="Search By Name", font=LARGE_FONT)
        Title.pack()

        label = tk.Label(self, text="Name:")
        label.pack()

        self.entry_name = tk.Entry(self)
        self.entry_name.pack()
    

        btnSearch = tk.Button(self, text="Search",
                            command=self.searchByName)
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
            messagebox.showinfo("byName - foutmelding", "Something has gone wrong...")
    
        
    
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
            messagebox.showinfo("byName - foutmelding", "Something has gone wrong...")
    
    def searchByName(self):
        try:
            #send BYNAME to clienthandler
            pickle.dump("BYNAME", self.my_writer_obj)

            
            name = str(self.entry_name.get())
            print(name)
           
            #Voeg name toe aan klasse 
            search = ByName(name)
            pickle.dump(search, self.my_writer_obj)
            self.my_writer_obj.flush()

            # waiting for answer
            search = pickle.load(self.my_writer_obj)
            print(search.result.columns)

            self.tk_table['height'] = 20

            self.tk_table['show'] = 'headings'
            
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
            messagebox.showinfo("byName", "Something has gone wrong...")

    def close_connection(self):
        try:
            logging.info("Close connection with server...")
            pickle.dump("C", self.my_writer_obj)
        
            self.my_writer_obj.flush()
            self.socket_to_server.close()
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("byName", "Something has gone wrong...")


logging.basicConfig(level=logging.INFO)

app = Movies()
app.geometry("600x600")
app.mainloop()
