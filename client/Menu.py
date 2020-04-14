import logging
import pickle
import socket
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import pandas as pd
from tkinter import ttk 
import numpy as np

from PIL import ImageTk, Image

#import os
#print(os.getcwd())

#import sys
#sys.path.insert(0, "../")
#from data.movie import Stopafstand, ByGenre

from movie import ByCompany, ByGenre, ByName, BetweenYears
 

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
        for F in (HomePage, pageByGenre, pageByName,pageByCompany, pageBetweenYears,pageGraphScore):

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
        btnByGenre.pack(ipady=10,ipadx=150,pady=10)

        btnByName = tk.Button(self, text="By Name",
                            command=lambda: controller.show_frame(pageByName))
        btnByName.pack(ipady=10,ipadx=150,pady=10)

        btnByCompany = tk.Button(self, text="By Company",
                            command=lambda: controller.show_frame(pageByCompany))
        btnByCompany.pack(ipady=10,ipadx=150,pady=10)

        btnBetweenYears = tk.Button(self, text="Between Years",
                            command=lambda: controller.show_frame(pageBetweenYears))
        btnBetweenYears.pack(ipady=10,ipadx=150,pady=10)

        
        btnGraphScore = tk.Button(self, text="Graph Off Score",
                            command=lambda: controller.show_frame(pageGraphScore))
        btnGraphScore.pack(ipady=10,ipadx=150,pady=10)

        btnreconnect = tk.Button(self, text="Reconnect To Server",
                            command=lambda: makeConnnectionWithServer(self))
        btnreconnect.pack(ipady=10,ipadx=150,pady=10)

        #Wordt verwijderd 
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
         
        


