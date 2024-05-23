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
        pass