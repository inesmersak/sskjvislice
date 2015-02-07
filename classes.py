import resources


class Beseda:
    def __init__(self, niz, defin=None):
        self.beseda = niz
        self.definicija = defin
        self.neznano = niz
        self.znano = "_" * len(niz)
        self.preostali_poskusi = 11  # koliko poskusov je se do konca
        self.ugibano = ""  # vse do zdaj ugibane crke

    def __str__(self):
        return self.beseda

    def __repr__(self):
        return "Beseda(" + self.beseda + ")"

    def __len__(self):
        return len(self.beseda)

    def __iter__(self):
        for x in self.beseda:
            yield x

    def velike(self):
        return self.beseda.upper()

    def za_gui(self, konec=False, presledki=1):
        g = ""
        if konec:
            for x in self.beseda:
                g += x + " " * presledki
        else:
            for x in self.znano:
                g += x + " " * presledki
        return g[:len(g)-presledki]

    def ugibaj(self, niz, abc=resources.abe):
        znano_zdaj = self.znano
        for x in niz:
            if x not in abc:
                raise ValueError("Napačen vnos! Vrednost =", x)
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
                self.preostali_poskusi -= 1
        if self.znano == znano_zdaj:
            return None
        return self.znano

    def reseno(self):
        return len(self.neznano) == 0
