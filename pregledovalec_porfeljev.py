import bottle
from hashlib import sha256


SKRIVNOST = "njrelnfkonmakdnenfonmklernmkondakwndwanfo"


@bottle.get("/static/<ime_datoteke:path>")
def static(ime_datoteke):
    return bottle.static_file(ime_datoteke, root="views")


@bottle.get("/img/<ime_datoteke:path>")
def img(ime_datoteke):
    return bottle.static_file(ime_datoteke, root="img")


@bottle.get("/")
def get_index():
    return bottle.template("index", uporabnisko_ime=poisci_uporabnisko_ime())


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
    return bottle.template("moji-portfelji", portfelji=portfelji, uporabnisko_ime=poisci_uporabnisko_ime())


@bottle.get("/moji-portfelji/<id_portfelja>")
def get_portfelj(id_portfelja):
    portfelj = najdi_portfelj(id_portfelja)
    return bottle.template("portfelj", portfelj=portfelj, uporabnisko_ime=poisci_uporabnisko_ime())


@bottle.get("/prijava/")
def get_prijava():
    return bottle.template(
        "prijava",
        napaka=None,
        uporabnisko_ime=poisci_uporabnisko_ime(),
    )


@bottle.post("/prijava/")
def post_prijava():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo = zasifriraj_geslo(bottle.request.forms.getunicode("geslo"))
    napaka = None
    if uporabnisko_ime in slovar_uporabniskih_imen_in_gesel():
        if preveri_geslo(
            uporabnisko_ime=uporabnisko_ime, zasifrirano_geslo=geslo
        ):
            bottle.response.set_cookie(
                name="uporabnisko_ime",
                value=uporabnisko_ime,
                secret=SKRIVNOST,
                path="/",
            )
        else:
            napaka = "Uporabniško ime in geslo se ne ujemata!"
    else:
        napaka = "Ta uporabnik ne obstaja. Preveri črkovanje ali ustvari nov račun!"
    if napaka:
        return bottle.template(
            "prijava", napaka=napaka, uporabnisko_ime=poisci_uporabnisko_ime()
        )
    else:
        return bottle.redirect("/")


@bottle.get("/registracija/")
def get_registracija():
    return bottle.template(
        "registracija",
        napaka=None,
        uporabnisko_ime=poisci_uporabnisko_ime(),
    )


@bottle.post("/registracija/")
def post_registracija():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    zasifrirano_geslo = zasifriraj_geslo(bottle.request.forms.getunicode("geslo"))
    napaka = None
    if uporabnisko_ime in slovar_uporabniskih_imen_in_gesel().keys():
        napaka = "To uporabniško ime je že zasedeno. Prosim, izberi drugačno ime."
        return bottle.template(
            "registracija", napaka=napaka, uporabnisko_ime=poisci_uporabnisko_ime()
        )
    else:
        dodaj_uporabnika(uporabnisko_ime=uporabnisko_ime, zasifrirano_geslo=zasifrirano_geslo)
        bottle.response.set_cookie(
            name="uporabnisko_ime", value=uporabnisko_ime, secret=SKRIVNOST, path="/"
        )
        return bottle.redirect("/")


#####################################################################################################
# WIP

@bottle.get("/kriptovaluta/<id_kriptovalute>")
def get_kriptovaluta(id_kriptovalute):
    kriptovaluta = najdi_kriptovaluto(id_kriptovalute)
    return bottle.template(
        "kriptovaluta",
        kriptovaluta=kriptovaluta,
        uporabnisko_ime=poisci_uporabnisko_ime()
        )

#####################################################################################################

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

def najdi_kriptovaluto(id_kriptovalue):
    '''TODO'''
    transakcija1 = {
                "id" : 1,
                "cena_enote" : 20105.20,
                "kolicina" : 0.002,
                "datum" : "13. 5. 2024",
            }
    transakcija2 = {
                "id" : 2,
                "cena_enote" : 19595.20,
                "kolicina" : 0.00420,
                "datum" : "11. 9. 2001",
            }
    kriptovaluta = {
        "ime": "Bitcoin",
        "kratica": "BTC",
        "vrednost_enote": 18697.65,
        "trend": 0.64,
        "transakcije": [
            transakcija1,
            transakcija2
        ]
    }
    return kriptovaluta


def poisci_uporabnisko_ime():
    """Poišče in vrne vrednost piškotka `uporabnisko_ime`."""
    return bottle.request.get_cookie(key="uporabnisko_ime", secret=SKRIVNOST)


def zasifriraj_geslo(geslo_raw):
    '''TODO (prestavit v drug file eventually)'''
    return sha256(geslo_raw.encode('UTF-8')).hexdigest()


def slovar_uporabniskih_imen_in_gesel():
    '''TODO'''
    return {
        'Test_username': zasifriraj_geslo('Test_username'), 
        'Micka': zasifriraj_geslo('Micka'),
        'Francelj': zasifriraj_geslo('Francelj')
        }


def preveri_geslo(uporabnisko_ime, zasifrirano_geslo):
    '''TODO'''
    return slovar_uporabniskih_imen_in_gesel()[uporabnisko_ime] == zasifrirano_geslo


def dodaj_uporabnika(uporabnisko_ime, zasifrirano_geslo):
    '''TODO'''
    pass


bottle.run(debug=True, reloader=True)