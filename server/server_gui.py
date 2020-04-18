import logging
import socket
from queue import Queue
from threading import Thread
import tkinter as tk
from tkinter import *
import pickle
import numpy as np
import pandas as pd
from tkinter import messagebox, ttk

from multithreader import Movie_thread

import json
from pathlib import Path
from dbHandler import get_json_file_contents
from data.movie import User


import os 
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
sys.path.insert(0, BASE_DIR)
jsonDb = f"{PROJECT_ROOT}\\data\\users.json"



LARGE_FONT= ("Verdana", 12)


class ServerWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}

        # Voeg elke pagina hieraan toe 
        for F in (ServerLog,OverviewOnlineUsers,OverviewAskedSearch,OverviewUsers,SendMessage,PopularitieOffSearch):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(ServerLog)
        
        

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()



class OverviewOnlineUsers(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)


        label = tk.Label(self, text="Overview Online Users", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
    

       

        btnHome = tk.Button(self, text="Back To Home",
                            command=lambda: controller.show_frame(ServerLog))
        btnHome.pack(ipady=10,ipadx=150,pady=10)



        

class OverviewUsers(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)



        label = tk.Label(self, text="Overview Users", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        btnHome = tk.Button(self, text="Back To Home",
                            command=lambda: controller.show_frame(ServerLog))
        btnHome.pack(ipady=10,ipadx=150,pady=10)

       
        self.showUsers()
      
        
                
    def showUsers(self):
        try:
            # Show treeview
            self.tk_table = ttk.Treeview(self)

            # Scroll Vertical
            scrolly = ttk.Scrollbar(self, orient=VERTICAL, command=self.tk_table.yview)
            scrolly.pack(side=RIGHT, fill="y")
            self.tk_table.configure(yscrollcommand=scrolly.set)

            # Scroll Horizontal -> treeview
            scroll = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.tk_table.xview)
            scroll.pack(side=BOTTOM, fill="x")
            self.tk_table.configure(xscrollcommand=scroll.set)


            self.tk_table["height"] = 17

            self.tk_table["show"] = "headings"

            # add each colum in columns
            columns = ["name","username","email"]
            
            

            # display columns
            self.tk_table["columns"] = columns

            indexx = 1  # niet 0 omdat je de eerte kolom niet kunt gebruiken
            for col in columns:
                self.tk_table.heading(f"#{indexx}", text=col)
                indexx += 1
            
            all_users = get_json_file_contents(jsonDb)
            # Display rows
            for each_rec in all_users:
                self.tk_table.insert(
                    "", tk.END, values=(each_rec["name"],each_rec["username"],each_rec["email"])
                )

            self.tk_table.pack()
        
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("signIn", "Something has gone wrong...")

            

        

        

       

        # Display rows
        
        #self.tk_table.insert(
        #    "", tk.END, values=(all_users["name"],all_users["username"],all_users["email"]))

        

class OverviewAskedSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        #per client een nieuwe tabel

        label = tk.Label(self, text="Overview Asked Search", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        btnHome = tk.Button(self, text="Back To Home",
                            command=lambda: controller.show_frame(ServerLog))
        btnHome.pack(ipady=10,ipadx=150,pady=10)

   
   
class SendMessage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        #per client een nieuwe tabel

        label = tk.Label(self, text="Send Message To All The Users", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        btnHome = tk.Button(self, text="Back To Home",
                            command=lambda: controller.show_frame(ServerLog))
        btnHome.pack(ipady=10,ipadx=150,pady=10)



class PopularitieOffSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        #per client een nieuwe tabel

        label = tk.Label(self, text="Overview Popularitie Off Search", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        btnHome = tk.Button(self, text="Back To Home",
                            command=lambda: controller.show_frame(ServerLog))
        btnHome.pack(ipady=10,ipadx=150,pady=10)
        


class ServerLog(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
      
        self.init_window()
        self.init_messages_queue()
        self.init_server()


        btnOnlineUsers = tk.Button(self, text="Online Users",
                            command=lambda: controller.show_frame(OverviewOnlineUsers))
        btnOnlineUsers.grid(row=4, column=0, columnspan=3, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

        btnUsers = tk.Button(self, text="Overview Users",
                            command=lambda: controller.show_frame(OverviewUsers))
        btnUsers.grid(row=5, column=0, columnspan=3, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)


        btnOverviewAskedSearch = tk.Button(self, text="Overview Off Asked Search",
                            command=lambda: controller.show_frame(OverviewAskedSearch))
        btnOverviewAskedSearch.grid(row=6, column=0, columnspan=3, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

        btnSendMessage = tk.Button(self, text="Send Message",
                            command=lambda: controller.show_frame(SendMessage))
        btnSendMessage.grid(row=7, column=0, columnspan=3, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

        btnPopularitieOffSearch = tk.Button(self, text="Popularitie Off Search",
                            command=lambda: controller.show_frame(PopularitieOffSearch))
        btnPopularitieOffSearch.grid(row=8, column=0, columnspan=3, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)


        #self.btnHome = Button(self, text="Back To Home",  command=lambda:controller.show_frame(HomePage))
        #self.btnHome.grid(row=4, column=0, columnspan=3, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)



    def init_window(self):
        #self.master.title("Server")
        #self.pack(fill=BOTH, expand=1)

        Label(self, text="Server log: ").grid(row=0)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)

        self.lstnumbers = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstnumbers.yview)
        self.lstnumbers.grid(row=1, column=0, sticky=N + S + E + W)
        self.scrollbar.grid(row=1, column=1, sticky=N + S)

        self.btn_text = StringVar()
        self.btn_text.set("Start server")
        self.buttonServer = Button(
            self, textvariable=self.btn_text, command=self.start_stop_server
        )
        self.buttonServer.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=(5, 5),
            padx=(5, 5),
            sticky=N + S + E + W,
        )

        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

    def init_server(self):
        self.server = Movie_thread(socket.gethostname(), 9999, self.messages_queue)

    def close(self):
        if self.server != None:
            self.server.close_server_socket()

    def print_messsages_from_queue(self):
        message = self.messages_queue.get()
        while message != "CLOSING SERVER":
            self.lstnumbers.insert(END, message)
            self.messages_queue.task_done()
            message = self.messages_queue.get()
        print("Queue stopped")

    def init_messages_queue(self):
        self.messages_queue = Queue()
        t = Thread(target=self.print_messsages_from_queue)
        t.start()

    def start_stop_server(self):
        self.__is_connected = False
        if self.server.is_connected == True:
            self.server.close_server_socket()
            self.btn_text.set("Start server")
        else:
            self.server.init_server()
            self.server.start()  # thread!
            self.btn_text.set("Stop server")
