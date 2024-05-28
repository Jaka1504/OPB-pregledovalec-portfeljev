from Data.database import Repo
from Data.modeli import *
from Data.api import Api
from datetime import datetime

class TransakcijeService():
    def __init__(self):
        self.repo = Repo()
        self.api = Api()

    def naredi_transakcijo(self, id_kriptovalute, id_portfelja, kolicina):
        """Doda transakcijo v bazo, posodobi ceno kriptovalute s katero poteka transakcija in doda ceno v 
        tabelo CenaKriptovalute, če to lahko naredi, tj. če gre za prodajo (kolicina < 0), mora biti v 
        portfelju dovolj kriptovalute."""
        kolicine = self.repo.dobi_kolicino_kriptovalut_v_portfelju(id_portfelja)
        if kolicina + kolicine.get(id_kriptovalute, 0) < 0:
            raise Exception("V portfelju ni dovolj kriptovalute za prodajo!")
        seznam, cas = self.api.dobi_cene_kriptovalut([id_kriptovalute])
        kriptovaluta = seznam[0]
        self.repo.posodobi_ceno_kriptovalute(id_kriptovalute, kriptovaluta.zadnja_cena)

        transakcija = Transakcija(
            kriptovaluta=id_kriptovalute,
            portfelj=id_portfelja,
            kolicina=kolicina,
            cas=cas
        )
        self.repo.dodaj_transakcijo(transakcija)

        ck = CenaKriptovalute(
            cas=cas,
            kriptovaluta=id_kriptovalute,
            cena=kriptovaluta.zadnja_cena
        )
        self.repo.dodaj_ceno_kriptovalute(ck)
        return transakcija

    def dobi_transakcije_v_portfelju(self, id_portfelja, id_kripto=None):
        """Če je id_kripto=None, vrne seznam vseh transakcij v portfelju z id-jem id portfelja, sicer vrne 
        le transakcije s kriptovaluto z id-jem id_kripto Transakcije so objekti TransakcijaDto() iz Data.modeli. """
        transakcije = self.repo.dobi_transakcije_v_portfeljuDTO(id_portfelja)
        return transakcije

    def dobi_uporabnikove_transakcije(self, uporabnisko_ime, id_kripto=None):
        """Če je id_kripto=None, vrne seznam vseh transakcij uporabnika z uporabniškim imenom 
        uporabnisko_ime, sicer vrne le transakcije s kriptovaluto z id-jem id_kripto. Transakcije
        so objekti TransakcijaDto() it Data.modeli."""
        transakcije = self.repo.dobi_uporabnikove_transakcijeDTO(uporabnisko_ime)
        return transakcije
