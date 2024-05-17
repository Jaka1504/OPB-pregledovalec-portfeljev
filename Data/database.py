import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

from Data.modeli import *
import Data.auth_public as auth



DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

class Repo:
    def __init__(self): 
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def dodaj_uporabinka(self, uporabnik : Uporabnik):
        cmd = """
            INSERT into uporabnik(uporabnisko_ime, ime, priimek, geslo)
            VALUES (%s, %s, %s, %s) 
            """
        data = (uporabnik.uporabnisko_ime, uporabnik.ime, uporabnik.priimek, uporabnik.geslo)
        self.cur.execute(cmd, data)
        self.conn.commit()

    def dodaj_portfelj(self, portfelj : Portfelj):
        cmd = """
            INSERT into portfelj(ime, lastnik)
            VALUES (%s, %s)
            RETURNING id
            """
        data = (portfelj.ime, portfelj.lastnik)
        self.cur.execute(cmd, data)
        portfelj.id = self.cur.fetchone()[0]
        self.conn.commit()

    def dodaj_sredstvo(self, sredstvo : Sredstvo):
        cmd = """
            INSERT into sredstvo(kratica, tip, ime, zadnja_cena)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """
        data = (sredstvo.kratica, sredstvo.tip, sredstvo.ime, sredstvo.zadnja_cena)
        self.cur.execute(cmd, data)
        sredstvo.id = self.cur.fetchone()[0]
        self.conn.commit()

    def dodaj_transakcijo(self, transakcija : Transakcija):
        cmd = """
            INSERT into transakcija(kolicina, vrednost, cas, portfelj, sredstvo)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """
        data = (transakcija.kolicina, transakcija.vrednost, transakcija.cas, transakcija.portfelj, transakcija.sredstvo)
        self.cur.execute(cmd, data)
        transakcija.id = self.cur.fetchone()[0]
        self.conn.commit()