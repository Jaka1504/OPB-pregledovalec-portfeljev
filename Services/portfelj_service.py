from Data.database import Repo
from Data.modeli import *

#TODO
class PortfeljService():
    def __init__():
        self.repo = Repo()

    def posodobi_portfelj(self, id):
        '''Dobi trenutne cene kriptovalut v portfelju z id-jem id, jim posodobi cene, izračuna vrednost 
        portfelja ter jo vrne in vstavi ustrezne podatke v tabeli VrednostPortfelja in CenaKriptovalute.'''
        pass

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
        return self.repo.dobi_uporabnikove_portfelje(uporabnisko_ime)


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
        return self.repo.dobi_portfelj(id_portfelja)


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
