import logging
import socket
import os
import sys
from queue import Queue
from threading import Thread
import tkinter as tk
from tkinter import *
import pickle
import numpy as np
import pandas as pd
from tkinter import messagebox, ttk
#fix relative path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
sys.path.insert(0, BASE_DIR)
jsonDb = f"{PROJECT_ROOT}\\data\\users.json"

from server.multithreader import Movie_thread
from data.moderator import Online_users



import json
from pathlib import Path
from server.dbHandler import get_json_file_contents
from data.movie import User

#font
LARGE_FONT = ("Verdana", 12)



class ServerWindow(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Voeg elke pagina hieraan toe
        for F in (
            ServerLog,
            OverviewOnlineUsers,
            OverviewAskedSearch,
            OverviewUsers,
            SendMessage,
            PopularitieOffSearch,
        ):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(ServerLog)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class OverviewOnlineUsers(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Overview Online Users", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        label1 = tk.Label(self, text="Search History")
        label1.pack(pady=3, padx=10)

        #show table
        self.show_table()

        self.getOnlineUsers()

        btnShowUserInfo = tk.Button(
            self, text="Show Info About Selected User", command=lambda: self.get_userinfo())
        btnShowUserInfo.pack(ipady=10, ipadx=150, pady=3,padx=(10,0),fill="x")

        btnShowHistory = tk.Button(
            self, text="Show Search History Off Selected User", command=lambda: self.search_history())
        btnShowHistory.pack(ipady=10, ipadx=150, pady=3,padx=(10,0),fill="x")

        btnHome = tk.Button(
            self, text="Back To Home", command=lambda: controller.show_frame(ServerLog)
        )
        btnHome.pack(ipady=10, ipadx=150, pady=3,padx=(10,0),fill="x")
    
    def getOnlineUsers(self):
        users= Online_users.users_online()
        
        label2 = tk.Label(self, text="Users")
        label2.pack(pady=(2,1), padx=10)

        # Create combobox
        self.cbo_onlineUsers = ttk.Combobox(self, state="readonly", width=40)
        self.cbo_onlineUsers["values"] = users
        self.cbo_onlineUsers.pack(pady=(5,5),padx=(10,0),fill="x")

    def get_userinfo(self):
        #get all the users
        all_users = get_json_file_contents(jsonDb)
        # get the selected item off the treeview
        selected_item  = str(self.cbo_onlineUsers.get())
        # Check if selected an item before clicked on the button 
        if len(selected_item)!=0:
            selected_username=selected_item
            for u in all_users:
                if u['username'] == selected_username:
                    tk.messagebox.showinfo(f"Selected name {u['name']}",f"Name: {u['name']}\nUsername: {u['username']}\nEmail: {u['email']}")

        else:
            tk.messagebox.showinfo("get_userinfo", "select user before push the button")
    def show_table(self):
        # Show treeview
        self.tk_table = ttk.Treeview(self)

        # Scroll Vertical
        scrolly = ttk.Scrollbar(self, orient=VERTICAL, command=self.tk_table.yview)
        scrolly.pack(side=RIGHT, ipady=150,pady=(0,230))
        self.tk_table.configure(yscrollcommand=scrolly.set)

        self.tk_table["height"] = 17

        self.tk_table.pack(fill="x",padx=(10,0))
    def search_history(self):
        print("search history moet nog aangemaakt worden")





class OverviewUsers(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
   
        label = tk.Label(self, text="Overview Users", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.showUsers()

        btnGet_userInfo = tk.Button(
            self, text="Show info about selected user", command=self.get_userinfo)
        btnGet_userInfo.pack(ipady=10, ipadx=150, pady=3,padx=(10,0),fill="x")
     

        btnHome = tk.Button(
            self, text="Back To Home", command=lambda: controller.show_frame(ServerLog)
        )
        btnHome.pack(ipady=10, ipadx=150, pady=3,padx=(10,0),fill="x")

        

        

     
    def showUsers(self):
        try:
            # Show treeview
            self.tk_table = ttk.Treeview(self)

            # Scroll Vertical
            scrolly = ttk.Scrollbar(self, orient=VERTICAL, command=self.tk_table.yview)
            scrolly.pack(side=RIGHT, ipady=150,pady=(0,230))
            self.tk_table.configure(yscrollcommand=scrolly.set)

            self.tk_table["height"] = 17

            self.tk_table["show"] = "headings"

            # add each colum in columns
            columns = ["Username"]

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
                    "",
                    tk.END,
                    values=(each_rec["username"]),
                )

            self.tk_table.pack(fill="x",padx=(10,0))
            
        
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("show users", "Something has gone wrong...")
        
    def get_userinfo(self):
        #get all the users
        all_users = get_json_file_contents(jsonDb)
        # get the selected item off the treeview
        selected_item  = self.tk_table.selection()[0]
        # Check if selected an item before clicked on the button 
        if len(selected_item)!=0:
            selected_username=self.tk_table.item(selected_item)['values'][0]
            for u in all_users:
                if u['username'] == selected_username:
                    tk.messagebox.showinfo(f"Selected name {u['name']}",f"Name: {u['name']}\nUsername: {u['username']}\nEmail: {u['email']}")

        else:
            tk.messagebox.showinfo("get_userinfo", "select user before push the button")
    
    
        

class OverviewAskedSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # per client een nieuwe tabel

        label = tk.Label(self, text="Overview Asked Search", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        btnHome = tk.Button(
            self, text="Back To Home", command=lambda: controller.show_frame(ServerLog)
        )
        btnHome.pack(ipady=10, ipadx=150, pady=10)


class SendMessage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
    
        label = tk.Label(self, text="Send Message To Users", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.input_message()

        btnMessageToSend = tk.Button(
            self, text="Send Message", command=self.sendMessageToUsers)
        btnMessageToSend.pack(ipady=10, ipadx=150, pady=3,padx=(10,0),fill="x")

        btnHome = tk.Button(
            self, text="Back To Home", command=lambda: controller.show_frame(ServerLog)
        )
        btnHome.pack(ipady=10, ipadx=150, pady=3,padx=(10,0),fill="x")

    
    def input_message(self):
        #textarea aanmaken | scrollbar
        S = tk.Scrollbar(self)
        self.T = tk.Text(self, height=20, width=50)
        S.pack(side=RIGHT, fill="y")
        self.T.pack(fill="x")
        S.config(command=self.T.yview)
        self.T.config(yscrollcommand=S.set)
        
        
    def sendMessageToUsers(self):
        #print van begin tot eind
        message = self.T.get("1.0",tk.END)
        messegaLen = len(message)
        #if message is empty
        if messegaLen == 1:
            tk.messagebox.showinfo(f"Send message",f" Write something !!!")
        else:
            print(message)
            tk.messagebox.showinfo(f"Send message",f" Message sended to users !")
            ## komt nog code om te verzenden mss in class --> !!



class PopularitieOffSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # per client een nieuwe tabel

        label = tk.Label(self, text="Overview Popularitie Off Search", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        btnHome = tk.Button(
            self, text="Back To Home", command=lambda: controller.show_frame(ServerLog)
        )
        btnHome.pack(ipady=10, ipadx=150, pady=10)


class ServerLog(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.init_window()
        self.init_messages_queue()
        self.init_server()
        btnOnlineUsers = tk.Button(
            self,
            text="Online Users",
            command=lambda: controller.show_frame(OverviewOnlineUsers),
        )
        btnOnlineUsers.grid(
            row=4,
            column=0,
            columnspan=3,
            pady=(0, 5),
            padx=(5, 5),
            sticky=N + S + E + W,
        )

        btnUsers = tk.Button(
            self,
            text="Overview Users",
            command=lambda: controller.show_frame(OverviewUsers),
        )
        btnUsers.grid(
            row=5,
            column=0,
            columnspan=3,
            pady=(0, 5),
            padx=(5, 5),
            sticky=N + S + E + W,
        )

        btnSendMessage = tk.Button(
            self,
            text="Send Message",
            command=lambda: controller.show_frame(SendMessage),
        )
        btnSendMessage.grid(
            row=7,
            column=0,
            columnspan=3,
            pady=(0, 5),
            padx=(5, 5),
            sticky=N + S + E + W,
        )

        btnPopularitieOffSearch = tk.Button(
            self,
            text="Popularity Off Searches",
            command=lambda: controller.show_frame(PopularitieOffSearch),
        )
        btnPopularitieOffSearch.grid(
            row=8,
            column=0,
            columnspan=3,
            pady=(0, 5),
            padx=(5, 5),
            sticky=N + S + E + W,
        )

        # self.btnHome = Button(self, text="Back To Home",  command=lambda:controller.show_frame(HomePage))
        # self.btnHome.grid(row=4, column=0, columnspan=3, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)


    def init_window(self):
        # self.master.title("Server")
        # self.pack(fill=BOTH, expand=1)

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
