from Data.database import Repo
from Data.modeli import *
from Data.api import Api

import plotly.express as px
from pandas import DataFrame

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
    
    
    def ustvari_graf_zgodovine_cen(self, id):
        """Vrne objekt, ki ga vstavimo v HTML datoteko, da prikaže graf zgodovine cene kriptovalute z danim id-jem"""
        casi, cene = self.repo.dobi_zgodovino_cen_kriptovalute(id)
        df = DataFrame({
            "cas": casi,
            "cena": cene
        })
        fig = px.line(df, x="cas", y="cena")
        fig.update_layout({
            "plot_bgcolor" : "rgba(0, 0, 0, 0)",
            "paper_bgcolor" : "rgba(0, 0, 0, 0)",
            "font_color" : "rgba(255, 255, 255, 1)",
            "height" : 300,
            "margin" : {
                "l" : 0,
                "r" : 0,
                "b" : 10,
                "t" : 10,
                "pad" : 0
            }
        })
        fig.update_traces(line_color="#00ff00", line_width=2)
        return fig.to_html(full_html=False)