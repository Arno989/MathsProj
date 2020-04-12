class Stopafstand:
    def __init__(self, snelheid, reactietijd, wegdek):
        self.snelheid = snelheid
        self.reactietijd = reactietijd
        self.wegdek = wegdek
        self.stopafstand = None

    def __str__(self):
        return "Stopafstand berekenen snelheid: %d en reactietijd: %d en wegdek: %s" % (self.snelheid, self.reactietijd, self.wegdek)

    def __eq__(self, other):
        return (self.snelheid == other.snelheid) and (self.reactietijd == other.reactietijd) and (self.wegdek == other.wegdek)

class ByGenre:
    def __init__(self, genre):
        self.genre = genre
        self.resultaat = None

    def __str__(self):
        return f"Genre: {self.genre}"

    #def __eq__(self, other):
    #    return (self.genre == other.genre) 


class Movie:
    def __init__(
        self,
        budget,
        company,
        country,
        director,
        genre,
        gross,
        name,
        rating,
        released,
        runtime,
        score,
        star,
        votes,
        writer,
        year,
    ):

        self.budget = budget
        self.company = company
        self.country = country
        self.director = director
        self.genre = genre
        self.gross = gross
        self.name = name
        self.rating = rating
        self.released = released
        self.runtime = runtime
        self.score = score
        self.star = star
        self.votes = votes
        self.writer = writer
        self.year = year
