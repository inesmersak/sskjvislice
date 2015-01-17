def abeceda():
    return "abcčdefghijklmnoprsštuvzž"


def naredi_slovar_naglasov():
    """Unicode kode iz http://www.calcresult.com/reference/text/unicode-list.html"""
    slovar_naglasov = dict()
    slovar_naglasov["a"] = {
        "&#x00E0;",
        "&#x00E1;",
        "&#x00E2;",
        "&#x00E3;",
        "&#x00E4;",
        "&#x00E5;"}
    slovar_naglasov["A"] = {
        "&#x00C0;",
        "&#x00C1;",
        "&#x00C2;",
        "&#x00C3;",
        "&#x00C4;",
        "&#x00C6;"}
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
        "&#x00FC;"}
    slovar_naglasov["U"] = {
        "&#x00D9;",
        "&#x00DA;",
        "&#x00DB;",
        "&#x00DC;"}
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
        "&#x0159;"}
    slovar_naglasov["R"] = {
        "&#x0154;",
        "&#x0156;",
        "&#x0158;"}
    return slovar_naglasov

abe = abeceda()
slovar_naglasov = naredi_slovar_naglasov()