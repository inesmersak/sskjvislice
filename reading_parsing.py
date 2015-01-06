import re
import requests
import random


def abeceda():
    return "aeiourbcčdfghjklmnpsštvzž"


def naredi_slovar_naglasov():
    '''Unicode kode iz http://www.calcresult.com/reference/text/unicode-list.html'''
    slovar_naglasov = dict()
    slovar_naglasov["a"] = {
        "&#x00E0;",
        "&#x00E1;",
        "&#x00E2;",
        "&#x00E3;",
        "&#x00E4;",
        "&#x00E5;",}
    slovar_naglasov["A"] = {
        "&#x00C0;",
        "&#x00C1;",
        "&#x00C2;",
        "&#x00C3;",
        "&#x00C4;",
        "&#x00C6;",}
    slovar_naglasov["e"] = {
        "&#x00E8;",
        "&#x00E9;",
        "&#x00EA;",
        "&#x00EB;"}
    slovar_naglasov["E"] = {
        "&#x00C8;",
        "&#x00C9;",
        "&#x00CA;",
        "&#x00CB;"}
    slovar_naglasov["i"] = {
        "&#x00EC;",
        "&#x00ED;",
        "&#x00EE;",
        "&#x00EF;"}
    slovar_naglasov["I"] = {
        "&#x00CC;",
        "&#x00CD;",
        "&#x00CE;",
        "&#x00CF;"}
    slovar_naglasov["o"] = {
        "&#x00F2;",
        "&#x00F3;",
        "&#x00F4;",
        "&#x00F5;",
        "&#x00F6;"}
    slovar_naglasov["O"] = {
        "&#x00D2;",
        "&#x00D3;",
        "&#x00D4;",
        "&#x00D5;",
        "&#x00D6;"}
    slovar_naglasov["u"] = {
        "&#x00F9;",
        "&#x00FA;",
        "&#x00FB;",
        "&#x00FC;",}
    slovar_naglasov["U"] = {
        "&#x00D9;",
        "&#x00DA;",
        "&#x00DB;",
        "&#x00DC;",}
    slovar_naglasov["č"] = {
        "&#x010D;"}
    slovar_naglasov["Č"] = {
        "&#x010C;"}
    slovar_naglasov["š"] = {
        "&#x0161;"}
    slovar_naglasov["Š"] = {
        "&#x0160;"}
    slovar_naglasov["ž"] = {
        "&#x017E;"}
    slovar_naglasov["Ž"] = {
        "&#x017D;"}
    slovar_naglasov["r"] = {
        "&#x0155;",
        "&#x0157;",
        "&#x0159;",}
    slovar_naglasov["R"] = {
        "&#x0154;",
        "&#x0156;",
        "&#x0158;",}    
    return slovar_naglasov







class Beseda:
    def __init__(self, niz, definicija = None):
        self.beseda = niz
        self.definicija = definicija
        self.neznano = niz
        self.znano = ""
        for x in range(len(niz)):
            self.znano += "_"
        self.poskusi = 0
        self.napacno = ""
    def __str__(self):
        return self.beseda
    def __repr__(self):
        napis = self.beseda
        return napis

        
    def definiraj(self):
        if self.definicija != None:
            return self.definicija
        else:
            self.definicija = definicija(self.beseda)
            return self.definicija


    def ugibaj(self, niz, abc = abeceda()):
        for x in niz:
            if x not in abc:
                raise Exception("Napačen vnos!")
            elif x in self.znano or x in self.napacno:
                pass
            elif x in self.beseda:
                i = 0
                while i < len(self.beseda):
                    if x == self.beseda[i]:
                        self.znano = self.znano[:i] + x + self.znano[i+1:]
                    i += 1
                self.neznano = self.neznano.replace(x, "")
            elif x not in self.beseda:
                self.poskusi += 1
                self.napacno += x
                 
    def reseno(self):
        return len(self.neznano) == 0


def je_slovensko(beseda, abc = abeceda()):
    for x in beseda:
        if x not in abc:
            return False
    return True


def naglasi(beseda, slovar_naglasov = naredi_slovar_naglasov()):
    popravljeno = beseda
    for k in slovar_naglasov:
        for v in slovar_naglasov[k]:
            popravljeno = popravljeno.replace(v, k)
    return popravljeno


def naslov(geslo, i = 1):
    '''Spremeni vpisano geslo v url naslov SSKJ-jevega iskalnika'''
    return "http://bos.zrc-sazu.si/cgi/a03.exe?name=sskj_testa&expression=" + geslo.replace(" ", "+").replace("=*", "%3D*") + "&hs=" + str(i)

    
def stevilo_besed(geslo):
    '''Vrne stevilo besed, ki jih SSKJ najde pod danim geslom'''
    r = requests.get(naslov(geslo))
    niso = re.compile(r"Zadetkov ni bilo: ")
    s = niso.search(r.text)
    if s is None: #pogleda, če so zadetki. True = so
        so = re.compile(r'<h1 align="center">(.*) \((.+)\) <a href="http://bos.zrc-sazu.si/sskj.html">')
        s = so.search(r.text).group(2)
        return int(s.replace(".", ""))
    else:
        return 0

        
