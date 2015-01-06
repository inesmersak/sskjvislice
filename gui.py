from tkinter import *
from classes import *
from resources import *


class Aplikacija():
    def preveri(self, gumb=None, *args):
        self.gumbi[gumb].grid_remove()
        guess = self.abeceda[gumb]
        self.posodobi(self.beseda.ugibaj(guess))

    def posodobi(self, r=None):
        if r:
            self.odkrito.set(r)

    def __init__(self, master, beseda, abc):
        self.beseda = beseda
        self.abeceda = abc
        self.spaces = 2

        master.title('Vislice')
        okvir = Frame(master, width=600, height=600)
        okvir.grid()

        self.odkrito = StringVar()  # koliko besede je do zdaj odkrito
        self.odkrito.set(self.beseda.znano)
        Label(okvir, textvariable=self.odkrito).grid(row=0, column=0)

        self.gumbi = []
        for i, l in enumerate(self.abeceda):
            b = Button(okvir, text=l, command=lambda x=i: self.preveri(x))
            self.gumbi.append(b)
            b.grid(row=i // 9, column=i % 9 + 1)

        self.platno = Canvas(okvir, width=200, height=200)
        self.platno.grid(row=1, column=0, rowspan=3)


root = Tk()
App = Aplikacija(root, Beseda('mamba'), abeceda())
root.mainloop()
