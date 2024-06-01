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
            self.repo.posodobi_ceno_kriptovalute(kripto.id, kripto.zadnja_cena, kripto.trend24h, kripto.trend7d)
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
            vrednost = round(vrednosti[i], 2),
            kriptovalute = seznam_kolicin[i],
            vlozek = portfelj.vlozek,
            gotovina = portfelj.gotovina
        ) for i, portfelj in enumerate(portfelji)]


    def najdi_vse_portfelje(self, uporabnisko_ime):
        '''Vrne seznam portfeljev uporabnika. Vsak portfelj objekt PortfeljDto() iz Data.modeli z atributi
            id : 1,
            ime : "kripto:)",
            lastnik : "test",         # lastnik portfelja
            vrednost : 103.14,        # vsota (trenutna vrednost enote * kolicina) za vse transakcije
            kriptovalute : dict()     # slovar {id_kripto: kolicina_kripto}
            Da dobiš objekt Kriptovaluta() iz id_kripto glej Services.kriptovalute_service (dobi_kriptovaluto).
        '''
        portfelji = self.repo.dobi_uporabnikove_portfelje(uporabnisko_ime)
        ids = [p.id for p in portfelji]
        portfeljiDto = self.posodobi_portfelje(ids)
        return portfeljiDto


    def najdi_portfelj(self, id_portfelja):
        '''Vrne portfelj z id-jem id_portfelja. Portfelj je objekt PortfeljDto() iz Data.modeli z atributi
            id : 1,
            ime : "kripto:)",
            lastnik : "test",         # lastnik portfelja
            vrednost : 103.14,        # vsota (trenutna vrednost enote * kolicina) za vse transakcije
            kriptovalute : dict().     # slovar {id_kripto: kolicina_kripto}
            Da dobiš objekt Kriptovaluta() iz id_kripto glej Services.kriptovalute_service (dobi_kriptovaluto).
        '''
        ids = [id_portfelja]
        portfeljDto = self.posodobi_portfelje(ids)[0]
        return portfeljDto


    def ustvari_portfelj(self, uporabnisko_ime, ime_portfelja):
        portfelj = Portfelj(
            lastnik=uporabnisko_ime,
            ime=ime_portfelja,
            gotovina=0,
            vlozek=0
        )
        self.repo.dodaj_portfelj(portfelj)
        return portfelj

    def dodaj_vlozek(self, id_portfelja, vlozek):
        """Portfelju z id-jem portfelj doda vložek vlozek in vrne nov portfelj."""
        self.repo.dodaj_vlozek_portfelju(id_portfelja, vlozek)
        return self.repo.dobi_portfelj(id_portfelja)