def najdi_sskj(geslo, spodnja_meja = 1, omejitev = 1000000, zgornja_dolzina = 1000000, spodnja_dolzina = 1, pogoj = False):
    '''
Dobi niz geslo in poišče vse besede, ki vsebujejo geslo. "ge=geslo" vrne točno geslo,
"ge=*geslo" ali "ge=geslo*" vrne besede, ki imajo namesto "*" še nadaljevanje besede,
"ge=*" vrne vse besede SSKJ-ja. Omejitev omeji število besed. 1000000 je več od
vseh besed v SSKJ-ju. Dolzina pove, koliko je lahko beseda dolga. pogoj: True prepusti vse
besede, ne glede na dolžino ali slovenskost.
    '''
    def pogojnost(x, pogoj):
        return ((" " not in x.beseda) and (len(l) < omejitev) and spodnja_dolzina <= len(x.beseda) <= zgornja_dolzina and je_slovensko(x.beseda)) or pogoj
    l = list()
    vzorec = re.compile(r'<font face="Arial Unicode MS"><b>.*</b></font>&nbsp;')
    vzorec2 = r'.*<font face="Arial Unicode MS"><b>(.*)</b></font>&nbsp;'
    zgornja_meja = stevilo_besed(geslo)
    #ločena primera sta zato, ker pri uporabi "ge=" ne obarva rdeče
    if ("*" in geslo) or ("ge=" in geslo):
        for i in range(spodnja_meja, zgornja_meja, 25):
            r = requests.get(naslov(geslo, i))
            s = vzorec.findall(r.text)
            for x in s:
                zadetek = re.match(vzorec2, x)
                a = Beseda(naglasi(zadetek.group(1)))
                if pogojnost(a, pogoj):
                    l += [a]
        return l
    else:
        if zgornja_meja == 0:
            return None
        else:
            for i in range(spodnja_meja, zgornja_meja, 25):
                j = 0
                r = requests.get(naslov(geslo, i))
                s = vzorec.findall(r.text)
                for x in s:
                    zadetek = re.match(vzorec2, x)
                    a = naglasi(zadetek.group(1))
                    if "<font color=red>" in a: #ustavi, ko najde vse besede, ki vsebujejo geslo
                        b = Beseda(naglasi(a).replace("<font color=red>", "").replace("</font>", ""))
                        if pogojnost(b, pogoj):
                            l += [b] 
                    else:
                        j = 1
                        break
                if j == 1:
                    break
        return l


def definicija(geslo):
    if "ge=" in geslo:
        url = naslov(geslo)
    else:
        url = naslov("ge=" + geslo)
    mnozica = list()
    r = requests.get(url)
    R = r.text.split("<b>")
    vzorec2 = r'.*<i>(.+):.*</i>'
    for x in R:
        x = x.split("//")
        for y in x:
            if "//" not in y:
                a = re.match(vzorec2, y)
                if a != None:
                    a = a.group(1)
                    a = naglasi(a)
                    mnozica.append(a)
                else:
                    pass
    return mnozica


def random_crke(tezavnost = "normal"):
    '''tezavnost "normal": ni omejitve črk, na "easy" je srednja samoglasnik'''
    if tezavnost == "normal":
        x = random.randint(0,24)
        y = random.randint(0,24)
        z = random.randint(0,24)
    elif tezavnost == "easy":
        n = random.randint(1,2)
        if n == 1:
            x = random.randint(0,5)
            y = random.randint(5,24)
            z = random.randint(5,24)
        elif n == 2:
            y = random.randint(0,5)
            x = random.randint(5,24)
            z = random.randint(5,24)
        elif n == 3:
            z = random.randint(0,5)
            y = random.randint(5,24)
            x = random.randint(5,24)
    return abeceda()[x] + abeceda()[y] + abeceda()[z]


def random_besede(tezavnost = "normal", meja = 10, zg_dolzina = 15, sp_dolzina = 3):
    crke = random_crke(tezavnost)
    c = stevilo_besed(crke)
    if c == 0:
        print("KNOPE!")
        return random_besede(tezavnost)
    a = random.randint(1, max(1, c - meja))
    bese = najdi_sskj(crke, spodnja_meja = a, omejitev = meja, zgornja_dolzina = zg_dolzina, spodnja_dolzina = sp_dolzina)
    if (bese == []) or (bese == None):
        print("LESLIE!")
        return random_besede(tezavnost)
    else:
        return bese



def random_besede2(meja = 10, zg_dolzina = 15, sp_dolzina = 3):
    return najdi_sskj(geslo = "*", spodnja_meja = random.randint(1,93140), omejitev = meja, zgornja_dolzina = zg_dolzina, spodnja_dolzina = sp_dolzina)
                      
    


##def najdi(niz, slovar_naglasov = naredi_slovar_naglasov()):
##    iskano_split = niz.split("ge=")
##    iskano = iskano_split[1]
##    if iskano.isalpa():
##        "OKEY"
##    else 
    


    
##l = list()
##slovar = naredi_slovar_naglasov()
##with open("besede.txt", "w", encoding="UTF-8") as f:
##    for i in range(1, 100, 25):
##        naslov = "http://bos.zrc-sazu.si/cgi/a03.exe?name=sskj_testa&expression=*&hs="+str(i)
##        r = requests.get(naslov)
##        vzorec = re.compile(r'<font face="Arial Unicode MS"><b>.+</b></font>&nbsp;')
##        s = vzorec.findall(r.text)
##        vzorec2 = r'<font face="Arial Unicode MS"><b>(.+)</b></font>&nbsp;'
##        for x in s:
##            a = naglasi(re.match(vzorec2, x).group(1), slovar)
##            l += [a]
##            #print(a, file=f)
