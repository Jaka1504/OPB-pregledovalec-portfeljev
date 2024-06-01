from Data.database import Repo
from Data.modeli import *
from Data.api import Api

class KriptovaluteService:
    def __init__(self):
        self.repo = Repo()
        self.api = Api()

    def dodaj_zacetne_kriptovalute(self):
        '''
        V bazo doda prvih 2000 kriptovalut po tržni kapitalizaciji.
        '''
        kriptovalute = self.api.dobi_kriptovalute()
        for kripto in kriptovalute:
            self.repo.dodaj_kriptovaluto(kripto)


    def posodobi_ceno(self, kratica):
        """
        Posodobi ceno kriptovalute s kratico kratica iz tabele Kriptovaluta na zadnjo znano ceno, če taka kriptovaluta obstaja.
        """
        try:
            kriptovaluta = self.repo.dobi_kriptovaluto_po_kratici(kratica)
            kripto = self.api.dobi_cene_kriptovalut([kriptovaluta.id])[0][0]
            self.repo.posodobi_ceno_kriptovalute(kriptovaluta.id, kripto.zadnja_cena, kripto.trend24h, kripto.trend7d)
        except:
            raise Exception("Kratica ne obstaja.")

    def dobi_kriptovaluto(self, id):
        """Vrne objekt Kriptovaluta() iz Data.modeli, v katerem so shranjeni podatki o kriptovaluti z id-jem id."""
        kriptovaluta = self.repo.dobi_kriptovaluto(id)
        return kriptovaluta