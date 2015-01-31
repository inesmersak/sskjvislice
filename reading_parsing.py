import re
import requests
import random
import resources
from classes import *


def je_slovensko(beseda, abc=resources.abe):
    """Preveri, ali vnešena beseda vsebuje le slovenske črke ter vrne True
    ali false"""
    for x in beseda:
        if x not in abc:
            return False
    return True


def naglasi(beseda, slovar_naglasov=resources.slovar_naglasov):
    """SSKJ uporablja unicode kodiranje, kar pomeni, da so šumniki in črke
    z naglasi zapisani s kodo. Ta funkcija jih zamenja s pravilno črko, kakor
    je določeno v slovarju naglasov."""
    popravljeno = beseda
    for k in slovar_naglasov: #za vsako črko
        for v in slovar_naglasov[k]: #pogleda vse različice naglasov    
            popravljeno = popravljeno.replace(v, k) #in jih zamenja
    return popravljeno


def naslov(geslo, i=1):
    """Spremeni vpisano geslo v url naslov SSKJ-jevega iskalnika"""
    return "http://bos.zrc-sazu.si/cgi/a03.exe?name=sskj_testa&expression=" + \
           geslo.replace(" ", "+").replace("ge=", "ge%3D") + "&hs=" + str(i)
    #spremeni tudi nekatere parametre, ki jih lahko vnesemo v iskalnik

    
def stevilo_besed(geslo):
    """Vrne stevilo besed, ki jih SSKJ najde pod danim geslom"""
    #SSKJ na vrhu izpiše število besed, ki vsebujejo iskano geslo kot koren
    #ali se pojavlja v definiciji.
    r = requests.get(naslov(geslo))
    niso = re.compile(r"Zadetkov ni bilo: ")
    s = niso.search(r.text)
    if s is None:  # pogleda, če so zadetki. True = so
        so = re.compile(r'<h1 align="center">(.*) \((.+)\) <a href="http://bos.zrc-sazu.si/sskj.html">')
        s = so.search(r.text).group(2)
        return int(s.replace(".", ""))
    else:
        return 0

        
def najdi_sskj(geslo, spodnja_meja=1, omejitev=1000000, zgornja_dolzina=1000000, spodnja_dolzina=1, pogoj=False):
    """
Dobi niz geslo in poišče vse besede, ki vsebujejo geslo. "ge=geslo" vrne točno geslo,
"ge=*geslo" ali "ge=geslo*" vrne besede, ki imajo namesto "*" še nadaljevanje besede,
"ge=*" vrne vse besede SSKJ-ja. Omejitev omeji število besed. 1000000 je več od
vseh besed v SSKJ-ju. Dolzina pove, koliko je lahko beseda dolga. pogoj: True prepusti vse
besede, ne glede na dolžino ali slovenskost.
    """
    def pogojnost(x):
        return ((" " not in x.beseda) and (len(l) < omejitev)
                and spodnja_dolzina <= len(x.beseda) <= zgornja_dolzina
                and je_slovensko(x.beseda)) or pogoj
    # pogojnost omeji besede na takšne, kakršne iščemo. Svoja funkcija je zato, ker se uporablja na dveh mestih.
    l = list()
    vzorec = re.compile(r'<font face="Arial Unicode MS"><b>.*</b></font>&nbsp;')
    vzorec2 = r'.*<font face="Arial Unicode MS"><b>(.*)</b></font>&nbsp;'
    zgornja_meja = stevilo_besed(geslo)
    # ločena primera sta zato, ker pri uporabi "ge=" ne obarva rdeče
    # SSKJ ima besede razvrščene po 25 na stran, ki ima v URL-ju zaporedno številko prve. Naslednja stran se začne 
    # z za 25 višjo številko.
    if ("*" in geslo) or ("ge=" in geslo):
        for i in range(spodnja_meja-1, zgornja_meja, 25):
            r = requests.get(naslov(geslo, i))
            s = vzorec.findall(r.text)
            for x in s:
                zadetek = re.match(vzorec2, x)
                a = Beseda(naglasi(zadetek.group(1)))
                if pogojnost(a):
                    l += [a]
                    if len(l) >= omejitev:
                        return l
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
                    if "<font color=red>" in a:
                        # ustavi, ko najde vse besede, ki vsebujejo geslo, kar določa s tem, ali je beseda rdeča ali ne.
                        b = Beseda(naglasi(a).replace("<font color=red>", "").replace("</font>", ""))
                        if pogojnost(b):
                            l += [b]
                            if len(l) >= omejitev:
                                return l
                    else:
                        j = 1
                        break
                if j == 1:
                    break
        return l


