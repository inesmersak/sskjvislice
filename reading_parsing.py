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


"""
SUKANJČICA

Nekoč, pred davnimi časi, je na kmetiji skupaj z očetom živelo mlado dekle.
Njena mati jo je od mladih nog učila šivati. Po materini smrti je dekle obrt
še nadaljevalo in postalo je tako znano po svojih sposobnostih, da so jo vsi
klicali Sukanjčica.

Glas o Sukanjčici je dosegel tudi ušesa kraljice, ki jo je povabila, da bi
bila njena osebna mojškra. Sukanjčica je radostna sprejela delo, a njen
oče je bil manj navdušen. Bil je osamljen in v Sukanjčici je videl svojo
pokojno ženo; ni mu bilo všeč, da ga še ona zapušča. Po dolgotrajnem pregovarjanju
se je le vdal in Sukanjčici dovolil oditi delat na grad.

"Vsak dan bodi pred večerom doma!" ji je zabičal. "Ubogaj kraljico in kralj ter
pazi, da ne boš osramotila naše družine."

"Obljubim, da ne bom," je rekla Sukanjčica, ki ji je odleglo, da ji oče pusti
oditi.

Sprva je bila očarana nad življenjem na gradu. Občudovala je kraljičine obleke
in nakit, sline so se ji cedila ob vonjih okusne hrane, kakršne še ni jedla.
Laskali so ji pozdravi dvorjanov in nasploh se je počutila, kot da sanja.

Na žalost je vsak dan morala oditi domov k očetu, ki je bil čedalje bolj nejevoljen
zaradi njene odsotnosti. Noči je prebedela ob oknu svoje kajže in otožno opazovala
senco gradu na hribu nad vasjo. Želela si je grajskega življenja, še več, kot
ga je že imela. Še ko je spala, je sanjala o poroki s princem. Vsako jutro, ko se
je zbudila, jo je pogled na hlev ob kmetiji spomnil, kdo v resnici je.

Odločila se je, da vsaj poskusi dobiti življenje, po katerem je hrepenela,
zato je skovala načrt.

Vsako leto sta kralj in kraljica gostila velik ples na Noč treh obešencev,
največji praznik v deželi. Slavili so zmago kralja in poraz izdajalcev, ki so
bili po vojni obešeni za svoje zločine.

Starega kralja, očeta zdajšnje kraljice, je dvoličnež izzval na dvoboj. Ko se je častni
kralj odzval, je dvoličnež s seboj pripeljal množico razbojnikov, da so ga skupaj ubili.

Njegova žena, mačeha zdajnšnje krajice, je nalašč naredila splav in ni rodila kraljeviča,
ki bi podedoval kraljestvo, in obtožila kraljico čarovništva. Poročila se je z zlobnim
knezom, da si je lahko prisvojil prestol, ki ni bil njegov. 

Kraljica je s pomočjo prijaznega mladeniča premagala dvoličneža, prisvojitelja in
svojo mačeho ter si tako priborila svoje kraljestvo nazaj. Vsako leto je praznovala
obletnico dneva, ko so podlo trojico obesili.

Sukanjčica se je odločila, da se bo še sama udeležila plesa v maskah, kamor so smeli
le najvplivnejši in najpremožnejši. Kraljica ji je dovolj zaupala, da ji je pustila
domov jemati blago za šivanje njenih oblek. Sukanjčica je pri vsaki obleki nekaj
malega vzela zase in si sešila veličastno obleko, v kateri je ne bi nihče prepoznal. 
    
Na praznični večer je počakala, da je oče zaspal, nato pa se preoblekla in izmuznila
ven. Pretihotapila se je do gradu in pazila, da se ni umazala. Gostov je bilo toliko,
da je stražarji niso podrobno pregledali in so jo kar spustili skozi, ko se jim je
prijazno nasmehnila. 

V gradu jo je pričakal nepozaben prizor. Na dvorišču so postavili plesišče pod zvezdami
in tremi lutkami, visečimi z vislic. Vsa gospoda je plesala: vzdolž vrst, v parih ali
pa so se vrteli v krogu. Sluge so nosili srebrne pladnje, navrhane z vsemi vrstami
hrane in pijače. Vsakdo je nosil kostum in vsak je bil lepši od prejšnjega, a kostum
Sukanjčice je bil najbolj čudovit.

Sprehajala se je med glasnimi gosti, z enega pladnja vzela kozarec belega vina, z drugega
rdečega, iz vsakega naredila en požirek in ju nato zamenjala za hrano. Grižljaj sire,
kos mesa, ugriz sadežev... Vse je poskusila.

Usedla se je na leseno klop ob balkonu, ki je gledal proti dolini z njeno vasjo.
Na balkonu je stal par, temnolasa mlada dama v borovničevo modri obleki in postaven mladenič
v črnem, ki je v rokah držal ananas. Grb na njegovem plašču je prepoznala. Pripadal je deželi Potemle, znani po
poštenih in pametnih prebivalcih.

"Misliš, da lahko vržem tale ananas do tiste kmetije, mimo katere smo šli?" je vprašal mladenič.

"Ne bodi nor, komaj ga lahko tale vržeš do dna tistega pobočja."

"Stavim, da ga vržem na streh hleva," je vztrajal, čemur se je dama zasmejala. "Sem ti povedal
o tistemu kozlu, ki je vsak dan splezal na vrh hleva? Vrhhlevni Ikar smo mu rekli."

"Koze ne morejo splezati na vrh hleva. Neumnosti kvasiš."

"Bil je kozel. Vrhhlevni Ikar. In kozli znajo plezati po skoraj navpični skali."

"Vseeno ne verjamem. Kdo da kozlu ime Ikar?"

"Vsak vrhhleven kozel si zasluži močno ime. Najprej sem mu pravil Vrhhlevni Dedal, ampak
enkrat se je vnel hlev medtem, ko je bil on na vrhu in ni mogel skočiti dol. Mogoče je
bil preveč prestrašen. Vrhhlevni Ikar se mi je po tem zdelo primernejše."

"Ti imaš vedno neumne pripovedke. Plemič si, zakaj si se sploh ukvarjal s kozami?"

"Poskušal sem razviti gorsko konjenico. Oziroma kozlenico. Nič ne bi moglo ustaviti
naše vojske, če bi mi uspelo."

"Razen naključnih požarov."

"Prepričan sem, da je bila sabotaža."

"In koliko si sploh dosegel?"

"Vrhhleven Ikar je bil najokusnejša pečenka, kar sem jih jedel. Hmmm, mogoče bo ta
vrhhleven ananas prav tako božanski."

Temnolasa dama je le skimala z glavo. 

"Vas lahko prosim za ples?" je Sukanjčica slišala od strani in se obrnila. K njej je
pristopil najlepši moški, kar jih je kadarkoli videla. Imel je sinje modre oči in
pšenično rumene lase, oblečen pa je bil v kostum, ki se je lahko kosal z njenim.

"Seveda, z veseljem," je rekla in pozabila na omikanost, ki se je je naučila.

Plesala sta ves večer in celo noč. Predstavil se ji je kot princ sosednjega kraljestva
in naslednik bajnega bogastva. Poskušal je izvedeti, kdo je ona, vendar je iz strahu
vsakič zamenjala temo in ohranjala skrivnost svojega porekla.

Ko se je začelo daniti, se je spomnila, da mora oditi domov. Hitro se je poslovila
od svojega princa in stekla iz gradu.

"Čakaj!" je zavpil za njo. "Sploh ne vem, kako ti je ime!"

"Oprosti," je s solzami v očeh hlipala in tekla vso pot domov. Bala se je, da se je oče
že zbudil in da bo jezen, ker nje ni.

Z nogo je zadela ob nekaj trdega in padla po tleh. Blato ji je uničilo obleko, v katero
je vložila toliko truda in časa. Pogledala je, ob kaj se je spotaknila.

Bil ja ananas.

Hitro se je pobrala in stekla domov. Počasi je odprla vrata. Oddahnila si je, ker očeta
ni videla. Po prstih je odšla v svojo sobo in se preoblekla v delavska oblačila. Čimprej
je nameravala pomolzti kravo in se poskusiti izogniti očetovemu srdu.

Bilo je prepozno. Vrata so se s treskom odprla in v sobo je planil oče z zariplim obrazom.

"Kje si se potepala ponoči? Ravno takih stvari sem se bal, ko sem ti dovolil iti za mojškro,"
je tulil. "Ne bom dovolil, da se bo moja hči vlačila naokoli!" Zagledal je njeno blatno, a
še vedno prečudovito obleko na postelji. "Kaj je to?"

"Lahko ti pojasnim, oče!" ga je poskušala miriti.

"Na grad si šla, kajne? Misliš, da nisi dovolj dobra zame in za tako življenje? Ti bom že
pokazal, kaj si jaz mislim!" Pograbil je obleko, odprl okno in jo zalučal skozenj.

"Ne!" je zavpila Sukanjčica. "Ti drekobrbec!"

"Naj ti bo to v kazen, da me ne ubogaš," je rekel, odšel iz sobe in za sabo glasno zaloputnil
z vrati.

Sukanjčica se je sesedla na posteljo in jokala. Vsake toliko časa je pogledala skozi okno
in videla svojo umazano, vrhhlevno obleko ter se spomnila na princa, ki ga je pustila.
Pogledala je še grad, ki je predstavljal življenje, kakršnega ne bo nikoli imela, in
jokala je še močneje.

Nato je od zunaj zaslišala peketanje kopit. Nagnila je glavo skozi okno in zagledala svojega
princa na belem konju.

"Oprostite," je rekel princ. "Mimo sem jahal in opazil obleko na vašem hlevu. Ali mogoče..."
Ustavil se je sredi povedi. "To ste vi! Vi ste gospodična, s katero sem plesal včeraj!"

"Da, to sem jaz," je priznala. "Ime mi je Sukanjčica in sem navadna mojškra. Nisem vas hotela
zavajati, oprostite."

"Brez opravičil, prosim vas. Vseeno mi je, kdo ste. Ne morem nehati misliti na vas. Zadal sem
si, da vas najdem, in usoda mi je naklonila, da mi je to uspelo tako hitro. Ljubim vas, Sukanjčica,"
je rekel.

"In jaz vas, moj princ," je rekla nazaj.

"Je to res?" je vprašal oče, ki se je prikazal iz hleva. "Ti ljubiš tega princa in on ljubi tebe?"

"Da, oče," je rekla. "In ne moreš me ustaviti."

"Niti te nočem," je rekel. "Žal mi je za vse, kar sem ti naredil. Želim ti le, da bi bila vesela."

"Oh, oče," je rekla Sukanjčica. "Oprosti mi, da sem ti rekla drekobrbec."

"Saj sem se res tako obnašal." Obrnil se je proti princu. "Če se želite poročiti z mojo hčerko,
imate moj blagoslov."

"Odlična novica," je rekel princ. "Sukanjčica, bi se poročila z mano?"

"Da, tisočkrat da."

In tako sta Sukanjčica in njen princ živela do konca svojih dni.
"""



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
