import bottle


@bottle.get("/static/<ime_datoteke:path>")
def static(ime_datoteke):
    return bottle.static_file(ime_datoteke, root="views")


@bottle.get("/img/<ime_datoteke:path>")
def img(ime_datoteke):
    return bottle.static_file(ime_datoteke, root="img")


@bottle.get("/")
def get_index():
    return bottle.template("index")


@bottle.get("/moji-portfelji/")
def get_moji_portfelji():
    '''TODO'''
    portfelj1 = {
        "id" : 1,
        "ime" : "kripto:)",
        "cena" : 2.13,
        "vrednost" : 103.14,
        "donos" : 101.01,
        "trend" : 0.4
    }
    portfelj2 = {
        "id" : 2,
        "ime" : "slovenske_delnice",
        "cena" : 205.15,
        "vrednost" : 198.12,
        "donos" : -7.03,
        "trend" : -1.5
    }
    portfelji = [portfelj1, portfelj2, portfelj1, portfelj2, portfelj1, portfelj2, portfelj1, portfelj2, portfelj1, portfelj2, portfelj1]
    return bottle.template("moji-portfelji", portfelji=portfelji)

@bottle.get("/moji-portfelji/<id_portfelja>")
def get_portfelj(id_portfelja):
    portfelj = najdi_portfelj(id_portfelja)
    return bottle.template("portfelj", portfelj=portfelj)

def najdi_portfelj(id_portfelja):
    '''TODO'''
    transakcija1 = {
                "id" : 1,
                "kriptovaluta" : "Bitcoin",
                "kratica" : "BTC",
                "cena" : 105.20,
                "kolicina" : 0.002,
                "datum" : "13. 5. 2024",
                "vrednost": 113.69,
                "donos" : 8.49,
                "trend" : 0.19
            }
    transakcija2 = {
                "id" : 2,
                "kriptovaluta" : "Jakacoin",
                "kratica" : "JKC",
                "cena" : 95.20,
                "kolicina" : 4.20,
                "datum" : "11. 9. 2001",
                "vrednost": 153.69,
                "donos" : 59.57,
                "trend" : 1.03
            }
    portfelj1 = {
        "ime" : "kripto:)",
        "transakcije" : [transakcija1, transakcija2, transakcija1, transakcija2, transakcija1, transakcija2, transakcija1, transakcija2, transakcija1, transakcija2, transakcija1, transakcija2, transakcija1]
    }
    return portfelj1

bottle.run(debug=True, reloader=True)