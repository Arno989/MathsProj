import sys
import os
import json
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
sys.path.insert(0, BASE_DIR)
searchlog = f"{PROJECT_ROOT}\\data\\searchlog.json"

onlineUsers = []

startLog = [
    {"user": "user", "query": "query", "parameters": ["list(params)", "params"]},
    {"user": "user", "query": "query", "parameters": ["list(params)", "params"]},
]


class users_online:
    def loginUser(self, username):
        print(f"adding {username} to online list")
        onlineUsers.append(username)
        print(f"online users: {onlineUsers}")

    def logoutUser(self, username):
        print(f"removing {username} from online list")
        onlineUsers.pop(onlineUsers.index(username))
        print(f"online users: {onlineUsers}")

    def getUsers(self):
        return onlineUsers


class search_popularity:
    def logSearch(self, user, query, params=None):
        try:
            data = None
            with open(searchlog) as f:
                data = json.load(f)
            with open(searchlog, "w") as f:
                data.append({"user": user, "query": query, "parameters": params})
                json.dump(data, f, indent=4)

        except Exception as e:
            print(f"exception in logging: {e}")

    def getSearches(self, user="*"):
        with open(searchlog) as f:
            print("got in the moderator")
            data = json.load(f)
            searches = []
            try:
                if user == "*":
                    for record in data:
                        if not any(e["query"] == record["query"] for e in searches):
                            searches.append({"query": record["query"], "amount": 1})
                        else:
                            for e in searches:
                                if e["query"] == record["query"]:
                                    e["amount"] += 1
                else:
                    for record in data:
                        if record["user"] == user:
                            searches.append({"query": record["query"], "parameters": record["parameters"]})
                return searches
            except Exception as e:
                print(f"exception in reading log {e}")


class user_message:
    sentmessages = []

    def sendmessage(self, message, user="*"):
        try:
            if user == "*":
                pass
            else:
                pass
        except Exception as e:
            print(e)

    def getmessages(self, user="*"):
        try:
            if user == "*":
                pass
            else:
                pass
        except Exception as e:
            print(e)


"""
To Do:

List of sent messages sorteerbaar per user (of all)
# class Message(user)
# from server to client !!

New query GET_MESSAGES zodat elke user zijn messages kan opvragen

autoscroll bij server gui



show messages clienthandler fout van opvangen van message

online users list moet gecleared worden elke keer ze worden opgevraagd ->> al gebeurd toch? 

get online users runt op het moment dat het venster opgeroepen wordt 


# Bovenstaande items inserten in elk treeview ! <---------- ???


Done:

fout bij laden van image... 'str' object has no attribute 'read' --?? niks gedaan ma tis weg

fixed search popularity count & show

fixed user search " parameters

"""
