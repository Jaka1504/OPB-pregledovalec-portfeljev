import bottle
from Services.auth_service import AuthService
from Services.portfelj_service import PortfeljService
from Services.kriptovalute_service import KriptovaluteService
from Services.transakcije_service import TransakcijeService


# Da bottle najde template v pravi mapi
import os
base_path = os.path.abspath(os.path.dirname(__file__))
views_path = os.path.join(base_path, 'UserInterface', 'views')
bottle.TEMPLATE_PATH.insert(0, views_path)

SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)


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


@bottle.get("")
@bottle.get("/")
def get_index():
    auth = AuthService()
    uporabnisko_ime = poisci_uporabnisko_ime()
    if uporabnisko_ime:
        uporabnik = auth.dobi_uporabnika(uporabnisko_ime)
        ime = uporabnik.ime
    else:
        ime = ""
    return bottle.template(
        "index",
        uporabnisko_ime=uporabnisko_ime,
        ime = ime
    )


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
    uporabnisko_ime=poisci_uporabnisko_ime()
    portfelj = najdi_portfelj(id_portfelja)
    if portfelj.lastnik != uporabnisko_ime:
        return bottle.redirect("/napacen-uporabnik/")
    else:
        graf = p_service.ustvari_graf_zgodovine_vrednosti(id_portfelja)
        return bottle.template(
            "portfelj",
            portfelj=portfelj,
            graf=graf,
            uporabnisko_ime=uporabnisko_ime)


@bottle.get("/prijava/")
def get_prijava():
    return bottle.template(
        "prijava",
        napaka=None,
        uporabnisko_ime=poisci_uporabnisko_ime(),
    )


@bottle.post("/prijava/")
def post_prijava():
    auth = AuthService()
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo = auth.zasifriraj_geslo(bottle.request.forms.getunicode("geslo"))
    napaka = None
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
    auth = AuthService()
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


@bottle.get("/odjava/")
def get_odjava():
    odjavi_uporabnika()
    return bottle.redirect("/prijava/")


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
    vlozek = float(bottle.request.forms.getunicode("vlozek"))
    uporabnisko_ime = poisci_uporabnisko_ime()
    napaka = None
    imena_portfeljev=[portfelj.ime for portfelj in p_service.najdi_vse_portfelje(uporabnisko_ime=uporabnisko_ime)]
    if ime_portfelja in imena_portfeljev:
        napaka = "Na tem uporabniškem računu že obstaja portfelj s tem imenom. Prosim, izberite drugo ime."
        return bottle.template(
            "nov-portfelj", napaka=napaka, uporabnisko_ime=poisci_uporabnisko_ime()
        )
    else:
        nov_portfelj = p_service.ustvari_portfelj(uporabnisko_ime=uporabnisko_ime, ime_portfelja=ime_portfelja)
        p_service.dodaj_vlozek(nov_portfelj.id, vlozek)
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
    napaka = t_service.naredi_transakcijo(id_kriptovalute=kriptovaluta, id_portfelja=portfelj, kolicina=kolicina)
    if napaka is None:
        return bottle.redirect(f"/kriptovaluta/{portfelj}/{kriptovaluta}/")
    else:
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


@bottle.get("/dodaj-denar/")
def get_dodaj_denar():
    uporabnisko_ime=poisci_uporabnisko_ime()
    portfelji = p_service.najdi_vse_portfelje(uporabnisko_ime)
    return bottle.template(
        "dodaj-denar",
        napaka=None,
        portfelji=portfelji,
        uporabnisko_ime=uporabnisko_ime,
    )


@bottle.post("/dodaj-denar/")
def post_dodaj_denar():
    portfelj = int(bottle.request.forms.getunicode("portfelj"))
    kolicina = float(bottle.request.forms.getunicode("kolicina"))
    p_service.dodaj_vlozek(portfelj, kolicina)
    return bottle.redirect(f"/portfelj/{portfelj}/")


