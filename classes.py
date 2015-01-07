import reading_parsing
import resources


class Beseda:
    def __init__(self, niz, defin=None):
        self.beseda = niz
        self.definicija = defin
        self.neznano = niz
        self.znano = "_" * len(niz)
        self.napacni_poskusi = 0  # koliko crk je bilo napacnih
        self.ugibano = ""  # vse do zdaj ugibane crke

    def __str__(self):
        return self.beseda

    def __repr__(self):
        napis = self.beseda
        return napis

    def __len__(self):
        return len(self.beseda)

    def __iter__(self):
        for x in self.beseda:
            yield x

    def velike(self):
        return self.beseda.upper()

    def definiraj(self):
        if self.definicija:
            return self.definicija
        else:
            self.definicija = reading_parsing.definicija(self.beseda)
            return self.definicija

    def ugibaj(self, niz, abc=resources.abeceda()):
        znano_zdaj = self.znano
        for x in niz:
            if x not in abc:
                raise Exception("Napačen vnos!")
            elif x in self.ugibano:
                pass
            elif x in self.beseda:
                i = 0
                while i < len(self.beseda):
                    if x == self.beseda[i]:
                        self.znano = self.znano[:i] + x + self.znano[i+1:]
                    i += 1
                self.neznano = self.neznano.replace(x, "")
                self.ugibano += x
            elif x not in self.beseda:
                self.ugibano += x
                self.napacni_poskusi += 1
        if self.znano == znano_zdaj:
            return None
        return self.znano

    def reseno(self):
        return len(self.neznano) == 0
