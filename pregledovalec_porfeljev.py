import bottle
from Services.auth_service import AuthService
from Services.portfelj_service import PortfeljService

auth = AuthService()
p_service = PortfeljService()



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
    # portfelji = [portfelj1, portfelj2, portfelj1, portfelj2, portfelj1, portfelj2, portfelj1, portfelj2, portfelj1, portfelj2, portfelj1]
    portfelji = p_service.najdi_vse_portfelje(poisci_uporabnisko_ime())
    return bottle.template("moji-portfelji-reduciran", portfelji=portfelji, uporabnisko_ime=poisci_uporabnisko_ime())


@bottle.get("/moji-portfelji/<id_portfelja>")
def get_portfelj(id_portfelja):
    portfelj = najdi_portfelj(id_portfelja)
    # portfelj = logic.najdi_portfelj(id_portfelja)
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
    geslo = auth.zasifriraj_geslo(bottle.request.forms.getunicode("geslo"))
    napaka = None
    # TODO daj iz auth
    if uporabnisko_ime in auth.seznam_uporabniskih_imen():
        if auth.preveri_geslo(
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


@bottle.get("/nov-portfelj/")
def get_nov_portfelj():
    return bottle.template(
        "nov-portfelj",
        napaka=None,
        uporabnisko_ime=poisci_uporabnisko_ime(),
    )


@bottle.post("/nov-portfelj/")
def post_nov_portfelj():
    ime_portfelja = bottle.request.forms.getunicode("ime_portfelja")
    uporabnisko_ime = poisci_uporabnisko_ime()
    napaka = None
    imena_portfeljev=[portfelj.ime for portfelj in p_service.najdi_vse_portfelje(uporabnisko_ime=uporabnisko_ime)]
    if ime_portfelja in imena_portfeljev:
        napaka = "Na tem uporabniškem računu že obstaja portfelj s tem imenom. Prosim, izberite drugo ime."
        return bottle.template(
            "nov-portfelj", napaka=napaka, uporabnisko_ime=poisci_uporabnisko_ime()
        )
    else:
        p_service.ustvari_portfelj(uporabnisko_ime=uporabnisko_ime, ime_portfelja=ime_portfelja)
        return bottle.redirect("/moji-portfelji/")


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
    ime = bottle.request.forms.getunicode("ime")
    priimek = bottle.request.forms.getunicode("priimek")
    zasifrirano_geslo = auth.zasifriraj_geslo(bottle.request.forms.getunicode("geslo"))
    napaka = None
    if uporabnisko_ime in auth.seznam_uporabniskih_imen():
        napaka = "To uporabniško ime je že zasedeno. Prosim, izberi drugačno ime."
        return bottle.template(
            "registracija", napaka=napaka, uporabnisko_ime=poisci_uporabnisko_ime()
        )
    else:
        auth.dodaj_uporabnika(uporabnisko_ime=uporabnisko_ime, zasifrirano_geslo=zasifrirano_geslo, ime=ime, priimek=priimek)
        bottle.response.set_cookie(
            name="uporabnisko_ime", value=uporabnisko_ime, secret=SKRIVNOST, path="/"
        )
        return bottle.redirect("/")


@bottle.get("/kriptovaluta/<id_portfelja>/<id_kriptovalute>")
def get_kriptovaluta(id_portfelja, id_kriptovalute):
    kriptovaluta = najdi_kriptovaluto(id_portfelja, id_kriptovalute)
    # kriptovaluta = logic.najdi_kriptovaluto(id_portfelja, id_kriptovalute)
    return bottle.template(
        "kriptovaluta",
        kriptovaluta=kriptovaluta,
        uporabnisko_ime=poisci_uporabnisko_ime()
        )

#####################################################################################################

def najdi_portfelj(id_portfelja):
    '''TODO'''
    kriptovaluta1 = {
                "id" : 1,
                "ime" : "Bitcoin",
                "kratica" : "BTC",
                "cena" : 105.20,
                "kolicina" : 0.002,
                "vrednost": 113.69,
                "donos" : 8.49,
                "trend" : 0.19
            }
    kriptovaluta2 = {
                "id" : 2,
                "ime" : "Jakacoin",
                "kratica" : "JKC",
                "cena" : 95.20,
                "kolicina" : 4.20,
                "vrednost": 153.69,
                "donos" : 59.57,
                "trend" : 1.03
            }
    portfelj1 = {
        "id" : 1,
        "ime" : "kripto:)",
        "kriptovalute" : [kriptovaluta1, kriptovaluta2, kriptovaluta1, kriptovaluta2, kriptovaluta1, kriptovaluta2, kriptovaluta1, kriptovaluta2, kriptovaluta1, kriptovaluta2, kriptovaluta1, kriptovaluta2, kriptovaluta1]
    }
    return portfelj1

def najdi_kriptovaluto(id_portfelja, id_kriptovalute):
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
        "ime_portfelja": "kripto:)",
        "vrednost_enote": 18697.65,
        "trend": 0.64,
        "transakcije": [
            transakcija1,
            transakcija2,
            transakcija1,
            transakcija2,
            transakcija1,
            transakcija2,
            transakcija1,
            transakcija2,
            transakcija1,
            transakcija2,
            transakcija1,
            transakcija2,
            transakcija1,
            transakcija2,
            transakcija1,
            transakcija2
        ]
    }
    return kriptovaluta


def poisci_uporabnisko_ime():
    """Poišče in vrne vrednost piškotka `uporabnisko_ime`."""
    return bottle.request.get_cookie(key="uporabnisko_ime", secret=SKRIVNOST)


bottle.run(debug=True, reloader=True)