class pageByGenre(tk.Frame):
    

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

       
        # Make connection
        self.makeConnnectionWithServer()

        Title = tk.Label(self, text="Search By Genre", font=LARGE_FONT)
        Title.pack()

        label = tk.Label(self, text="Genre:")
        label.pack()

        #Find genres
        self.findGenres()

        btnSearch = tk.Button(self, text="Search",
                            command=self.searchByGenre)
        btnSearch.pack(pady=5,ipadx=30,ipady=5)

        btnClear = tk.Button(self, text="Clear",
                            command=self.clearTreeview)
        btnClear.pack(pady=5,ipadx=30,ipady=5)

        btnHome = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        btnHome.pack(pady=5,ipadx=30,ipady=5)

        

        #bind with return key 
        #self.entry_genre.bind("<Return>", (lambda event: self.searchByGenre()))

        
        #Show treeview
        self.tk_table = ttk.Treeview(self)

        #Scroll Vertical   
        scrolly = ttk.Scrollbar(self, orient=VERTICAL, command=self.tk_table.yview)
        scrolly.pack(side=RIGHT, fill="y")
        self.tk_table.configure(yscrollcommand=scrolly.set)

        #Scroll Horizontal -> treeview
        scroll = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.tk_table.xview)
        scroll.pack(side=BOTTOM, fill = 'x')
        self.tk_table.configure(xscrollcommand=scroll.set)      

        self.tk_table.pack()


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
    
    def findGenres(self):
        try:
            #get values for combobox
            pickle.dump("BYGENRE-Genre", self.my_writer_obj)
            self.my_writer_obj.flush()

            # waiting for answer
            self.genres = pickle.load(self.my_writer_obj)

            # Each genre go in list choices
            choices =[]
            for each_genre in self.genres:
                choices.append(each_genre)
                
            #Create combobox
            self.cbo_genre = ttk.Combobox(self,state = "readonly", width=40)
            self.cbo_genre['values'] = choices
            self.cbo_genre.pack()

            #self.cbo_genre.bind("<<ComboboxSelected>>", (lambda event: self.searchByGenre())
       
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("byGenre - foutmelding", "Something has gone wrong...")

    def searchByGenre(self):
        try:
            #send BYGENRE to clienthandler
            pickle.dump("BYGENRE", self.my_writer_obj)

            
            genre = str(self.cbo_genre.get())
            print(genre)
           
            #Voef genre toe aan klasse 
            search = ByGenre(genre)
            pickle.dump(search, self.my_writer_obj)
            self.my_writer_obj.flush()

            # waiting for answer
            search = pickle.load(self.my_writer_obj)
            print(search.result.columns)
   
            
            self.tk_table['height'] = 17

            self.tk_table['show'] = 'headings'

       
            #add each colum in columns
            columns = []
            for col in search.result.columns:
                columns.append(col)

            ## display columns
            self.tk_table['columns'] = columns
            
            indexx = 1 # niet 0 omdat je de eerte kolom niet kunt gebruiken 
            for col in search.result.columns.values:
                self.tk_table.heading(f"#{indexx}", text=col)
                indexx += 1
                
        
            # Display rows 
            for each_rec in range(len(search.result.values)):
                self.tk_table.insert("", tk.END, values=list(search.result.values[each_rec]))

                  
           #Change width and high off window
            app.geometry("700x600")

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
        btnSearch.pack(pady=5,ipadx=30,ipady=5)

        btnClear = tk.Button(self, text="Clear",
                            command=self.clearTreeview)
        btnClear.pack(pady=5,ipadx=30,ipady=5)

        btnHome = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        btnHome.pack(pady=5,ipadx=30,ipady=5)

        #Show treeview
        self.tk_table = ttk.Treeview(self)

        #Scroll Vertical   
        scrolly = ttk.Scrollbar(self, orient=VERTICAL, command=self.tk_table.yview)
        scrolly.pack(side=RIGHT, fill="y")
        self.tk_table.configure(yscrollcommand=scrolly.set)

        #Scroll Horizontal -> treeview
        scroll = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.tk_table.xview)
        scroll.pack(side=BOTTOM, fill = 'x')
        self.tk_table.configure(xscrollcommand=scroll.set)      

        self.tk_table.pack()


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

            self.tk_table['height'] = 17

            self.tk_table['show'] = 'headings'
            
            #add each colum in columns
            columns = []
            for col in search.result.columns:
                columns.append(col)

            ## display columns
            self.tk_table['columns'] = columns


            indexx = 1 # niet 0 omdat je de eerte kolom niet kunt gebruiken 
            for col in search.result.columns:
                self.tk_table.heading(f"#{indexx}", text=col)
                indexx += 1  

        
            # Display rows 
            for each_rec in range(len(search.result.values)):
                self.tk_table.insert("", tk.END, values=list(search.result.values[each_rec]))

             #Change width and high off window
            app.geometry("700x600")

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
        btnSearch.pack(pady=5,ipadx=30,ipady=5)

        btnClear = tk.Button(self, text="Clear",
                            command=self.clearTreeview)
        btnClear.pack(pady=5,ipadx=30,ipady=5)

        btnHome = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        btnHome.pack(pady=5,ipadx=30,ipady=5)

        #Show treeview
        self.tk_table = ttk.Treeview(self)

        #Scroll Vertical   
        scrolly = ttk.Scrollbar(self, orient=VERTICAL, command=self.tk_table.yview)
        scrolly.pack(side=RIGHT, fill="y")
        self.tk_table.configure(yscrollcommand=scrolly.set)

        #Scroll Horizontal -> treeview
        scroll = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.tk_table.xview)
        scroll.pack(side=BOTTOM, fill = 'x')
        self.tk_table.configure(xscrollcommand=scroll.set)      

        self.tk_table.pack() 



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

            self.tk_table['height'] = 5

            self.tk_table['show'] = 'headings'
            
            #add each colum in columns
            columns = []
            for col in search.result.columns:
                columns.append(col)

            ## display columns
            self.tk_table['columns'] = columns

            indexx = 1 # niet 0 omdat je de eerte kolom niet kunt gebruiken 
            for col in search.result.columns:
                self.tk_table.heading(f"#{indexx}", text=col)
                indexx += 1  

        
            # Display rows 
            for each_rec in range(len(search.result.values)):
                self.tk_table.insert("", tk.END, values=list(search.result.values[each_rec]))

                  
             #Change width and high off window
            app.geometry("700x450")

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

