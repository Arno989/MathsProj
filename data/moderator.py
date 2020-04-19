#list off online users
onlineUsers = ['arno']

class Online_users():    
    def loginUser(self, username):
        onlineUsers.append(username)
        
    def logoutUser(self, username):
        onlineUsers.remove(username)
    
    def users_online():
        return onlineUsers


#To Do 

#Fix Login

#List off sended message zowel (all users als unieke user)
## class Message(user)
## class Message() -> all
## from server to client !!

#n New query GET_MESSAGES -> zowel unieke messages als voor iedereen

#List off searches of each user & parameter
## class searches(user)

#List off all searches & paramater & how much searched
## class searches --> all


## Bovenstaande items inserten in elk treeview !