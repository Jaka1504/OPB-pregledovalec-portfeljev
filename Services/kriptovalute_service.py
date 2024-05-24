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
            cena = self.api.dobi_cene_kriptovalut([kriptovaluta.id])[0][0].zadnja_cena
            self.repo.posodobi_ceno_kriptovalute(kriptovaluta.id, cena)
        except:
            raise Exception("Kratica ne obstaja.")
