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

class BetweenYears:
    def __init__(self, year1,year2):
        self.year1 = year1
        self.year2 = year2
        self.result = None

    def __str__(self):
        return f"between: {self.year1} and {self.year2}"