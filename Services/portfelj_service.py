from Data.database import Repo
from Data.modeli import *
from Data.api import Api


class PortfeljService():
    def __init__(self):
        self.repo = Repo()
        self.api = Api()

    def posodobi_portfelje(self, ids : list):
        '''Dobi trenutne cene kriptovalut v portfeljih z id-ji v seznamu ids, jim posodobi cene, izračuna vrednost 
        portfeljev ter jih vrne in vstavi ustrezne podatke v tabeli VrednostPortfelja in CenaKriptovalute.'''
        portfelji = [self.repo.dobi_portfelj(id) for id in ids]
        seznam_kolicin = [self.repo.dobi_kolicino_kriptovalut_v_portfelju(id) for id in ids]
        seznam_kriptovalut = list(set(sum([list(d.keys()) for d in seznam_kolicin], [])))
        kriptovalute, cas = self.api.dobi_cene_kriptovalut(seznam_kriptovalut)
        vrednosti = [0 for _ in portfelji]
        for kripto in kriptovalute:
            kolicine = [kolicine_dict.get(kripto.id, 0) for kolicine_dict in seznam_kolicin]
            cena = kripto.zadnja_cena
            for i, kolicina in enumerate(kolicine):
                vrednosti[i] += kolicina * cena
            
            cenaKriptovalute = CenaKriptovalute(
                kriptovaluta = kripto.id,
                cas = cas,
                cena = kripto.zadnja_cena
            )
            self.repo.posodobi_ceno_kriptovalute(kripto.id, kripto.zadnja_cena)
            self.repo.dodaj_ceno_kriptovalute(cenaKriptovalute)

        vrednostiPortfeljev = [VrednostPortfelja(
            portfelj = portfelj.id,
            cas = cas,
            vrednost = round(vrednosti[i], 2)
        ) for i, portfelj in enumerate(portfelji)]
        for vp in vrednostiPortfeljev:
            self.repo.dodaj_vrednost_porfelja(vp)

        return [PortfeljDto(
            id = portfelj.id,
            lastnik = portfelj.lastnik,
            ime = portfelj.ime,
            vrednost = round(vrednosti[i], 2)
        ) for i, portfelj in enumerate(portfelji)]


    def najdi_vse_portfelje(self, uporabnisko_ime):
        '''Vrne seznam portfeljev uporabnika. Vsak portfelj je slovar oblike
        portfelj = {
            "id" : 1,
            "ime" : "kripto:)",
            "cena" : 2.13,              # vsota cen vseh transakcij tega portfelja, koliko je uporabnik plačal
            "vrednost" : 103.14,        # vsota (trenutna vrednost enote * kolicina) za vse transakcije
            "donos" : 101.01,           # razlika prejsnjih dveh
            "trend" : 0.4               # za koliko procentov se je povecala vrednost, če pogledamo zadnja dva (razlicna?) vnosa
        }'''
        portfelji = self.repo.dobi_uporabnikove_portfelje(uporabnisko_ime)
        ids = [p.id for p in portfelji]
        portfeljiDto = self.posodobi_portfelje(ids)
        return portfeljiDto


    def najdi_portfelj(self, id_portfelja):
        '''Vrne portfelj z ustreznim ID-jem. Portfelj naj bo slovar oblike 
        portfelj = {
            "id" : 1,
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
        ids = [id_portfelja]
        portfeljDto = self.posodobi_portfelje(ids)[0]
        return portfeljDto


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
        pass
