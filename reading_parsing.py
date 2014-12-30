import re
import requests


def naredi_slovar_naglasov():
    slovar_naglasov = dict()
    slovar_naglasov["a"] = {
        "&#x00E0;",
        "&#x00E1;",
        "&#x00E2;"}
    slovar_naglasov["A"] = {
        "&#x00C1;"}
    slovar_naglasov["e"] = {
        "&#x00E8;",
        "&#x00E9;",
        "&#x00EA;"}
    slovar_naglasov["i"] = {
        "&#x00EC;",
        "&#x00ED;",
        "&#x00EE;"}
    slovar_naglasov["o"] = {
        "&#x00F2;",
        "&#x00F3;",
        "&#x00F4;"}
    slovar_naglasov["u"] = {
        "&#x00F9;",
        "&#x00FA;",
        "&#x00FB;"}
    slovar_naglasov["č"] = {
        "&#x010D;"}
    slovar_naglasov["š"] = {
        "&#x0161;"}
    slovar_naglasov["ž"] = {
        "&#x017E;"}
    slovar_naglasov["r"] = {
        "&#x0155;"}
    return slovar_naglasov


def naglasi(beseda, slovar_naglasov):
    popravljeno = beseda
    for k in slovar_naglasov:
        for v in slovar_naglasov[k]:
            popravljeno = popravljeno.replace(v, k)
    return popravljeno

l = list()
slovar = naredi_slovar_naglasov()
with open("besede.txt", "w", encoding="UTF-8") as f:
    for i in range(1, 100, 25):
        naslov = "http://bos.zrc-sazu.si/cgi/a03.exe?name=sskj_testa&expression=*&hs="+str(i)
        r = requests.get(naslov)
        vzorec = re.compile(r'<font face="Arial Unicode MS"><b>.+</b></font>&nbsp;')
        s = vzorec.findall(r.text)
        vzorec2 = r'<font face="Arial Unicode MS"><b>(.+)</b></font>&nbsp;'
        for x in s:
            a = naglasi(re.match(vzorec2, x).group(1), slovar)
            l += [a]
            print(a, file=f)