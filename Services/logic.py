# V tej datoteki so pomožne funkcije, ki iz baze pridobijo podatke, ki jih zahteva spletni vmesnik

from hashlib import sha256

# =================== Podatki o portfeljih =======================

def najdi_vse_portfelje(uporabnisko_ime):
    '''Vrne seznam portfeljev uporabnika. Vsak portfelj je slovar oblike
    portfelj = {
        "id" : 1,
        "ime" : "kripto:)",
        "cena" : 2.13,              # vsota cen vseh transakcij tega portfelja, koliko je uporabnik plačal
        "vrednost" : 103.14,        # vsota (trenutna vrednost enote * kolicina) za vse transakcije
        "donos" : 101.01,           # razlika prejsnjih dveh
        "trend" : 0.4               # za koliko procentov se je povecala vrednost, če pogledamo zadnja dva (razlicna?) vnosa
    }'''
    pass


def najdi_portfelj(id_portfelja):
    '''Vrne portfelj z ustreznim ID-jem. Portfelj naj bo slovar oblike 
    portfelj = {
        "ime" : "kripto:)",
        "kriptovalute" : [kriptovaluta1, kriptovaluta2]
    Kriptovalute naj bodo slovarji oblike
    kriptovaluta1 = {
        "id" : 1,
        "ime" : "Bitcoin",
        "kratica" : "BTC",
        "cena" : 105.20,            # vsota cen vseh transakcij pri tem portfelju s to kriptovaluto
        "kolicina" : 0.002,         # vsota kolicin vseh transakcij pri tem portfelju s to kriptovaluto
        "vrednost": 113.69,         # trenutna vrednost enote * kolicina
        "donos" : 8.49,             # vrednost - cena
        "trend" : 0.19              # za koliko procentov se je povecala vrednost, če pogledamo zadnja dva (razlicna?) vnosa
    }'''
    pass


def najdi_kriptovaluto(id_portfelja, id_kriptovalute):
    '''Vrne naslednje podatke za dano kriptovaluto v danem portfelju v obliki slovarja:
    kriptovaluta = {
        "ime": "Bitcoin",
        "kratica": "BTC",
        "ime_portfelja": "kripto:)",
        "vrednost_enote": 18697.65,         # trenutna vrednost enote kriptovalute
        "trend": 0.64,                      # za koliko procentov se je povecala vrednost, če pogledamo zadnja dva (razlicna?) vnosa
        "transakcije": [                    # seznam transakcij v tem portfelju s to kriptovaluto.
            transakcija1,
            transakcija2
            ]
        }
    kjer so transakcije slovarji oblike:
    transakcija1 = {
        "id" : 1,
        "cena_enote" : 20105.20,            # Takratna cena ene enote
        "kolicina" : 0.002,
        "datum" : "13. 5. 2024",
        }
    '''

# ========================== Funkcije za prijavo in registracijo =============================


def seznam_uporabniskih_imen():
    '''Vrne seznam vseh uporabniskih imen v bazi. (Ne rabi bit nujno seznam zarad mene, sam da je nek iterable)'''
    pass


def preveri_geslo(uporabnisko_ime, zasifrirano_geslo):
    '''Vrne True ce obstaja uporabnik s tem imenom in je njegovo geslo v bazi enako
    podanemu geslu (v bazo bi shranjevala samo zašifrirana gesla)'''
    pass


def zasifriraj_geslo(geslo_raw):
    '''Vrne zakodiran niz z algoritmom SHA256 - za shranjevanje gesel v nerazpoznavni obliki.'''
    return sha256(geslo_raw.encode('UTF-8')).hexdigest()


def dodaj_uporabnika(uporabnisko_ime, zasifrirano_geslo):
    '''Doda uporabnika v bazo podatkov'''