def definicija(geslo):
    """Poišče definicijo besede, vnešene kot geslo, če se nahaja v SSKJ."""
    if "ge=" in geslo:
        url = naslov(geslo)
    else:
        url = naslov("ge=" + geslo)
    mnozica = list()
    r = requests.get(url)
    big_r = r.text.split("<b>")
    # Vsaka beseda je napisano odebeljeno. Če ima več definicij, so napisane po odebeljenih številkah.
    # S splitom dobimo tekst posameznih definicij v obeh primerih.
    # Iskane definicije so napisane poševno in se končajo z ":", če je za njimi naveden primer.
    # Pri nekaterih besedah primera ni.
    vzorec2 = r'.*<i>(.+)(:</i>|</i> )'
    for x in big_r:
        x = x.split("//")
        for y in x:
            if "//" not in y:
                a = re.match(vzorec2, y)
                if a:
                    a = a.group(1)
                    a = naglasi(a).replace(":", "")
                    mnozica.append(a)
                else:
                    pass
    # Definicija nekaterih besed pravi, da moramo gledati drugo besedo.
    if mnozica == []:
        vzorec1 = r'.* <font size=-1>gl.</font> (.+) <font face="Lucida Sans Unicode">&#x266A;</font>'
        a = re.match(vzorec1, big_r[1])
        if a:
            a = a.group(1)
            a = naglasi(a)
            a = a.split(" ")[0]
            mnozica = definicija(str(a))
    return mnozica


def definiraj(beseda):
    """Še en možen način, da dodaš definicijo besedi."""
    if beseda.definicija:
        return beseda.definicija
    else:
        beseda.definicija = definicija(beseda.beseda)
        return beseda.definicija


def random_crke(tezavnost="normal"):
    """tezavnost "normal": ni omejitve črk, na "easy" je srednja samoglasnik"""
    # Neuporabljen način iskanje naključnih besed.
    # To si izmisli niz treh naključnih črk.
    if tezavnost == "normal":
        x = random.randint(0, 24)
        y = random.randint(0, 24)
        z = random.randint(0, 24)
    elif tezavnost == "easy":
        n = random.randint(1, 2)
        if n == 1:
            x = random.randint(0, 5)
            y = random.randint(5, 24)
            z = random.randint(5, 24)
        elif n == 2:
            y = random.randint(0, 5)
            x = random.randint(5, 24)
            z = random.randint(5, 24)
        elif n == 3:
            z = random.randint(0, 5)
            y = random.randint(5, 24)
            x = random.randint(5, 24)
    return resources.abe[x] + resources.abe[y] + resources.abe[z]


def random_besede(tezavnost="normal", meja=10, zg_dolzina=15, sp_dolzina=3):
    # Neuporabljen način iskanje naključnih besed.
    # Iz naključnega niza treh črk poišče besedo. Traja predolgo.
    crke = random_crke(tezavnost)
    c = stevilo_besed(crke)
    if c == 0:
        return random_besede(tezavnost)
    a = random.randint(1, max(1, c - meja))
    bese = najdi_sskj(crke, spodnja_meja=a, omejitev=meja, zgornja_dolzina=zg_dolzina, spodnja_dolzina=sp_dolzina)
    if (bese == []) or (bese is None):
        return random_besede(tezavnost)
    else:
        return bese


def random_beseda(sp_dolzina=3, zg_dolzina=8):
    """Vrne naključno besedo razreda Beseda, katere dolžina je med parametroma."""
    # Izbere naključno številko in išče najbližjo ustrezno besedo z zaporedno številko, večjo ali enako od izbrane.
    # Mogoče je še določati dolžino besede.
    return najdi_sskj(geslo="*", spodnja_meja=random.randint(1, 93140), omejitev=1, zgornja_dolzina=zg_dolzina,
                      spodnja_dolzina=sp_dolzina)[0]
