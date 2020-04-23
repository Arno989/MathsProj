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
from server.moderator import users_online,user_message,search_popularity


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
            OverviewUsers,
            SendMessage,
            PopularityOfSearch,
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

        
        #combobox of online users
        self.show_cbo()

        label3 = tk.Label(self, text="First Click On Get Online Users Button")
        label3.pack(pady=(2,1), padx=10)

        btngetOnlineUsers = tk.Button(
            self, text="Get Online Users", command=self.getOnlineUsers)
        btngetOnlineUsers.pack(ipady=10, ipadx=150, pady=3,padx=(10,0),fill="x")

        btnShowUserInfo = tk.Button(
            self, text="Show Info About Selected User", command=lambda: self.get_userinfo())
        btnShowUserInfo.pack(ipady=10, ipadx=150, pady=3,padx=(10,0),fill="x")

        btnShowHistory = tk.Button(
            self, text="Show Search History Of Selected User", command=lambda: self.search_history())
        btnShowHistory.pack(ipady=10, ipadx=150, pady=3,padx=(10,0),fill="x")

        btnHome = tk.Button(
            self, text="Back To Home", command=lambda: controller.show_frame(ServerLog)
        )
        btnHome.pack(ipady=10, ipadx=150, pady=3,padx=(10,0),fill="x")
    
    def show_cbo(self):
        
        
        label2 = tk.Label(self, text="Users")
        label2.pack(pady=(2,1), padx=10)

        # Create combobox
        self.cbo_onlineUsers = ttk.Combobox(self, state="readonly", width=40)
        
        self.cbo_onlineUsers.pack(pady=(5,5),padx=(10,0),fill="x")


    def getOnlineUsers(self):
        self.cbo_onlineUsers.set("")
        users= users_online().getUsers()
        print(users)

        #inser users
        self.cbo_onlineUsers["values"] = users
        

    def get_userinfo(self):
        #get all the users
        all_users = get_json_file_contents(jsonDb)
        # get the selected item of the treeview
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
            columns = ["Searches","Parameter"]

            # display columns
            self.tk_table["columns"] = columns

            indexx = 1  # niet 0 omdat je de eerte kolom niet kunt gebruiken
            for col in columns:
                self.tk_table.heading(f"#{indexx}", text=col)
                indexx += 1

            self.tk_table.pack(fill="x",padx=(10,0))
            
        
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("show searches of user", "Something has gone wrong...")


    def search_history(self):
        if self.cbo_onlineUsers.get()=="":
            tk.messagebox.showinfo("Info","You need to select a user first")
        else:
            #clear the treeview before show data
            for i in self.tk_table.get_children():
                self.tk_table.delete(i)
            print("search history moet nog aangemaakt worden")
            
            #here insert table
            user = self.cbo_onlineUsers.get()
            print(f"toon zoekgeschiedenis van {user}")
            try:
                all_searches = search_popularity().getSearches(user)
                print(all_searches)
                #Display rows
                for each_rec in all_searches:
                    self.tk_table.insert(
                        "",
                        tk.END,
                        values=(each_rec["query"],each_rec["parameters"]),
                    )
            except Exception as ex:
                logging.error("Foutmelding: %s" % ex)
                messagebox.showinfo("insert data popularity", "Something has gone wrong...")




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
        # get the selected item of the treeview
        selected_item  = self.tk_table.selection()[0]
        # Check if selected an item before clicked on the button 
        if len(selected_item)!=0:
            selected_username=self.tk_table.item(selected_item)['values'][0]
            for u in all_users:
                if u['username'] == selected_username:
                    tk.messagebox.showinfo(f"Selected name {u['name']}",f"Name: {u['name']}\nUsername: {u['username']}\nEmail: {u['email']}")

        else:
            tk.messagebox.showinfo("get_userinfo", "select user before push the button")


