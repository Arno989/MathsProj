import datetime
import json
import logging
import math
import os
import pickle
import sys
import threading
from pathlib import Path

import bcrypt  # u gotta "pip install bcrypt" bro
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from PIL import Image

from data.movie import BetweenYears, ByCompany, ByGenre, ByName, User
from server.moderator import search_popularity, user_message, users_online

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(PROJECT_ROOT))
dataset = pd.read_csv(f"{PROJECT_ROOT}\\data\\movies.csv", encoding="ISO-8859-1")
jsonDb = f"{PROJECT_ROOT}\\data\\users.json"


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
        try:
            writer_obj = self.socket_to_client.makefile(mode="rwb")

            self.printGui(f"Waiting for first query...")
            query = pickle.load(writer_obj)

            user = User()
            user.authenticated = False

            while query != "C":
                while query == "SIGNIN":
                    try:
                        user = pickle.load(writer_obj)
                        if auth_user(user.username, user.password):
                            user.authenticated = True
                            pickle.dump(user, writer_obj)
                            writer_obj.flush()
                            users_online().loginUser(user.username)
                            self.printGui(f"User {user.username} signed in")
                            search_popularity().logSearch(user.username, query)
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
                        try:
                            add_user(
                                user.username, user.password, user.email, user.name
                            )
                            self.printGui(f"Added user {user.username}")
                            user.authenticated = True
                            pickle.dump(user, writer_obj)
                            writer_obj.flush()
                            users_online().loginUser(user.username)
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
                        search_popularity().logSearch(user.username, query, search)

                        # Execute query
                        try:
                            q_Genre.result = dataset.loc[dataset["genre"] == search]
                        except Exception as e:
                            self.printGui(f"Error from query: {e}")
                        self.printGui(f"Result from query")

                        # Reply with results
                        pickle.dump(q_Genre, writer_obj)
                        writer_obj.flush()
                        self.printGui(f"Sent query results")

                        query = pickle.load(writer_obj)

                    while query == "BY_COMPANY":  # Search by company name
                        q_Company = pickle.load(writer_obj)
                        search = str(q_Company.company)
                        search_popularity().logSearch(user.username, query, search)

                        # Execute query
                        try:
                            q_Company.result = dataset.loc[dataset["company"] == search]
                        except Exception as e:
                            self.printGui(f"Error from query: {e}")
                        self.printGui(f"Result from query")

                        # Reply with results
                        pickle.dump(q_Company, writer_obj)
                        writer_obj.flush()
                        self.printGui(f"Sent query results")

                        query = pickle.load(writer_obj)

                    while query == "BY_NAME":  # Search by main star name
                        q_Name = pickle.load(writer_obj)
                        search = str(q_Name.name)
                        search_popularity().logSearch(user.username, query, search)

                        # Execute query
                        try:
                            q_Name.result = dataset.loc[dataset['name'].str.contains(pat=search, case=False, regex=False)]
                        except Exception as e:
                            self.printGui(f"Error from query: {e}")
                        self.printGui(f"Result from query")

                        # Reply with results
                        pickle.dump(q_Name, writer_obj)
                        writer_obj.flush()
                        self.printGui(f"Sent query results")

                        query = pickle.load(writer_obj)

                    while query == "BY_BETWEEN_YEARS":  # Search between 2 years
                        q_BetweenYears = pickle.load(writer_obj)
                        search_popularity().logSearch(user.username, query, [q_BetweenYears.year1, q_BetweenYears.year2])

                        # Execute query
                        try:
                            q_BetweenYears.result = dataset.loc[
                                (dataset["year"] >= int(q_BetweenYears.year1))
                                & (dataset["year"] <= int(q_BetweenYears.year2))
                            ]
                        except Exception as e:
                            self.printGui(f"Error from query: {e}")
                        self.printGui(f"Result from query")

                        # Reply with results
                        pickle.dump(q_BetweenYears, writer_obj)
                        writer_obj.flush()
                        self.printGui(f"Sent query results")

                        query = pickle.load(writer_obj)

                    while query == "GRAPH_SCORE":
                        search_popularity().logSearch(user.username, query)
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

                        query = pickle.load(writer_obj)

                    while query == "GET_MESSAGES":
                        try:
                            search_popularity().logSearch(user.username, query)
                            messages = user_message().getmessages(user.username)

                            pickle.dump(messages, writer_obj)
                            writer_obj.flush()
                            print(messages)

                            self.printGui(f"Sent usermessages for {user.username}")

                            query = pickle.load(writer_obj)

                        except Exception as e:
                            self.printGui(f"Error during logout: {e}")

                    while query == "SIGNOFF":
                        try:
                            user.authenticated = False
                            pickle.dump(user, writer_obj)
                            writer_obj.flush()
                            users_online().logoutUser(user.username)
                            self.printGui(f"User {user.username} signed off")
                            print(users_online().getUsers())

                            query = ""

                        except Exception as e:
                            self.printGui(f"Error during logout: {e}")

                        query = pickle.load(writer_obj)

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

        except (EOFError, ConnectionResetError):
            self.printGui(f"Client lost connection")
            self.socket_to_client.close()
            return

    def printGui(self, message):
        self.message_queue.put(f"CLH {self.id}> {message}")
        logging.info(f"CLH {self.id}> {message}")
        print(f"CLH {self.id}> {message}")

#region Login and database
#region dbHandler
startUsers = [
    User(name="yeet", username="yeet", password="hash", email="yeet"),
    User(name="yeet2", username="yeet2", password="hash2", email="yeet2"),
]


def obj_dict(obj):
    return obj.__dict__


def create_file_if_not_exists(path: str):
    if not Path(path).is_file():
        with open(path, "w") as users_file:
            json.dump([ob.__dict__ for ob in startUsers], users_file)


def get_json_file_contents(path: str):
    with open(path) as users_file:
        return json.load(users_file)
#endregion

#region Encryption
def hash_password(password: str) -> str:
    encoded_password = password.encode("utf8")
    cost_rounds = 12  # tegen de bruteforce jwz
    random_salt = bcrypt.gensalt(cost_rounds)
    hashed_password = bcrypt.hashpw(encoded_password, random_salt).decode(
        "utf8", "strict"
    )
    return hashed_password


def check_password(password: str, password_hash: str) -> bool:
    encoded_password = password.encode("utf8")
    encoded_password_hash = password_hash.encode("utf8")
    password_matches = bcrypt.checkpw(encoded_password, encoded_password_hash)
    return password_matches
#endregion

#region login
def add_user(username: str, password: str, name: str, email: str):
    create_file_if_not_exists(jsonDb)
    is_duplicate_user = retrieve_user(username)
    if is_duplicate_user != None:
        print(f'Username "{username}" already exists.')
    new_user = User(
        username=username, password=hash_password(password), name=name, email=email
    )
    all_users = get_json_file_contents(jsonDb)
    all_users.append(new_user.__dict__)
    with open(jsonDb, "w") as users_file:
        json.dump(all_users, users_file, indent=4)


def retrieve_user(username: str):
    all_users = get_json_file_contents(jsonDb)
    if len(all_users) != 0:
        for u in all_users:
            if u['username'] == username:
                return u
        return None
    else:
        return None


def auth_user(username: str, password: str):
    user = retrieve_user(username)
    password_hash = user['password']
    if not user:
        return False
    if not check_password(password, password_hash):
        return False
    return True
#endregion
#endregion
