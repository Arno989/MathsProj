import sys
import os
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
sys.path.insert(0, BASE_DIR)
searchlog = f"{PROJECT_ROOT}\\data\\searchlog.json"

onlineUsers = []

class users_online():    
    def loginUser(self, username):
        print(f'adding {username} to online list')
        onlineUsers.append(username)
        print(f'online users: {onlineUsers}')
        
    def logoutUser(self, username):
        print(f'removing {username} from online list')
        onlineUsers.pop(onlineUsers.index(username))
        print(f'online users: {onlineUsers}')
    
    def getUsers(self):
        return onlineUsers
    
    
class search_popularity():
    def logSearch(self, user, query, params = []):
        try:
            data = json.load(searchlog)
            temp = data['searches'] 
            print(f'logging query {query} for user {user}')
            temp.append({'user' : user, 'query': query, 'parameters': list(params)}) 
            with open(searchlog,'w') as f: 
                json.dump(data, f, indent=4)
        except Exception as e:
            print(e)
    
    def getSearches(self, user='*'):
        data = json.load(searchlog)
        temp = data['searches']
        searches = {}
        try:
            if user == '*':
                for search in data['searches']:
                    if search.query in searches:
                        searches.query.append({search.query : '1'})
                    else:
                        searches.query[search.query] += 1
            else:
                for search in data['searches']:
                    if search.user == user:
                        if search.query in searches:
                            searches.query.append({search.query : '1'})
                        else:
                            searches.query[search.query] += 1
        except Exception as e:
            print(e)
    

class user_message():
    sentmessages = []
    
    def sendmessage(self, message, user='*'):
        try:
            if user == '*':
                pass
            else:
                pass
        except Exception as e:
            print(e)
            
    def getmessages(self, user='*'):
        try:
            if user == '*':
                pass
            else:
                pass
        except Exception as e:
            print(e)


'''
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

search history zorg erook voor dat je de parameter kunt terug krijgen 

fixed re-login crash

auto clear bij verandering zoekopdracht <- client side

layout van server side for get online users fix

terug naar login na logout

Fix Login

List off all searches & paramater & user

'''