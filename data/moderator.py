#list off online users
onlineUsers = ['arno']

class Online_users():    
    def loginUser(self, username):
        onlineUsers.append(username)
        
    def logoutUser(self, username):
        onlineUsers.remove(username)
    
    def users_online():
        return onlineUsers
