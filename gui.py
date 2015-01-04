from tkinter import *


class Aplikacija():
    def preveri(self, gumb=None, *args):
        print(self.abeceda[gumb])

    def posodobi(self):
        pass

    def __init__(self, master, beseda, abeceda):
        self.beseda = beseda
        self.abeceda = abeceda

        master.title('Vislice')
        okvir = Frame(master, width=600, height=600)
        okvir.grid()

        self.odkrito = StringVar()  # koliko besede je do zdaj odkrito
        self.odkrito.set('_ ' * (len(self.beseda)-1) + '_')
        Label(okvir, textvariable=self.odkrito).grid(row=0, column=0)

        for i, l in enumerate(self.abeceda):
            Button(okvir, text=l, command=lambda x=i: self.preveri(x)).grid(row=i // 9, column=i % 9 + 1)

        self.platno = Canvas(okvir, width=200, height=200)
        self.platno.grid(row=1, column=0, rowspan=3)



root = Tk()
App = Aplikacija(root, 'človek', 'ABCČDEFGHIJKLMNOPRSŠTUVZŽ')
root.mainloop()
