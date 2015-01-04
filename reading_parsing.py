import re
import requests


class Beseda:
    def __init__(self, niz, definicija = None):
        self.beseda = niz
        self.definicija = definicija
        self.neznano = set()
        for x in range(len(niz)):
            self.neznano.add(x)
        self.znano = {}
    def __str__(self):
        return self.beseda
    def __repr__(self):
        napis = self.beseda + ": \n ZNANO:"
        for x in self.znano:
            napis += " " + self.beseda[x]
        napis += " \n NEZNANO:" 
        for x in self.neznano:
            napis += " " + self.beseda[x]
        return napis
        


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
        return int(s)
    else:
        return 0

        
def najdi_sskj(geslo, spodnja_meja = 1):
    l = list()
    if geslo == "*":
        for i in range(spodnja_meja, 93154, 25):
            r = requests.get(naslov(geslo, i))
            vzorec = re.compile(r'<font face="Arial Unicode MS"><b>.+</b></font>&nbsp;')
            s = vzorec.findall(r.text)
            vzorec2 = r'<font face="Arial Unicode MS"><b>(.+)</b></font>&nbsp;'
            for x in s:
                a = Beseda(naglasi(re.match(vzorec2, x).group(1), naredi_slovar_naglasov()))
                l += [a]
        return l
    else:
        zgornja_meja = stevilo_besed(geslo)
        if zgornja_meja == 0:
            return None
        return l
    
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
