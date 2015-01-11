import reading_parsing
from tkinter import *
from resources import *


class Aplikacija():
    def pot_do_slike(self):
        return 'slike/vislice' + str(11-self.beseda.preostali_poskusi) + '.png'

    def posodobi_sliko(self):
        self.platno.delete(ALL)
        self.platno.background = PhotoImage(file=self.pot_do_slike())
        self.platno.create_image(0, 0, image=self.platno.background, anchor='nw')

    def preveri(self, gumb=None):
        if type(gumb) == int:  # ce je uporabnik pritisnil na gumb na zaslonu
            self.gumbi[gumb].grid_remove()
            guess = self.abeceda[gumb]
        elif type(gumb) == Event:  # ce je uporabnik pritisnil na tipko na tipkovnici
            guess = gumb.char
            if guess in self.abeceda:
                indeks = self.abeceda.find(guess)
                self.gumbi[indeks].grid_remove()
        self.novo = False
        try:
            r = self.beseda.ugibaj(guess)
            self.posodobi(r)
        except ValueError:
            pass

    def posodobi(self, r=None):
        if r:
            self.odkrito.set(self.beseda.za_gui())
        else:
            self.napacno.set(self.beseda.preostali_poskusi)
            self.posodobi_sliko()
        if self.beseda.reseno() or self.beseda.preostali_poskusi == 0:
            self.odkrito.set(self.beseda.za_gui(True))
            self.defin.set(reading_parsing.definiraj(self.beseda))
            self.posodobi_sliko()
            for b in self.gumbi:
                b.grid_remove()
            self.beseda = reading_parsing.random_beseda()
            self.novo = True

    def nova_igra(self, *args):
        if not self.novo:
            self.beseda = reading_parsing.random_beseda()
            self.novo = True
        for b in self.gumbi:
            b.grid()
        self.defin.set('')
        self.posodobi_sliko()
        self.odkrito.set(self.beseda.za_gui())
        self.napacno.set(self.beseda.preostali_poskusi)

    def __init__(self, master, beseda, abc):
        self.beseda = beseda
        self.abeceda = abc
        self.spaces = 2
        self.novo = True  # nam pove ali je beseda povsem nova ali ne

        master.title('Vislice')
        master.minsize(width=380, height=300)

        # meni
        self.meni = Menu(master)
        master.config(menu=self.meni)
        self.meni.add_command(label="Nova igra", command=self.nova_igra)
        self.meni.add_command(label="Zapri", command=quit)

        okvir = Frame(master)
        okvir.grid(row=0, column=0)

        self.odkrito = StringVar()  # koliko besede je do zdaj odkrito
        self.odkrito.set(self.beseda.za_gui())
        Label(okvir, textvariable=self.odkrito).grid(row=0, column=0)

        self.defin = StringVar()
        Label(okvir, textvariable=self.defin).grid(row=1, column=0)

        novo = Button(okvir, text="Nova igra", command=self.nova_igra)
        novo.grid(row=2, column=0)

        tipkovnica = Frame(master)
        tipkovnica.grid(row=0, column=1)
        self.gumbi = []
        for i, l in enumerate(self.abeceda):
            b = Button(tipkovnica, text=l, command=lambda x=i: self.preveri(x))
            self.gumbi.append(b)
            b.grid(row=i // 9, column=i % 9)

        self.platno = Canvas(master, width=200, height=200)
        self.platno.grid(row=1, column=0)
        self.platno.background = PhotoImage(file=self.pot_do_slike())
        self.platno.create_image(0, 0, image=self.platno.background, anchor='nw')

        okvir1 = Frame(master)
        okvir1.grid(row=2, column=0)
        self.napacno = StringVar()
        self.napacno.set(self.beseda.preostali_poskusi)
        Label(okvir1, text="Preostali poskusi: ").grid(row=0, column=0)
        Label(okvir1, textvariable=self.napacno).grid(row=0, column=1)

        # bindingi
        master.bind("<Key>", self.preveri)
        master.bind("<F1>", self.nova_igra)

root = Tk()
App = Aplikacija(root, reading_parsing.random_beseda(), abeceda())
root.mainloop()
