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

    def getSearches(self, user="*"):  # bruh idk anymore, shit's confusing and took me 2 hours
        with open(searchlog) as f:
            print("got in the moderator")
            data = json.load(f)
            searches = []
            try:
                if user == "*":
                    for record in data:
                        if not any(record['query'] in d for d in searches):
                            searches.append({record["query"]: 1})
                        else:
                            for r in searches:
                                for k in r:
                                    if k == record["query"]:
                                        r[k] += 1
                else:
                    for record in data:
                        if record["user"] == user:
                            if record["query"] in searches:
                                searches.query.append({record["query"]: 1})
                            else:
                                searches.query[record["query"]] += 1
                                print(f"returning: {searches}")
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

fout bij laden van image... 'str' object has no attribute 'read'

show messages clienthandler fout van opvangen van message


# Bovenstaande items inserten in elk treeview ! <---------- ???


Done:

adjusted search by name for free strings

search history zorg erook voor dat je de parameter kunt terug krijgen 

fixed re-login crash

auto clear bij verandering zoekopdracht <- client side

layout van server side for get online users fix

terug naar login na logout

Fix Login

List off all searches & paramater & user

"""
