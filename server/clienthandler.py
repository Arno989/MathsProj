import threading
import logging
import pickle
import pandas as pd
import numpy as np
import os
import math
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image


pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", 15)
pd.set_option("display.width", None)

dataset = pd.read_csv("server/movies.csv", encoding="ISO-8859-1")

dataset.score = dataset.score.astype(float)


class ClientHandler(threading.Thread):
    numbers_clienthandlers = 0

    def __init__(self, socketclient, messages_queue):
        threading.Thread.__init__(self)
        self.socket_to_client = socketclient
        self.messages_queue = messages_queue
        self.id = ClientHandler.numbers_clienthandlers
        ClientHandler.numbers_clienthandlers += 1

    def run(self):
        writer_obj = self.socket_to_client.makefile(mode="rwb")

        self.print_gui_message("Waiting for inputs...")
        operation = pickle.load(writer_obj)
        print(operation)
        
        authenticated = True
        

        # Search by genre
        if authenticated:
            while operation != "C":
                while operation == "BYGENRE":
                    byGenre = pickle.load(writer_obj)
                    search = str(byGenre.genre).capitalize()
                    try:
                        byGenre.result = dataset.loc[
                            dataset["genre"] == search
                        ]  # dataset[dataset.genre == search]
                    except Exception as e:
                        self.print_gui_message(f"Error from query: {e}")
                    self.print_gui_message(byGenre.result)

                    # stuur genre door
                    pickle.dump(byGenre, writer_obj)
                    writer_obj.flush()
                    self.print_gui_message(f"Sending operation results")

                    operation = pickle.load(writer_obj)

                while operation == "BYCOMPANY":
                    byCompany = pickle.load(writer_obj)
                    search = str(byCompany.company)
                    try:
                        byCompany.result = dataset.loc[
                            dataset["company"] == search
                        ]  # dataset[dataset.genre == search]    .lower()*2
                    except Exception as e:
                        self.print_gui_message(f"Error from query: {e}")
                    self.print_gui_message(f"{byCompany.result}")

                    # stuur resultaat door
                    pickle.dump(byCompany, writer_obj)
                    writer_obj.flush()
                    self.print_gui_message(f"Sending operation results")

                    operation = pickle.load(writer_obj)

                while operation == "BYNAME":
                    byName = pickle.load(writer_obj)
                    search = str(byName.name)
                    try:
                        byName.result = dataset.loc[dataset["name"] == search]
                    except Exception as e:
                        self.print_gui_message(f"Error from query: {e}")
                    self.print_gui_message(f"{byName.result}")

                    # stuur resultaat door
                    pickle.dump(byName, writer_obj)
                    writer_obj.flush()
                    self.print_gui_message(f"Sending operation results")

                    operation = pickle.load(writer_obj)

                while operation == "BETWEENYEARS":
                    betweenYears = pickle.load(writer_obj)
                    year1 = int(betweenYears.year1)
                    year2 = int(betweenYears.year2)
                    try:

                        betweenYears.result = dataset.loc[
                            (dataset["year"] >= year1) & (dataset["year"] <= year2)
                        ]
                    except Exception as e:
                        self.print_gui_message(f"Error from query: {e}")
                    self.print_gui_message(f"{betweenYears.result}")

                    # stuur resultaat door
                    pickle.dump(betweenYears, writer_obj)
                    writer_obj.flush()
                    self.print_gui_message(f"Sending operation results")

                    operation = pickle.load(writer_obj)

                while operation == "GRAPH-SCORE":

                    # pandas en patplotlib shit
                    plt.rcParams.update(
                        {"figure.max_open_warning": 0}
                    )  # Max open -> important to avoid a crash

                    # generate graph
                    plt.figure(figsize=(8, 8))
                    colors = plt.get_cmap("ocean")(
                        np.linspace(0, 1, 100)
                    )  # https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
                    n, bins, patches = plt.hist(dataset.score, bins=100)
                    for patch, color in zip(patches, colors):
                        patch.set_facecolor(color)

                    # save
                    filename = "graph.jpg"
                    plt.savefig(filename)

                    # Scale size off image
                    basewidth = 600
                    img = Image.open(filename)
                    wpercent = basewidth / float(img.size[0])
                    hsize = int((float(img.size[1]) * float(wpercent)))
                    img = img.resize((basewidth, hsize), Image.ANTIALIAS)

                    # Save and open file
                    img.save(filename)
                    f = open(filename, "rb")

                    # filezise
                    size_in_bytes = os.path.getsize(filename)
                    number = math.ceil(size_in_bytes / 1024)

                    # notify client
                    pickle.dump("%d" % number, writer_obj)
                    writer_obj.flush()

                    # send graph
                    l = f.read(1024)
                    while l:
                        pickle.dump(l, writer_obj)
                        writer_obj.flush()
                        # self.socketclient.send(l)
                        l = f.read(1024)

                ######### Get unique values to create dropdowns #########
                while operation == "GET-GENRES":
                    try:
                        # Unique genres
                        genres = dataset.genre.unique()

                    except Exception as e:
                        self.print_gui_message(f"Error from query: {e}")
                    self.print_gui_message(f"{genres}")

                    # stuur resultaat door
                    pickle.dump(genres, writer_obj)
                    writer_obj.flush()
                    self.print_gui_message(f"Sending operation results")

                    operation = pickle.load(writer_obj)

                while operation == "GET-COMPANIES":
                    try:
                        # Unique companies
                        companies = dataset.company.unique()

                    except Exception as e:
                        self.print_gui_message(f"Error from query: {e}")
                    self.print_gui_message(f"{companies}")

                    # stuur resultaat door
                    pickle.dump(companies, writer_obj)
                    writer_obj.flush()
                    self.print_gui_message(f"Sending operation results")

                    operation = pickle.load(writer_obj)

                while operation == "GET-NAMES":
                    try:
                        # Unique names
                        names = dataset.name.unique()

                    except Exception as e:
                        self.print_gui_message(f"Error from query: {e}")
                    self.print_gui_message(f"{names}")

                    # stuur resultaat door
                    pickle.dump(names, writer_obj)
                    writer_obj.flush()
                    self.print_gui_message(f"Sending operation results")

                    operation = pickle.load(writer_obj)

                while operation == "GET-YEARS":
                    try:
                        # Unique years
                        years = dataset.year.unique()

                    except Exception as e:
                        self.print_gui_message(f"Error from query: {e}")
                    self.print_gui_message(f"{years}")

                    # stuur resultaat door
                    pickle.dump(years, writer_obj)
                    writer_obj.flush()
                    self.print_gui_message(f"Sending operation results")

                    operation = pickle.load(writer_obj)

            self.print_gui_message(f"Connection closed")
            self.socket_to_client.close()

    def print_gui_message(self, message):
        self.messages_queue.put(f"CLH {self.id}:> {message}")
