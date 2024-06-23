import UserInterface.bottle as bottle
from Services.auth_service import AuthService
from Services.portfelj_service import PortfeljService
from Services.kriptovalute_service import KriptovaluteService
from Services.transakcije_service import TransakcijeService


# Da bottle najde template v pravi mapi
import os
base_path = os.path.abspath(os.path.dirname(__file__))
views_path = os.path.join(base_path, 'UserInterface', 'views')
bottle.TEMPLATE_PATH.insert(0, views_path)


auth = AuthService()
p_service = PortfeljService()
k_service = KriptovaluteService()
t_service = TransakcijeService()


SKRIVNOST = "njrelnfkonmakdnenfonmklernmkondakwndwanfo"


@bottle.get("/static/<ime_datoteke:path>")
def static(ime_datoteke):
    return bottle.static_file(ime_datoteke, root="UserInterface/views")


@bottle.get("/img/<ime_datoteke:path>")
def img(ime_datoteke):
    return bottle.static_file(ime_datoteke, root="UserInterface/img")


@bottle.get("/")
def get_index():
    return bottle.template("index", uporabnisko_ime=poisci_uporabnisko_ime())


@bottle.get("/moji-portfelji/")
def get_moji_portfelji():
    '''TODO'''
    uporabnisko_ime = poisci_uporabnisko_ime()
    if not uporabnisko_ime:
        bottle.redirect("/prijava/")
    else:
        portfelji = p_service.najdi_vse_portfelje(uporabnisko_ime)
        return bottle.template("moji-portfelji", portfelji=portfelji, uporabnisko_ime=poisci_uporabnisko_ime())


@bottle.get("/portfelj/<id_portfelja>/")
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
    

@bottle.get("/profil/")
def get_profil():
    uporabnisko_ime = poisci_uporabnisko_ime()
    return bottle.template("profil", uporabnisko_ime=uporabnisko_ime, napaka=None)


@bottle.post("/odjava/")
def post_odjava():
    odjavi_uporabnika()
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


@bottle.get("/nova-transakcija/")
def get_nova_transakcija():
    uporabnisko_ime=poisci_uporabnisko_ime()
    vse_kriptovalute=k_service.dobi_kriptovalute()
    portfelji = p_service.najdi_vse_portfelje(uporabnisko_ime)
    return bottle.template(
        "nova-transakcija",
        napaka=None,
        vse_kriptovalute=vse_kriptovalute,
        portfelji=portfelji,
        uporabnisko_ime=uporabnisko_ime,
    )


@bottle.post("/nova-transakcija/")
def post_nova_transakcija():
    portfelj = int(bottle.request.forms.getunicode("portfelj"))
    kriptovaluta = int(bottle.request.forms.getunicode("kriptovaluta"))
    kolicina = float(bottle.request.forms.getunicode("kolicina"))
    try:
        t_service.naredi_transakcijo(id_kriptovalute=kriptovaluta, id_portfelja=portfelj, kolicina=kolicina)
        bottle.redirect(f"/kriptovaluta/{portfelj}/{kriptovaluta}/")
    except Exception:
        if kolicina > 0:        # kupujemo => ni dovolj denarja
            napaka = "Na tem portfelju ni dovolj denarja. Povišajte vložek ali izberite drugo količino kriptovalute."
        else:                   # prodajamo => ni dovolj kriptovalute
            napaka = "Na tem portfelju ni dovolj enot izbrane kriptovalute."
        uporabnisko_ime=poisci_uporabnisko_ime()
        vse_kriptovalute=k_service.dobi_kriptovalute()
        portfelji = p_service.najdi_vse_portfelje(uporabnisko_ime)
        return bottle.template(
            "nova-transakcija",
            napaka=napaka,
            vse_kriptovalute=vse_kriptovalute,
            portfelji=portfelji,
            uporabnisko_ime=uporabnisko_ime,
        )


@bottle.get("/kriptovaluta/<id_portfelja>/<id_kriptovalute>/")
def get_kriptovaluta(id_portfelja, id_kriptovalute):
    kriptovaluta = najdi_kriptovaluto(id_portfelja, id_kriptovalute)
    # kriptovaluta = logic.najdi_kriptovaluto(id_portfelja, id_kriptovalute)
    graf = k_service.ustvari_graf_zgodovine_cen(id=id_kriptovalute)
    return bottle.template(
        "kriptovaluta",
        kriptovaluta=kriptovaluta,
        uporabnisko_ime=poisci_uporabnisko_ime(),
        graf = graf
        )

#####################################################################################################

def najdi_portfelj(id_portfelja):
    '''TODO'''
    portfelj = p_service.najdi_portfelj(id_portfelja=id_portfelja)
    for id_kripto, kolicina in portfelj.kriptovalute.items():
        kriptovaluta = k_service.dobi_kriptovaluto(id_kripto)
        portfelj.kriptovalute[id_kripto] = {
            "id" : id_kripto,
            "ime" : kriptovaluta.ime,
            "kratica" : kriptovaluta.kratica,
            "kolicina" : kolicina,
            "vrednost" : kolicina * kriptovaluta.zadnja_cena,
            "trend24h" : kriptovaluta.trend24h,                     # WIP
            "trend7d" : kriptovaluta.trend7d
        }
    return portfelj

def najdi_kriptovaluto(id_portfelja, id_kriptovalute):
    '''TODO'''
    portfelj = p_service.najdi_portfelj(id_portfelja)
    kripto = k_service.dobi_kriptovaluto(id_kriptovalute)
    transakcije = t_service.dobi_transakcije_v_portfelju(id_portfelja, id_kriptovalute)
    kriptovaluta = {
        "ime": kripto.ime,
        "kratica": kripto.kratica,
        "ime_portfelja": portfelj.ime,
        "vrednost_enote": kripto.zadnja_cena,
        "trend24h": kripto.trend24h,
        "trend7d": kripto.trend7d,
        "transakcije": transakcije
    }

    # transakcija1 = {
    #             "id" : 1,
    #             "cena_enote" : 20105.20,
    #             "kolicina" : 0.002,
    #             "datum" : "13. 5. 2024",
    #         }
    # transakcija2 = {
    #             "id" : 2,
    #             "cena_enote" : 19595.20,
    #             "kolicina" : 0.00420,
    #             "datum" : "11. 9. 2001",
    #         }
    # kriptovaluta = {
    #     "ime": "Bitcoin",
    #     "kratica": "BTC",
    #     "ime_portfelja": "kripto:)",
    #     "vrednost_enote": 18697.65,
    #     "trend": 0.64,
    #     "transakcije": [
    #         transakcija1,
    #         transakcija2,
    #         transakcija1,
    #         transakcija2,
    #         transakcija1,
    #         transakcija2,
    #         transakcija1,
    #         transakcija2,
    #         transakcija1,
    #         transakcija2,
    #         transakcija1,
    #         transakcija2,
    #         transakcija1,
    #         transakcija2,
    #         transakcija1,
    #         transakcija2
    #     ]
    # }
    return kriptovaluta


def poisci_uporabnisko_ime():
    """Poišče in vrne vrednost piškotka `uporabnisko_ime`."""
    return bottle.request.get_cookie(key="uporabnisko_ime", secret=SKRIVNOST)


def odjavi_uporabnika():
    """Izbriše piškotek `uporabniško_ime`."""
    bottle.response.delete_cookie("uporabnisko_ime", path="/")


bottle.run(debug=True, reloader=True)