class pageBetweenYears(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        # Make connection
        self.makeConnnectionWithServer()

        Title = tk.Label(self, text="Search Between Years", font=LARGE_FONT)
        Title.pack()

        label = tk.Label(self, text="year:")
        label.pack()

        

        self.entry_year1 = tk.Entry(self)
        self.entry_year1.pack()

        label2 = tk.Label(self, text="year:")
        label2.pack()

        self.entry_year2 = tk.Entry(self)
        self.entry_year2.pack()
    

        btnSearch = tk.Button(self, text="Search",
                            command=self.searchBetweenYears)
        btnSearch.pack(pady=5,ipadx=30,ipady=5)

        btnClear = tk.Button(self, text="Clear",
                            command=self.clearTreeview)
        btnClear.pack(pady=5,ipadx=30,ipady=5)

        btnHome = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        btnHome.pack(pady=5,ipadx=30,ipady=5)

        #Show treeview
        self.tk_table = ttk.Treeview(self)

        #Scroll Vertical   
        scrolly = ttk.Scrollbar(self, orient=VERTICAL, command=self.tk_table.yview)
        scrolly.pack(side=RIGHT, fill="y")
        self.tk_table.configure(yscrollcommand=scrolly.set)

        #Scroll Horizontal -> treeview
        scroll = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.tk_table.xview)
        scroll.pack(side=BOTTOM, fill = 'x')
        self.tk_table.configure(xscrollcommand=scroll.set)      

        self.tk_table.pack()



    def __del__(self):
        self.close_connection()

    def clearTreeview(self):
        try:
            for i in self.tk_table.get_children():
                self.tk_table.delete(i)


        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("betweenYears - foutmelding", "Something has gone wrong...")
    
        
    
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
            messagebox.showinfo("betweenYears - foutmelding", "Something has gone wrong...")
    
    def searchBetweenYears(self):
        try:
            #send BYNAME to clienthandler
            pickle.dump("BETWEENYEARS", self.my_writer_obj)

            
            year1 = int(self.entry_year1.get())
            year2 = int(self.entry_year2.get())
           
            #Voeg name toe aan klasse 
            search = BetweenYears(year1,year2)
            pickle.dump(search, self.my_writer_obj)
            self.my_writer_obj.flush()

            # waiting for answer
            search = pickle.load(self.my_writer_obj)

            self.tk_table['height'] = 17

            self.tk_table['show'] = 'headings'

             #add each colum in columns
            columns = []
            for col in search.result.columns:
                columns.append(col)

            ## display columns
            self.tk_table['columns'] = columns
            
            #For each col make colum
            indexx = 1 # niet 0 omdat je de eerte kolom niet kunt gebruiken 
            for col in search.result.columns:
                self.tk_table.heading(f"#{indexx}", text=col)
                indexx += 1  


        
            # Display rows 
            for each_rec in range(len(search.result.values)):
                self.tk_table.insert("", tk.END, values=list(search.result.values[each_rec]))

            #Change width and high off window
            app.geometry("700x600")
           

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("betweenYears", "Something has gone wrong...")

    def close_connection(self):
        try:
            logging.info("Close connection with server...")
            pickle.dump("C", self.my_writer_obj)
        
            self.my_writer_obj.flush()
            self.socket_to_server.close()
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("betweenYears", "Something has gone wrong...")


class pageGraphScore(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Make connection
        self.makeConnnectionWithServer()

        Title = tk.Label(self, text="Show Graph Off Score ", font=LARGE_FONT)
        Title.pack()


        btnShowGraph = tk.Button(self, text="Show Graph",
                            command=self.showGraph)
        btnShowGraph.pack(pady=8, ipadx=30,ipady=5)

        btnHome = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(HomePage))
        btnHome.pack(pady=8,ipadx=30,ipady=5)

        #bind with return key 
        btnShowGraph.bind("<Return>", (lambda event: self.showGraph()))

        self.image = tk.Label(self)
        self.image.pack(pady=(5,5),padx=(5,5))
            
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
            messagebox.showinfo("graphScore - foutmelding", "Something has gone wrong...")
    
    def showGraph(self):
        try:
            #get values for combobox
            pickle.dump("GRAPH-SCORE", self.my_writer_obj)
            self.my_writer_obj.flush()
            
            #get image
            answer = pickle.load(self.my_writer_obj)
            number_of_sends = int(answer)

            with open("received_file", "wb+") as f:
                for i in range(0, number_of_sends):
                    data = pickle.load(self.my_writer_obj)
                    f.write(data)

            logging.info('Successfully get the image')
           
            #showing image
            im = Image.open('received_file')
            self.img = ImageTk.PhotoImage(Image.open("received_file"))
            self.image['image'] = self.img


            app.geometry("600x700")
        
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("graphScore - foutmelding", "Something has gone wrong...")

    def close_connection(self):
        try:
            logging.info("Close connection with server...")
            pickle.dump("C", self.my_writer_obj)
        
            self.my_writer_obj.flush()
            self.socket_to_server.close()
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("graphScore", "Something has gone wrong...")



logging.basicConfig(level=logging.INFO)

app = Movies()
app.geometry()
app.mainloop()
