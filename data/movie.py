class Stopafstand:
    def __init__(self, snelheid, reactietijd, wegdek):
        self.snelheid = snelheid
        self.reactietijd = reactietijd
        self.wegdek = wegdek
        self.stopafstand = None

    def __str__(self):
        return "Stopafstand berekenen snelheid: %d en reactietijd: %d en wegdek: %d" % (self.snelheid, self.reactietijd, self.wegdek)

    def __eq__(self, other):
        return (self.snelheid == other.snelheid) and (self.reactietijd == other.reactietijd) and (self.wegdek == other.wegdek)
