from tkinter import *
from classes import *
from resources import *
from reading_parsing import *

class Aplikacija():
    def preveri(self, gumb=None, *args):
        self.gumbi[gumb].grid_remove()
        guess = self.abeceda[gumb]
        self.posodobi(self.beseda.ugibaj(guess))

    def posodobi(self, r=None):
        if r:
            self.odkrito.set(self.beseda.za_gui())
        else:
            self.napacno.set(self.beseda.napacni_poskusi)
        if self.beseda.reseno() or self.beseda.napacni_poskusi == 11:
            self.nova_igra()

    def nova_igra(self):
        for b in self.gumbi:
            b.grid()
        self.beseda = reading_parsing.random_beseda()
        self.platno.delete(ALL)
        self.odkrito.set(self.beseda.za_gui())
        self.napacno.set(self.beseda.napacni_poskusi)

    def __init__(self, master, beseda, abc):
        self.beseda = beseda
        self.abeceda = abc
        self.spaces = 2

        master.title('Vislice')

        # meni
        self.meni = Menu(master)
        master.config(menu=self.meni)
        self.meni.add_command(label="Nova igra", command=self.nova_igra)
        self.meni.add_command(label="Zapri", command=quit)

        okvir = Frame(master, width=600, height=600)
        okvir.grid()

        self.odkrito = StringVar()  # koliko besede je do zdaj odkrito
        self.odkrito.set(self.beseda.za_gui())
        Label(okvir, textvariable=self.odkrito).grid(row=1, column=1, columnspan=2)

        self.gumbi = []
        for i, l in enumerate(self.abeceda):
            b = Button(okvir, text=l, command=lambda x=i: self.preveri(x))
            self.gumbi.append(b)
            b.grid(row=i // 9 + 1, column=i % 9 + 3)

        self.platno = Canvas(okvir, width=200, height=200)
        self.platno.grid(row=2, column=1, rowspan=3, columnspan=2)

        self.napacno = StringVar()
        self.napacno.set(self.beseda.napacni_poskusi)
        Label(okvir, text="Napačni poskusi: ").grid(row=5, column=1)
        Label(okvir, textvariable=self.napacno).grid(row=5, column=2)

root = Tk()
App = Aplikacija(root, reading_parsing.random_beseda(), abeceda())
root.mainloop()
