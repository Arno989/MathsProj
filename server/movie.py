class ByGenre:
    def __init__(self, genre):
        self.genre = genre
        self.result = None

    def __str__(self):
        return f"Genre: {self.genre}"

    # def __eq__(self, other):
    #    return (self.genre == other.genre)

class ByCompany:
    def __init__(self, company):
        self.company = company
        self.result = None

    def __str__(self):
        return f"Company: {self.company}"

class ByName:
    def __init__(self, name):
        self.name = name
        self.result = None

    def __str__(self):
        return f"Name: {self.name}"


class SignIn:
    def __init__(self, nickname,password):
        self.nickname = nickname
        self.password = password
        self.authenticated = None

    def __str__(self):
        return f"Signed in: {self.nickname}"

class SignUp:
    def __init__(self, name,nickname,email,password):
        self.name = name
        self.nickname = nickname
        self.email = email
        self.password = password
        self.authenticated = None
      

    def __str__(self):
        return f"Signed up: {self.nickname}"
   

class BetweenYears:
    def __init__(self, year1,year2):
        self.year1 = year1
        self.year2 = year2
        self.result = None

    def __str__(self):
        return f"between: {self.year1} and {self.year2}"



