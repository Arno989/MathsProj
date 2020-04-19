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
import sys


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
sys.path.insert(0, BASE_DIR)
dataset = pd.read_csv(f"{PROJECT_ROOT}\\data\\movies.csv", encoding="ISO-8859-1")

from server.multithreader import Online_users
from server.login import auth_user, add_user
from data.movie import BetweenYears, ByCompany, ByGenre, ByName, User

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", 15)
pd.set_option("display.width", None)
plt.rcParams.update(
    {"figure.max_open_warning": 0}
)  # Max open -> important to avoid a crash


class ClientHandler(threading.Thread):
    def __init__(self, socket, message_queue, id):
        threading.Thread.__init__(self)
        self.socket_to_client = socket
        self.message_queue = message_queue
        self.id = id
        logging.info(f"CLH> thread {self.id} added on socket {socket}")

    def run(self):
        writer_obj = self.socket_to_client.makefile(mode="rwb")

        self.printGui(f"Waiting for first query...")
        query = pickle.load(writer_obj)

        user = User()
        user.authenticated = True

        while query != "C":
            while query == "SIGNIN":
                try:
                    user = pickle.load(writer_obj)
                    if auth_user(user.username, user.password):
                        user.authenticated = True
                        pickle.dump(user, writer_obj)
                        writer_obj.flush()
                        Online_users.loginUser(user.username)
                        self.printGui(f"User {user.username} signed in")
                    else:
                        user.authenticated = False
                        pickle.dump(user, writer_obj)
                        writer_obj.flush()
                        self.printGui(f"Login refused")

                except Exception as e:
                    self.printGui(f"Error during login: {e}")

                query = pickle.load(writer_obj)

            while query == "SIGNUP":
                try:
                    user = pickle.load(writer_obj)
                    print(user)
                    try:
                        add_user(user.username, user.password, user.email, user.name)
                        self.printGui(f"Added user {user.username}")
                        user.authenticated = True
                        pickle.dump(user, writer_obj)
                        writer_obj.flush()
                        Online_users.loginUser(user.username)
                        self.printGui(f"User {user.username} Signed in")

                    except ValueError:
                        user.authenticated = True
                        pickle.dump(False, writer_obj)
                        writer_obj.flush()
                        self.printGui(f"Username already exists")

                except Exception as e:
                    self.printGui(f"Error during signup: {e}")

                query = pickle.load(writer_obj)

            while user.authenticated:
                while query == "BY_GENRE":  # Search by genre
                    q_Genre = pickle.load(writer_obj)
                    search = str(q_Genre.genre).capitalize()

                    # Execute query
                    try:
                        q_Genre.result = dataset.loc[dataset["genre"] == search]
                    except Exception as e:
                        self.printGui(f"Error from query: {e}")
                    self.printGui(f"Result from query: {q_Genre.result}")

                    # Reply with results
                    pickle.dump(q_Genre, writer_obj)
                    writer_obj.flush()
                    self.printGui(f"Sent query results")

                    query = pickle.load(writer_obj)

                while query == "BY_COMPANY":  # Search by company name
                    q_Company = pickle.load(writer_obj)
                    search = str(q_Company.company)

                    # Execute query
                    try:
                        q_Company.result = dataset.loc[dataset["company"] == search]
                    except Exception as e:
                        self.printGui(f"Error from query: {e}")
                    self.printGui(f"Result from query: {q_Company.result}")

                    # Reply with results
                    pickle.dump(q_Company, writer_obj)
                    writer_obj.flush()
                    self.printGui(f"Sent query results")

                    query = pickle.load(writer_obj)

                while query == "BY_NAME":  # Search by main star name
                    q_Name = pickle.load(writer_obj)
                    search = str(q_Name.name)

                    # Execute query
                    try:
                        q_Name.result = dataset.loc[dataset["name"] == search]
                    except Exception as e:
                        self.printGui(f"Error from query: {e}")
                    self.printGui(f"Result from query: {q_Name.result}")

                    # Reply with results
                    pickle.dump(q_Name, writer_obj)
                    writer_obj.flush()
                    self.printGui(f"Sent query results")

                    query = pickle.load(writer_obj)

                while query == "BY_BETWEEN_YEARS":  # Search between 2 years
                    q_BetweenYears = pickle.load(writer_obj)

                    # Execute query
                    try:
                        q_BetweenYears.result = dataset.loc[
                            (dataset["year"] >= int(q_BetweenYears.year2))
                            & (dataset["year"] <= int(q_BetweenYears.year2))
                        ]
                    except Exception as e:
                        self.printGui(f"Error from query: {e}")
                    self.printGui(f"Result from query: {q_BetweenYears.result}")

                    # Reply with results
                    pickle.dump(q_BetweenYears, writer_obj)
                    writer_obj.flush()
                    self.printGui(f"Sent query results")

                    query = pickle.load(writer_obj)

                while query == "GRAPH_SCORE":
                    # Generate graph with dank colors  -->  https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
                    plt.figure(figsize=(8, 8))
                    colors = plt.get_cmap("ocean")(np.linspace(0, 1, 100))
                    n, bins, patches = plt.hist(dataset.score, bins=100)
                    for patch, color in zip(patches, colors):
                        patch.set_facecolor(color)

                    # Save image to send
                    filename = "graph.jpg"
                    plt.savefig(filename)

                    # Scale size of image
                    basewidth = 600
                    img = Image.open(filename)
                    wpercent = basewidth / float(img.size[0])
                    hsize = int((float(img.size[1]) * float(wpercent)))
                    img = img.resize((basewidth, hsize), Image.ANTIALIAS)

                    # Save and open file
                    img.save(filename)
                    f = open(filename, "rb")

                    # Get filezise
                    size_in_bytes = os.path.getsize(filename)
                    number = math.ceil(size_in_bytes / 1024)

                    # Notify client of incomming package and it's size
                    pickle.dump("%d" % number, writer_obj)
                    writer_obj.flush()

                    # Send graph
                    l = f.read(1024)
                    while l:
                        pickle.dump(l, writer_obj)
                        writer_obj.flush()
                        l = f.read(1024)

                # Get unique values to create dropdown
                while query == "GET_GENRES":
                    genres = dataset.genre.unique()
                    pickle.dump(genres, writer_obj)
                    writer_obj.flush()
                    query = pickle.load(writer_obj)

                while query == "GET_COMPANIES":
                    companies = dataset.company.unique()
                    pickle.dump(companies, writer_obj)
                    writer_obj.flush()
                    query = pickle.load(writer_obj)

                while query == "GET_NAMES":
                    names = dataset.name.unique()
                    pickle.dump(names, writer_obj)
                    writer_obj.flush()
                    query = pickle.load(writer_obj)

                while query == "GET_YEARS":
                    years = dataset.year.unique()
                    pickle.dump(years, writer_obj)
                    writer_obj.flush()
                    query = pickle.load(writer_obj)

                while query == "SIGNOFF":
                    try:
                        user = pickle.load(writer_obj)
                        user.authenticated = False
                        pickle.dump(user, writer_obj)
                        writer_obj.flush()
                        Online_users.logoutUser(user.username)
                        self.printGui(f"User {user.username} signed off")

                    except Exception as e:
                        self.printGui(f"Error during logout: {e}")


            self.printGui(f"Connection closing")
            self.socket_to_client.close()

    def printGui(self, message):
        self.message_queue.put(f"CLH {self.id}> {message}")
        logging.info(f"CLH {self.id}> {message}")
