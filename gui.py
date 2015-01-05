from tkinter import *


class Aplikacija():
    def preveri(self, gumb=None, *args):
        guess = self.abeceda[gumb]
        if guess in self.beseda:
            self.posodobi(guess)
        else:
            self.posodobi()

    def posodobi(self, r=None):
        if r:
            nov_string = ''
            for l in self.beseda:
                if l == r:
                    nov_string += r + ' ' * self.spaces
                else:
                    nov_string += '_' + ' ' * self.spaces
            self.odkrito.set(nov_string[:len(nov_string)-1])

    def __init__(self, master, beseda, abeceda):
        self.beseda = beseda.upper()
        self.abeceda = abeceda
        self.spaces = 2

        master.title('Vislice')
        okvir = Frame(master, width=600, height=600)
        okvir.grid()

        self.odkrito = StringVar()  # koliko besede je do zdaj odkrito
        self.odkrito.set(('_' + (' ' * self.spaces)) * (len(self.beseda)-1) + '_')
        Label(okvir, textvariable=self.odkrito).grid(row=0, column=0)

        for i, l in enumerate(self.abeceda):
            Button(okvir, text=l, command=lambda x=i: self.preveri(x)).grid(row=i // 9, column=i % 9 + 1)

        self.platno = Canvas(okvir, width=200, height=200)
        self.platno.grid(row=1, column=0, rowspan=3)


root = Tk()
App = Aplikacija(root, 'mamba', 'ABCČDEFGHIJKLMNOPRSŠTUVZŽ')
root.mainloop()
