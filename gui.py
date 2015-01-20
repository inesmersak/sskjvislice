import reading_parsing
import resources
from tkinter import *


class Aplikacija():
    def pot_do_slike(self):
        """ Vrne path do slike, ki bo prikazana, glede na preostale poskuse uporabnika. """
        return 'slike/vislice' + str(11-self.beseda.preostali_poskusi) + '.png'

    def polepsaj_definicijo(self):
        """ Poklice funkcijo definiraj iz datoteke reading_parsing, dobljen seznam pa spremeni v niz in olepsa za
        prikaz:
        postavi stevilko pred vsakim novim pomenom besede, doda prelom vrstice, kjer je definicija predolga. Nazadnje
        tudi prikaže definicijo na zaslonu (posodobi StringVar self.defin)."""
        sez = reading_parsing.definiraj(self.beseda)
        niz = ''
        for i, x in enumerate(sez):
            niz += str(i + 1) + '.  '
            x = x.split()
            for j, l in enumerate(x):
                niz += l + ' '
                if j > 0 and j % 9 == 0 and len(x) != j+1:
                    niz += '\n'
            niz += '\n'
        self.defin.set(niz)
        return niz

    def posodobi_sliko(self):
        """ Metoda, ki posodobi platno: najprej odstrani vse prejšnje elemente (torej prejšnjo sliko), potem pridobi
        pot nove slike s pomočjo metode pot_do_slike, nakar to sliko prikaže na platnu. """
        self.platno.delete(ALL)
        self.platno.background = PhotoImage(file=self.pot_do_slike())
        self.platno.create_image(0, 0, image=self.platno.background, anchor='nw')

    def preveri(self, gumb=None):
        """ Se poklice, kadar uporabnik pritisne tipko na tipkovnice ali na gumb, prikazan v graficnem vmesniku. Sprejme
        parameter gumb, ki je celo stevilo, ce je uporabnik pritisnil na gumb, in objekt razreda Event, ce je uporabnik
        pritisnil na tipko. Glede na izbran znak odstrani gumb iz graficnega vmesnika, in poskusa poklicati metodo
        ugibaj razreda Beseda. V kolikor je znak, ki ga je uporabnik izbral, napacen, metoda ulovi napako,
        ki se pri tem zgodi, in jo izpiše. """
        if type(gumb) == int:  # ce je uporabnik pritisnil na gumb na zaslonu
            self.gumbi[gumb].grid_remove()
            guess = self.abeceda[gumb]
        elif type(gumb) == Event:  # ce je uporabnik pritisnil na tipko na tipkovnici
            guess = gumb.char
            if guess in self.abeceda and guess != '':
                indeks = self.abeceda.find(guess)
                self.gumbi[indeks].grid_remove()  # ce igra ne tece, potem so takoalitako vsi gumbi ze odstranjeni
        if self.gamestate:
            self.novo = False  # ko je uporabnik enkrat ugibal, potem beseda ni vec nova - ob naslednjem klicu nove
            # igre se izbere druga beseda
        try:
            if self.gamestate:  # v kolikor igra ne tece, potem pritisk na gumb/tipko ne spremeni nicesar
                r = self.beseda.ugibaj(guess)
                self.posodobi(r)
        except ValueError as e:
            print(e)

    def posodobi(self, r=None):
        """ Glede na to, ali je izbrani znak del besede ali ne, ta metoda posodobi niz z znanimi crkami,
        stevilo preostalih poskusov in sliko. V kolikor je igra ze koncana (torej je uporabnik uganil besedo ali pa mu
        je zmanjkalo poskusov), metoda odkrije iskano besedo, posodobi sliko, odstrani vse preostale gumbe z zaslona,
        posodobi statistiko, prridobi in prikaze definicijo s pomocjo metode polepsaj_definicijo, nazadnje pa se
        pridobi besedo za novo igro. """
        if r:
            self.odkrito.set(self.beseda.za_gui())
        else:
            self.napacno.set(self.beseda.preostali_poskusi)
            self.posodobi_sliko()
        if self.beseda.reseno() or self.beseda.preostali_poskusi == 0:  # igre je konec, ce je beseda uganjena ali ce
            #  je uporabniku zmanjkalo poskusov
            self.gamestate = False
            self.odkrito.set(self.beseda.za_gui(True))
            self.posodobi_sliko()
            for b in self.gumbi:
                b.grid_remove()
            if self.beseda.reseno():
                self.zmage.set(str(int(self.zmage.get()) + 1))
            elif self.beseda.preostali_poskusi == 0:
                self.porazi.set(str(int(self.porazi.get()) + 1))
            self.klici_def.grid()

    def nova_igra(self, *args):
        """ Se poklice, kadar uporabnik klikne na gumb 'Nova igra', tipko F1, ali pa ce v meniju izbere moznost 'Nova
        igra'. Posodobi graficni vmesnik tako, da je pripravljen na novo igro: ponovno prikaze vse gumbe s crkami,
        posodobi sliko, stevilo preostalih poskusov in ze znane dele besed (na zacetku so to sami podcrtaji).
        V kolikor beseda, ki je spravljena v atributu beseda, ni nova (torej v kolikor funkcije za pridobitev nove
        besede nismo klicali ze prej, recimo ob koncu igre), se poklice tudi funkcija random_beseda iz datoteke
        reading_parsing."""
        self.beseda = reading_parsing.random_beseda()
        self.novo = True
        # if not self.novo:
        #     self.beseda = reading_parsing.random_beseda()
        #     self.novo = True
        self.klici_def.grid_remove()
        for b in self.gumbi:
            b.grid()
        self.defin.set('')
        self.posodobi_sliko()
        self.odkrito.set(self.beseda.za_gui())
        self.napacno.set(self.beseda.preostali_poskusi)
        self.gamestate = True

    def quit(self, *args):
        root.destroy()

    def __init__(self, master, beseda, abc):
        self.beseda = beseda
        self.abeceda = abc
        self.spaces = 2  # lahko nastavimo stevilo presledkov, ki naj bodo med podcrtaji/crkami v prikazani besedi
        self.novo = True  # nam pove, ali je beseda povsem nova oz. ali je uporabnik ze zacel ugibati
        self.gamestate = True  # nam pove, ali igra tece; v kolikor je igre konec, igra ne tece vec

        master.title('Vislice')
        master.minsize(width=380, height=300)

        # ZACETEK MENIJA
        self.meni = Menu(master)
        master.config(menu=self.meni)
        self.meni.add_command(label="Nova igra  [F1] ", command=self.nova_igra)
        self.meni.add_command(label="Zapri  [Esc]", command=self.quit)
        # KONEC MENIJA

        # ZACETEK OKVIRJA Z BESEDO
        okvir = Frame(master)
        okvir.grid(row=0, column=0)

        self.odkrito = StringVar()  # koliko besede je do zdaj odkrito
        self.odkrito.set(self.beseda.za_gui())
        Label(okvir, textvariable=self.odkrito).grid(row=0, column=0)

        self.defin = StringVar()  # definicija se prikaze naknadno, po koncu igre
        self.klici_def = Button(okvir, text="Definicija", command=self.polepsaj_definicijo)
        self.klici_def.grid(row=1, column=0)
        self.klici_def.grid_remove()
        Label(okvir, textvariable=self.defin).grid(row=2, column=0)

        novo = Button(okvir, text="Nova igra", command=self.nova_igra)
        novo.grid(row=3, column=0)
        # KONEC OKVIRJA Z BESEDO

        # ZACETEK OKVIRJA S TIPKOVNICO
        tipkovnica = Frame(master)
        tipkovnica.grid(row=0, column=1)
        self.gumbi = []
        for i, l in enumerate(self.abeceda):
            b = Button(tipkovnica, text=l, command=lambda x=i: self.preveri(x))
            self.gumbi.append(b)
            b.grid(row=i // 9, column=i % 9)
        # KONEC OKVIRJA S TIPKOVNICO

        # ZACETEK PLATNA
        self.platno = Canvas(master, width=200, height=200)
        self.platno.grid(row=1, column=0)
        self.platno.background = PhotoImage(file=self.pot_do_slike())
        self.platno.create_image(0, 0, image=self.platno.background, anchor='nw')
        # KONEC PLATNA

        # ZACETEK OKVIRJA S STATISTIKO
        statistika = LabelFrame(master, text="Statistika", font="bold", padx=8, pady=8)
        statistika.grid(row=1, column=1, sticky='s')
        self.zmage = StringVar()
        self.zmage.set(0)
        self.porazi = StringVar()
        self.porazi.set(0)
        Label(statistika, text="Zmage: ").grid(row=0, column=0, sticky='w')
        Label(statistika, textvariable=self.zmage).grid(row=0, column=1, sticky='e')
        Label(statistika, text="Porazi: ").grid(row=1, column=0, sticky='w')
        Label(statistika, textvariable=self.porazi).grid(row=1, column=1, sticky='e')
        # KONEC OKVIRJA S STATISTIKO

        # ZACETEK OKVIRJA S PREOSTALIMI POSKUSI
        okvir1 = Frame(master)
        okvir1.grid(row=2, column=0)
        self.napacno = StringVar()
        self.napacno.set(self.beseda.preostali_poskusi)
        Label(okvir1, text="Preostali poskusi: ").grid(row=0, column=0)
        Label(okvir1, textvariable=self.napacno).grid(row=0, column=1)
        # KONEC OKVIRJA S PREOSTALIMI POSKUSI

        # BINDINGI
        master.bind("<Key>", self.preveri)
        master.bind("<F1>", self.nova_igra)
        master.bind("<Escape>", self.quit)

root = Tk()
App = Aplikacija(root, reading_parsing.random_beseda(), resources.abe)
root.mainloop()
