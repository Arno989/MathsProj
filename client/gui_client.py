# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import logging
import socket
import pickle


from tkinter import *


from tkinter import messagebox
from tkinter.ttk import Combobox

from data.stopafstand import Stopafstand



class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.makeConnnectionWithServer()

    # Creation of init_window
    def init_window(self):
        self.master.title("Stopafstand")
        self.pack(fill=BOTH, expand=1)

        Label(self, text="Snelheid (km/u):").grid(row=0)
        Label(self, text="Reactietijd (sec):", pady=10).grid(row=1)
        Label(self, text="Type wegdek:", pady=10).grid(row=2)
        Label(self, text="Stopafstand:", pady=10).grid(row=4)


        self.entry_snelheid = Entry(self, width=40)
        self.entry_reactietijd = Entry(self, width=40)
        self.entry_wegdek = Entry(self, width=40)
        self.label_resultaat = Label(self, width=40, anchor='w')

        self.entry_snelheid.grid(row=0, column=1, sticky=E + W, pady=(5, 5))
        self.entry_reactietijd.grid(row=1, column=1, sticky=E + W)
        self.label_resultaat.grid(row=4, column=1, sticky=E + W)

        choices = ('Droog wegdek', 'Nat wegdek')
        # self.entry_wegdek.grid(row=2, column=1, sticky=E + W)
        self.cbo_wegdek = Combobox(self, state="readonly", width=40)
        self.cbo_wegdek['values'] = choices
        self.cbo_wegdek.grid(row=2, column=1, sticky=E + W)

        Label(self, text="km/u").grid(row=0, column=2)
        Label(self, text="sec", pady=10).grid(row=1, column=2)

        self.buttonCalculate = Button(self, text="Bereken stopafstand", command=self.calculateStopafstand)
        self.buttonCalculate.grid(row=3, column=0, columnspan=3, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

        Grid.rowconfigure(self, 2, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

        # root.protocol("WM_DELETE_WINDOW", _delete_window)

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
            wegdek = (self.cbo_wegdek.get())
            
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

root = Tk()
# root.geometry("400x300")
app = Window(root)
root.mainloop()