class SendMessage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
    
        label = tk.Label(self, text="Send Message To Users", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        label4 = tk.Label(self, text="MessageBox")
        label4.pack(pady=(2,1), padx=10)

        self.input_message()
        
        

        btnMessageToSend = tk.Button(
            self, text="Send Message To All", command=self.sendMessageToAllUsers)
        btnMessageToSend.pack(ipady=10, ipadx=150, pady=3,padx=(10,0),fill="x")

        self.show_cbo()

        label3 = tk.Label(self, text="First Click On Get Online Users Button")
        label3.pack(pady=(2,1), padx=10)

        btngetOnlineUsers = tk.Button(
            self, text="Get Online Users", command=self.getOnlineUsers)
        btngetOnlineUsers.pack(ipady=10, ipadx=150, pady=3,padx=(10,0),fill="x")

        btnMessageToSendUser = tk.Button(
            self, text="Send Message To Selected User", command=self.sendMessageToUser)
        btnMessageToSendUser.pack(ipady=10, ipadx=150, pady=3,padx=(10,0),fill="x")

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

    def show_cbo(self):
        

        label2 = tk.Label(self, text="Online users")
        label2.pack(pady=(2,1), padx=10)

        #Create combobox
        self.cbo_onlineUsers = ttk.Combobox(self, state="readonly", width=40)
        self.cbo_onlineUsers.pack(pady=(5,5),padx=(10,0),fill="x")

    def getOnlineUsers(self):
        self.cbo_onlineUsers.set("")
        users= users_online().getUsers()

        #fill combobox
        self.cbo_onlineUsers["values"] = users
       
        
        
    def sendMessageToAllUsers(self):
        #print van begin tot eind
        message = self.T.get("1.0",tk.END)
        messageLen = len(message)
        #if message is empty
        if messageLen == 1:
            tk.messagebox.showinfo(f"Send message",f" Write something !!!")
            self.cbo_onlineUsers.set("")
        else:
            #Clear the textbox
            self.T.delete('1.0', tk.END)
            self.cbo_onlineUsers.set("")
            tk.messagebox.showinfo(f"Send message",f" Message sended to users !")
            ## send the message to all users
            print(message)
            user_message().sendmessage(message)
    
    def sendMessageToUser(self):
        #print van begin tot eind
        message = self.T.get("1.0",tk.END)
        messageLen = len(message)
        selected_user = str(self.cbo_onlineUsers.get())
        #if message is empty
        if messageLen == 1:
            tk.messagebox.showinfo(f"Send message",f" Write something !!!")
            self.cbo_onlineUsers.set("")
            
        else:
            print(message)
            tk.messagebox.showinfo(f"Send message",f" Message sended to {selected_user} !")
            self.cbo_onlineUsers.set("")
            #clear the textbox
            self.T.delete('1.0', tk.END)
            ## send message to user
            user_message().sendmessage(message,selected_user)




class PopularityOfSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # per client een nieuwe tabel

        label = tk.Label(self, text="Overview Popularity Of Searches", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        #treeview
        self.showPopularity()

        btnShowData = tk.Button(
            self, text="Show Popularity", command=self.insert_data
        )
        btnShowData.pack(ipady=10, ipadx=150, pady=3,padx=(10,0),fill="x")

        btnHome = tk.Button(
            self, text="Back To Home", command=lambda: controller.show_frame(ServerLog)
        )
        btnHome.pack(ipady=10, ipadx=150, pady=3,padx=(10,0),fill="x")

        
    def showPopularity(self):
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
            columns = ["Searches","Parameter","Times Requested"]

            # display columns
            self.tk_table["columns"] = columns

            indexx = 1  # niet 0 omdat je de eerte kolom niet kunt gebruiken
            for col in columns:
                self.tk_table.heading(f"#{indexx}", text=col)
                indexx += 1

         

            self.tk_table.pack(fill="x",padx=(10,0))
            
        
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("show popularity searches", "Something has gone wrong...")
    
    def insert_data(self):
        #clear the treeview before show data
        for i in self.tk_table.get_children():
            self.tk_table.delete(i)
        try: 
            print("getting searches")
            all_searches = search_popularity().getSearches()
            print(all_searches)
            #Display rows
            for query in all_searches:
                self.tk_table.insert(
                    "",
                    tk.END,
                    values=(query.keys()[0], query[query.keys()[1]],query[query.keys()[0]]), # not dynamic to format change but will have to do
                )
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            print(ex)
            messagebox.showinfo("insert data popularity", "Something has gone wrong...")
    

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

        btnPopularitieOfSearch = tk.Button(
            self,
            text="Popularity Of Searches",
            command=lambda: controller.show_frame(PopularityOfSearch),
        )
        btnPopularitieOfSearch.grid(
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
