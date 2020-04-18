import logging
import os
import pickle
import socket
import sys
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk

import numpy as np
import pandas as pd
from PIL import Image, ImageTk

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
sys.path.insert(0, BASE_DIR)

from data.movie import BetweenYears, ByCompany, ByGenre, ByName, User


LARGE_FONT = ("Verdana", 12)


try:
    logging.info("Making connection with server...")
    # get local machine name
    host = socket.gethostname()
    port = 9999
    socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connection to hostname on the port.
    socket_to_server.connect((host, port))
    my_writer_obj = socket_to_server.makefile(mode="rwb")
    socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connection to hostname on the port.
    socket_to_server.connect((host, port))
    logging.info("Open connection with server succesfully")
except Exception as ex:
    logging.error("Foutmelding: %s" % ex)
    messagebox.showinfo("sign Up page - foutmelding", "Something has gone wrong...")


def closeConnection():
    try:
        logging.info("Close connection with server...")
        pickle.dump("C", my_writer_obj)

        my_writer_obj.flush()
        socket_to_server.close()
    except Exception as ex:
        logging.error("Foutmelding: %s" % ex)
        messagebox.showinfo("cose connection", "Something has gone wrong...")


class Movies(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Voeg elke pagina hieraan toe
        for F in (
            pageSignIn,
            pageSignUp,
            HomePage,
            pageByGenre,
            pageByName,
            pageByCompany,
            pageBetweenYears,
            pageGraphScore,
        ):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(pageSignIn)

    def __del__(self):
        closeConnection()

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class pageSignIn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Title = tk.Label(self, text="Login Page", font=LARGE_FONT)
        Title.pack()

        label = tk.Label(self, text="Username:")
        label.pack()

        self.entry_username = tk.Entry(self)
        self.entry_username.pack()

        label1 = tk.Label(self, text="Password:")
        label1.pack()

        self.entry_password = tk.Entry(self)
        self.entry_password.pack()

        btnSignIn = tk.Button(self, text="Sign In", command=self.controleValues)
        btnSignIn.pack(pady=5, ipadx=30, ipady=5)

        btnSignUp = Button(
            self, text="SignUp", command=lambda: controller.show_frame(pageSignUp)
        )
        btnSignUp.pack(pady=5, ipadx=30, ipady=5)

    def __del__(self):
        closeConnection()

    def controleValues(self):
        try:
            # get values from cbo
            username = str(self.entry_username.get())
            password = str(self.entry_password.get())

            # When is empty give warning
            if username == "" or password == "":
                tk.messagebox.showwarning(
                    title="Warning", message="Please fill all the input fields !"
                )
                self.entry_username.focus()
            else:
                # go to function
                self.singIn()

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo(
                "controleGenre - foutmelding", "Something has gone wrong..."
            )

    def signIn(self):
        try:
            # send BYGENRE to clienthandler
            pickle.dump("SIGNIN", my_writer_obj)

            # selected value off combobox
            username = str(self.entry_username.get())
            password = str(self.entry_password.get())

            # Voeg signIn toe aan klasse
            signIn = User(username=username, password=password)
            pickle.dump(signIn, my_writer_obj)
            my_writer_obj.flush()

            # waiting for answer
            signIn = pickle.load(my_writer_obj)
            print(signIn)

            if signIn == True:
                self.HomePage()
            else:
                self.messagebox.showinfo("SignIn", "Login refused")

            self.entry_username.set("")
            self.entry_password.set("")

        # Change width and high off window
        # app.geometry("200x100")

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("signIn", "Something has gone wrong...")


class pageSignUp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Title = tk.Label(self, text="Sign Up", font=LARGE_FONT)
        Title.pack()

        label1 = tk.Label(self, text="Name:")
        label1.pack()
        self.entry_name = tk.Entry(self)
        self.entry_name.pack()

        label2 = tk.Label(self, text="Email:")
        label2.pack()
        self.entry_email = tk.Entry(self)
        self.entry_email.pack()

        label3 = tk.Label(self, text="Username:")
        label3.pack()
        self.entry_username = tk.Entry(self)
        self.entry_username.pack()

        label4 = tk.Label(self, text="Password:")
        label4.pack()
        self.entry_password = tk.Entry(self)
        self.entry_password.pack()

        btnSignUp = tk.Button(self, text="Sign Up", command=self.controleValues)
        btnSignUp.pack(pady=5, ipadx=30, ipady=5)

        label3 = tk.Label(self, text="If u already have an account:")
        label3.pack()
        btnSignIn = tk.Button(
            self, text="Sign In", command=lambda: controller.show_frame(pageSignIn)
        )
        btnSignIn.pack(pady=5, ipadx=30, ipady=5)

    def __del__(self):
        closeConnection()

    def controleValues(self):
        try:
            # get values from cbo
            username = str(self.entry_username.get())
            password = str(self.entry_password.get())
            name = str(self.entry_password.get())
            email = str(self.entry_password.get())

            # When is empty give warning
            if username == "" or password == "" or email == "" or name == "":
                self.messagebox.showwarning(
                    title="Warning", message="Please fill all the input fields !"
                )
                self.entry_name.focus()
            else:
                # go to function
                self.signUp()

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo(
                "controleSignUp- foutmelding", "Something has gone wrong..."
            )

    def signUp(self):
        try:
            # send BYGENRE to clienthandler
            pickle.dump("SIGNUP", my_writer_obj)

            # selected value off combobox
            username = str(self.entry_username.get())
            password = str(self.entry_password.get())
            email = str(self.entry_email.get())
            name = str(self.entry_name.get())

            # Voeg signIn toe aan klasse
            signUp = User(name=name, username=username, email=email, password=password)
            pickle.dump(signUp, my_writer_obj)
            my_writer_obj.flush()

            # waiting for answer
            signUp = pickle.load(my_writer_obj)
            print(signUp)

            if signUp.authenticated == True:
                self.messagebox.showinfo("SignUp", "You are correctly signed up")
                self.HomePage()
            else:
                self.messagebox.showinfo("SignUp", "Refused to sign up")

            self.entry_username.set("")
            self.entry_email.set("")
            self.entry_name.set("")
            self.entry_password.set("")

        # Change width and high off window
        # app.geometry("200x100")

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("signUp", "Something has gone wrong...")


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="HOME", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        btnByGenre = tk.Button(
            self, text="By Genre", command=lambda: controller.show_frame(pageByGenre)
        )
        btnByGenre.pack(ipady=10, ipadx=150, pady=10)

        btnByName = tk.Button(
            self, text="By Name", command=lambda: controller.show_frame(pageByName)
        )
        btnByName.pack(ipady=10, ipadx=150, pady=10)

        btnByCompany = tk.Button(
            self,
            text="By Company",
            command=lambda: controller.show_frame(pageByCompany),
        )
        btnByCompany.pack(ipady=10, ipadx=150, pady=10)

        btnBetweenYears = tk.Button(
            self,
            text="Between Years",
            command=lambda: controller.show_frame(pageBetweenYears),
        )
        btnBetweenYears.pack(ipady=10, ipadx=150, pady=10)

        btnGraphScore = tk.Button(
            self,
            text="Graph Off Score",
            command=lambda: controller.show_frame(pageGraphScore),
        )
        btnGraphScore.pack(ipady=10, ipadx=150, pady=10)

    def __del__(self):
        closeConnection()


class pageByGenre(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Title = tk.Label(self, text="Search By Genre", font=LARGE_FONT)
        Title.pack()

        label = tk.Label(self, text="Genre:")
        label.pack()

        # Find genres
        self.getGenres()

        btnSearch = tk.Button(self, text="Search", command=self.controleValues)
        btnSearch.pack(pady=5, ipadx=30, ipady=5)

        btnClear = tk.Button(self, text="Clear", command=self.clearTreeview)
        btnClear.pack(pady=5, ipadx=30, ipady=5)

        btnHome = tk.Button(
            self, text="Back to Home", command=lambda: controller.show_frame(HomePage)
        )
        btnHome.pack(pady=5, ipadx=30, ipady=5)

        # bind with return key
        # self.entry_genre.bind("<Return>", (lambda event: self.searchByGenre()))

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

        self.tk_table.pack()

    def __del__(self):
        closeConnection()

    def clearTreeview(self):
        try:
            for i in self.tk_table.get_children():
                self.tk_table.delete(i)

            self.cbo_genre.set("")

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("byGenre - foutmelding", "Something has gone wrong...")

    def getGenres(self):
        try:
            # get values for combobox
            pickle.dump("GET_GENRES", my_writer_obj)
            my_writer_obj.flush()

            # waiting for answer
            self.genres = pickle.load(my_writer_obj)

            # Each genre go in list choices
            choices = []
            for each_genre in self.genres:
                choices.append(each_genre)

            # Create combobox
            self.cbo_genre = ttk.Combobox(self, state="readonly", width=40)
            self.cbo_genre["values"] = choices
            self.cbo_genre.pack()

            # self.cbo_genre.bind("<<ComboboxSelected>>", (lambda event: self.searchByGenre())

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("byGenre - foutmelding", "Something has gone wrong...")

    def controleValues(self):
        try:
            # get values from cbo
            genre = str(self.cbo_genre.get())

            # When is empty give warning
            if genre == "":
                tk.messagebox.showwarning(title="Warning", message="Genre is empty !")
                self.cbo_genre.focus()
            else:
                # go to function
                self.searchByGenre()

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo(
                "controleGenre - foutmelding", "Something has gone wrong..."
            )

    def searchByGenre(self):
        try:
            # send BYGENRE to clienthandler
            pickle.dump("BY_GENRE", my_writer_obj)

            # selected value off combobox
            genre = str(self.cbo_genre.get())

            # Voef genre toe aan klasse
            search = ByGenre(genre)
            pickle.dump(search, my_writer_obj)
            my_writer_obj.flush()

            # waiting for answer
            search = pickle.load(my_writer_obj)
            print(search.result.columns)

            self.tk_table["height"] = 17

            self.tk_table["show"] = "headings"

            # add each colum in columns
            columns = []
            for col in search.result.columns:
                columns.append(col)

            ## display columns
            self.tk_table["columns"] = columns

            indexx = 1  # niet 0 omdat je de eerte kolom niet kunt gebruiken
            for col in search.result.columns.values:
                self.tk_table.heading(f"#{indexx}", text=col)
                indexx += 1

            # Display rows
            for each_rec in range(len(search.result.values)):
                self.tk_table.insert(
                    "", tk.END, values=list(search.result.values[each_rec])
                )

            # Change width and high off window
            app.geometry("700x600")

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("byGenre", "Something has gone wrong...")


class pageByCompany(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Title = tk.Label(self, text="Search By Company", font=LARGE_FONT)
        Title.pack()

        label = tk.Label(self, text="Company:")
        label.pack()

        # get companies and create combobox
        self.getCompanies()

        btnSearch = tk.Button(self, text="Search", command=self.controleValues)
        btnSearch.pack(pady=5, ipadx=30, ipady=5)

        btnClear = tk.Button(self, text="Clear", command=self.clearTreeview)
        btnClear.pack(pady=5, ipadx=30, ipady=5)

        btnHome = tk.Button(
            self, text="Back to Home", command=lambda: controller.show_frame(HomePage)
        )
        btnHome.pack(pady=5, ipadx=30, ipady=5)

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

        self.tk_table.pack()

    def __del__(self):
        closeConnection()

    def clearTreeview(self):
        try:
            for i in self.tk_table.get_children():
                self.tk_table.delete(i)

            self.cbo_companie.set("")
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo(
                "byCompany - foutmelding", "Something has gone wrong..."
            )

    def getCompanies(self):
        try:
            # get values for combobox
            pickle.dump("GET_COMPANIES", my_writer_obj)
            my_writer_obj.flush()

            # waiting for answer
            self.companies = pickle.load(my_writer_obj)

            # Each companie go in list choices
            choices = []
            for each_companie in self.companies:
                choices.append(each_companie)

            # Create combobox
            self.cbo_companie = ttk.Combobox(self, state="readonly", width=40)
            self.cbo_companie["values"] = choices
            self.cbo_companie.pack()

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo(
                "getCompanies - foutmelding", "Something has gone wrong..."
            )

    def controleValues(self):
        try:
            # get values from cbo
            companie = str(self.cbo_companie.get())

            # When it's empty give warning
            if companie == "":
                tk.messagebox.showwarning(
                    title="Warning", message="Companie is empty !"
                )
                self.cbo_companie.focus()
            else:
                # go to function
                self.searchByCompany()

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo(
                "controleCompany - foutmelding", "Something has gone wrong..."
            )

    def searchByCompany(self):
        try:
            # send BYCOMPANY to clienthandler
            pickle.dump("BY_COMPANY", my_writer_obj)

            # Get selected value off combobox
            company = str(self.cbo_companie.get())

            # add to  klasse
            search = ByCompany(company)
            pickle.dump(search, my_writer_obj)
            my_writer_obj.flush()

            # waiting for answer
            search = pickle.load(my_writer_obj)
            print(search)
            print(search.result.values)

            self.tk_table["height"] = 17

            self.tk_table["show"] = "headings"

            # add each colum in columns
            columns = []
            for col in search.result.columns:
                columns.append(col)

            ## display columns
            self.tk_table["columns"] = columns

            indexx = 1  # niet 0 omdat je de eerte kolom niet kunt gebruiken
            for col in search.result.columns:
                self.tk_table.heading(f"#{indexx}", text=col)
                indexx += 1

            # Display rows
            for each_rec in range(len(search.result.values)):
                self.tk_table.insert(
                    "", tk.END, values=list(search.result.values[each_rec])
                )

            # Change width and high off window
            app.geometry("700x600")

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("byCompany", "Something has gone wrong...")


class pageByName(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Title = tk.Label(self, text="Search By Name", font=LARGE_FONT)
        Title.pack()

        label = tk.Label(self, text="Name:")
        label.pack()

        # Get values to search and create combobox
        self.getNames()

        btnSearch = tk.Button(self, text="Search", command=self.controleValues)
        btnSearch.pack(pady=5, ipadx=30, ipady=5)

        btnClear = tk.Button(self, text="Clear", command=self.clearTreeview)
        btnClear.pack(pady=5, ipadx=30, ipady=5)

        btnHome = tk.Button(
            self, text="Back to Home", command=lambda: controller.show_frame(HomePage)
        )
        btnHome.pack(pady=5, ipadx=30, ipady=5)

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

        self.tk_table.pack()

    def __del__(self):
        closeConnection()

    def clearTreeview(self):
        try:
            for i in self.tk_table.get_children():
                self.tk_table.delete(i)
            self.cbo_name.set("")

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("byName - foutmelding", "Something has gone wrong...")

    def getNames(self):
        try:
            # get values for combobox
            pickle.dump("GET_NAMES", my_writer_obj)
            my_writer_obj.flush()

            # waiting for answer
            self.names = pickle.load(my_writer_obj)

            # Each name go in list choices
            choices = []
            for each_name in self.names:
                choices.append(each_name)

            # Create combobox
            self.cbo_name = ttk.Combobox(self, state="readonly", width=40)
            self.cbo_name["values"] = choices
            self.cbo_name.pack()

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("getNames - foutmelding", "Something has gone wrong...")

    def controleValues(self):
        try:
            # get values from cbo
            name = str(self.cbo_name.get())

            # When is empty give warning
            if name == "":
                tk.messagebox.showwarning(title="Warning", message="Name is empty !")
                self.cbo_name.focus()
            else:
                # go to function
                self.searchByName()

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo(
                "controleName - foutmelding", "Something has gone wrong..."
            )

    def searchByName(self):
        try:
            # send BYNAME to clienthandler
            pickle.dump("BY_NAME", my_writer_obj)

            # get selectec value off combobox
            name = str(self.cbo_name.get())

            # Voeg name toe aan klasse
            search = ByName(name)
            pickle.dump(search, my_writer_obj)
            my_writer_obj.flush()

            # waiting for answer
            search = pickle.load(my_writer_obj)
            print(search.result.columns)

            self.tk_table["height"] = 5

            self.tk_table["show"] = "headings"

            # add each colum in columns
            columns = []
            for col in search.result.columns:
                columns.append(col)

            ## display columns
            self.tk_table["columns"] = columns

            indexx = 1  # niet 0 omdat je de eerte kolom niet kunt gebruiken
            for col in search.result.columns:
                self.tk_table.heading(f"#{indexx}", text=col)
                indexx += 1

            # Display rows
            for each_rec in range(len(search.result.values)):
                self.tk_table.insert(
                    "", tk.END, values=list(search.result.values[each_rec])
                )

            # Change width and high off window
            app.geometry("700x450")

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("byName", "Something has gone wrong...")


class pageBetweenYears(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Title = tk.Label(self, text="Search Between Years", font=LARGE_FONT)
        Title.pack()

        # get years and create combobox (year1 & year2)
        self.getYears()

        btnSearch = tk.Button(self, text="Search", command=self.controleValues)
        btnSearch.pack(pady=5, ipadx=30, ipady=5)

        btnClear = tk.Button(self, text="Clear", command=self.clearTreeview)
        btnClear.pack(pady=5, ipadx=30, ipady=5)

        btnHome = tk.Button(
            self, text="Back to Home", command=lambda: controller.show_frame(HomePage)
        )
        btnHome.pack(pady=5, ipadx=30, ipady=5)

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

        self.tk_table.pack()

    def __del__(self):
        closeConnection()

    def clearTreeview(self):
        try:
            for i in self.tk_table.get_children():
                self.tk_table.delete(i)
            self.cbo_year1.set("")
            self.cbo_year2.set("")
        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo(
                "betweenYears - foutmelding", "Something has gone wrong..."
            )

    def getYears(self):
        try:
            # get values for combobox
            pickle.dump("GET_YEARS", my_writer_obj)
            my_writer_obj.flush()

            # waiting for answer
            self.years = pickle.load(my_writer_obj)

            # Each year go in list choices
            choices = []
            for each_year in self.years:
                choices.append(each_year)

            # Create label for year1
            label = tk.Label(self, text="From year:")
            label.pack()

            # Create combobox year1
            self.cbo_year1 = ttk.Combobox(self, state="readonly", width=40)
            self.cbo_year1["values"] = choices
            self.cbo_year1.pack()

            # Create label for year1
            label2 = tk.Label(self, text="To year:")
            label2.pack()

            # Create combobox year2
            self.cbo_year2 = ttk.Combobox(self, state="readonly", width=40)
            self.cbo_year2["values"] = choices
            self.cbo_year2.pack()

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("getYears - foutmelding", "Something has gone wrong...")

    def controleValues(self):

        try:
            # get values from cbo
            year1 = self.cbo_year1.get()
            year2 = self.cbo_year2.get()

            # When year1 or year2 is empty
            if year1 == "" or year2 == "":
                tk.messagebox.showwarning(
                    title="Warning", message="FROM YEAR or TO YEAR is empty !!"
                )
            else:
                # to int
                year1 = int(self.cbo_year1.get())
                year2 = int(self.cbo_year2.get())

                # show warning when year2 > year1
                if year1 < year2:
                    self.searchBetweenYears()
                else:
                    tk.messagebox.showwarning(
                        title="Warning",
                        message="TO YEAR need to be greather than FROM YEAR !!",
                    )
                    self.cbo_year2.focus()

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo(
                "controleBetweenYears - foutmelding", "Something has gone wrong..."
            )

    def searchBetweenYears(self):
        try:
            # send BYNAME to clienthandler
            pickle.dump("BY_BETWEEN_YEARS", my_writer_obj)

            # get values from cbo
            year1 = int(self.cbo_year1.get())
            year2 = int(self.cbo_year2.get())

            # Voeg name toe aan klasse
            search = BetweenYears(year1, year2)
            pickle.dump(search, my_writer_obj)
            my_writer_obj.flush()

            # waiting for answer
            search = pickle.load(my_writer_obj)

            self.tk_table["height"] = 17

            self.tk_table["show"] = "headings"

            # add each colum in columns
            columns = []
            for col in search.result.columns:
                columns.append(col)

            ## display columns
            self.tk_table["columns"] = columns

            # For each col make colum
            indexx = 1  # niet 0 omdat je de eerte kolom niet kunt gebruiken
            for col in search.result.columns:
                self.tk_table.heading(f"#{indexx}", text=col)
                indexx += 1

            # Display rows
            for each_rec in range(len(search.result.values)):
                self.tk_table.insert(
                    "", tk.END, values=list(search.result.values[each_rec])
                )

            # Change width and high off window
            app.geometry("700x600")

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("betweenYears", "Something has gone wrong...")


class pageGraphScore(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Title = tk.Label(self, text="Show Graph Off Score ", font=LARGE_FONT)
        Title.pack()
        btnShowGraph = tk.Button(self, text="Show Graph", command=self.showGraph)
        btnShowGraph.pack(pady=8, ipadx=30, ipady=5)

        btnHome = tk.Button(
            self, text="Back to Home", command=lambda: controller.show_frame(HomePage)
        )
        btnHome.pack(pady=8, ipadx=30, ipady=5)

        # bind with return key
        btnShowGraph.bind("<Return>", (lambda event: self.showGraph()))

        self.image = tk.Label(self)
        self.image.pack(pady=(5, 5), padx=(5, 5))

    def __del__(self):
        closeConnection()

    def showGraph(self):
        try:
            # get values for combobox
            pickle.dump("GRAPH_SCORE", my_writer_obj)
            my_writer_obj.flush()

            # get image
            answer = pickle.load(my_writer_obj)
            number_of_sends = int(answer)

            with open("received_file", "wb+") as f:
                for i in range(0, number_of_sends):
                    data = pickle.load(my_writer_obj)
                    f.write(data)

            logging.info("Successfully get the image")

            # showing image
            im = Image.open("received_file")
            self.img = ImageTk.PhotoImage(Image.open("received_file"))
            self.image["image"] = self.img

            app.geometry("600x700")

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo(
                "graphScore - foutmelding", "Something has gone wrong..."
            )


app = Movies()


def Stop():
    logging.info("Deleting window")
    try:
        app.destroy()
        logging.info("root destroyed but program still running, have to close threads")
        sys.exit()
        logging.info("closed threads and stopped program, this should not show up")
    except Exception as ex:
        logging.error("Start.py :> Exception during stop " + str(ex))

try:

    logging.basicConfig(level=logging.INFO)

    app.geometry()
    app.mainloop()

except KeyboardInterrupt:
    print("Interrupted, calling Stop().")
    Stop()

except Exception as e:
    print(f"ran into exception: {e}")
    Stop()
