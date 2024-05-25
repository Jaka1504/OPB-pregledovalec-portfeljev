from Data.database import Repo
from Data.modeli import *
from hashlib import sha256

class AuthService():
    def __init__(self):
        self.repo = Repo()

    def seznam_uporabniskih_imen(self):
        '''Vrne seznam vseh uporabniskih imen v bazi.'''
        uporabniki = self.repo.dobi_uporabnike()
        return [u.uporabnisko_ime for u in uporabniki]


    def preveri_geslo(self, uporabnisko_ime, zasifrirano_geslo):
        '''Vrne True če obstaja uporabnik s tem imenom in je njegovo geslo v bazi enako
        podanemu geslu, sicer vrne False.'''
        try:
            uporabnik = self.repo.dobi_uporabnika(uporabnisko_ime)
            if zasifrirano_geslo == uporabnik.geslo:
                return True
            else:
                return False
        except:
            return False


    def zasifriraj_geslo(geslo_raw):
        '''Vrne zakodiran niz z algoritmom SHA256 - za shranjevanje gesel v nerazpoznavni obliki.'''
        return sha256(geslo_raw.encode('UTF-8')).hexdigest()


    def dodaj_uporabnika(uporabnisko_ime, zasifrirano_geslo, ime, priimek):
        '''Doda uporabnika v bazo podatkov'''
        uporabnik = Uporabnik(
            uporabnisko_ime=uporabnisko_ime,
            geslo=zasifrirano_geslo,
            ime=ime,
            priimek=priimek
        )

        self.repo.dodaj_uporabnika(uporabnik)