@bottle.get("/kriptovaluta/<id_portfelja>/<id_kriptovalute>/")
def get_kriptovaluta(id_portfelja, id_kriptovalute):
    uporabnisko_ime=poisci_uporabnisko_ime()
    portfelj = najdi_portfelj(id_portfelja)
    if portfelj.lastnik != uporabnisko_ime:
        return bottle.redirect("/napacen-uporabnik/")
    else:
        kriptovaluta = najdi_kriptovaluto(id_portfelja, id_kriptovalute)
        graf = k_service.ustvari_graf_zgodovine_cen(id=id_kriptovalute)
        return bottle.template(
            "kriptovaluta",
            kriptovaluta=kriptovaluta,
            uporabnisko_ime=uporabnisko_ime,
            graf = graf
            )


@bottle.get("/kriptovalute/<id_kriptovalute>/")
def get_kriptovalute(id_kriptovalute):
    uporabnisko_ime = poisci_uporabnisko_ime()
    vse_kriptovalute = k_service.dobi_kriptovalute()
    kriptovaluta = dobi_kriptovaluto(id_kriptovalute)
    graf = k_service.ustvari_graf_zgodovine_cen(id=id_kriptovalute)
    return bottle.template(
        "kriptovalute",
        graf=graf,
        vse_kriptovalute=vse_kriptovalute,
        kriptovaluta=kriptovaluta,
        uporabnisko_ime=uporabnisko_ime,
    )

@bottle.post("/najdi-kripto/")
def post_nova_transakcija():
    id_kriptovalute = int(bottle.request.forms.getunicode("kriptovaluta"))
    return bottle.redirect(f"/kriptovalute/{id_kriptovalute}/")


@bottle.get("/napacen-uporabnik/")
def get_napacen_uporabnik():
    uporabnisko_ime = poisci_uporabnisko_ime()
    return bottle.template(
        "napacen-uporabnik",
        uporabnisko_ime=uporabnisko_ime
    )


#####################################################################################################

def najdi_portfelj(id_portfelja):
    """Vrne podatke o portfelju."""
    portfelj = p_service.najdi_portfelj(id_portfelja=id_portfelja)
    kriptovalute = dict()
    for id_kripto, kolicina in portfelj.kriptovalute.items():
        if kolicina > 0:
            kriptovaluta = k_service.dobi_kriptovaluto(id_kripto)
            kriptovalute[id_kripto] = {
                "id" : id_kripto,
                "ime" : kriptovaluta.ime,
                "kratica" : kriptovaluta.kratica,
                "kolicina" : kolicina,
                "vrednost" : kolicina * kriptovaluta.zadnja_cena,
                "trend24h" : kriptovaluta.trend24h,
                "trend7d" : kriptovaluta.trend7d
            }
    portfelj.kriptovalute = kriptovalute
    return portfelj


def najdi_kriptovaluto(id_portfelja, id_kriptovalute):
    "Vrne podatke o kriptovaluti iz portfelja."
    k_service.posodobi_ceno(id_kriptovalute)
    portfelj = p_service.najdi_portfelj(id_portfelja)
    kripto = k_service.dobi_kriptovaluto(id_kriptovalute)
    transakcije = t_service.dobi_transakcije_v_portfelju(id_portfelja, id_kriptovalute)
    kriptovaluta = {
        "ime": kripto.ime,
        "kratica": kripto.kratica,
        "portfelj": portfelj,
        "vrednost_enote": kripto.zadnja_cena,
        "trend24h": kripto.trend24h,
        "trend7d": kripto.trend7d,
        "transakcije": transakcije
    }
    return kriptovaluta

def dobi_kriptovaluto(id_kriptovalute):
    """Vrne podatke o kriptovaluti."""
    k_service.posodobi_ceno(id_kriptovalute)
    kripto = k_service.dobi_kriptovaluto(id_kriptovalute)
    kriptovaluta = {
        "ime": kripto.ime,
        "kratica": kripto.kratica,
        "vrednost_enote": kripto.zadnja_cena,
        "trend24h": kripto.trend24h,
        "trend7d": kripto.trend7d,
    }
    return kriptovaluta


def poisci_uporabnisko_ime():
    """Poišče in vrne vrednost piškotka `uporabnisko_ime`."""
    return bottle.request.get_cookie(key="uporabnisko_ime", secret=SKRIVNOST)


def odjavi_uporabnika():
    """Izbriše piškotek `uporabniško_ime`."""
    bottle.response.delete_cookie("uporabnisko_ime", path="/")

# if __name__ == "__main__":
#     bottle.run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)

bottle.run(host="localhost", port=SERVER_PORT, reloader=RELOADER)