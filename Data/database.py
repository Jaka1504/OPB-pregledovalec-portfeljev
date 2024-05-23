import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

from Data.modeli import *
import Data.auth_public as auth



DB_PORT = 5432

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

    def dodaj_kriptovaluto(self, kriptovaluta : Kriptovaluta):
        cmd = """
            INSERT into kriptovaluta(id, kratica, ime, zadnja_cena)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """
        data = (kriptovaluta.id, kriptovaluta.kratica,  kriptovaluta.ime, kriptovaluta.zadnja_cena)
        self.cur.execute(cmd, data)
        self.conn.commit()

    def dodaj_transakcijo(self, transakcija : Transakcija):
        cmd = """
            INSERT into transakcija(kolicina, cas, portfelj, kriptovaluta)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """
        data = (transakcija.kolicina, transakcija.cas, transakcija.portfelj, transakcija.kriptovaluta)
        self.cur.execute(cmd, data)
        transakcija.id = self.cur.fetchone()[0]
        self.conn.commit()

    def dobi_uporabnike(self):
        cmd = """
            SELECT uporabnisko_ime, geslo, ime, priimek from uporabnik
            """
        self.cur.execute(cmd)
        uporabniki = [Uporabnik.from_dict(u) for u in self.cur.fetchall()]
        return uporabniki

    def dobi_uporabnika(self, uporabnisko_ime):
        cmd = f"""
            SELECT uporabnisko_ime, geslo, ime, priimek from uporabnik
            WHERE uporabnisko_ime = '{uporabnisko_ime}'
            """
        self.cur.execute(cmd)
        uporabnik = Uporabnik.from_dict(self.cur.fetchone())
        return uporabnik

    def dobi_uporabnikove_portfelje(self, uporabnisko_ime):
        cmd = f"""
            SELECT id, ime, lastnik from portfelj 
            WHERE lastnik = '{uporabnisko_ime}'
            """
        self.cur.execute(cmd)
        portfelji = [Portfelj.from_dict(p) for p in self.cur.fetchall()]
        return portfelji

    def dobi_portfelj(self, id):
        cmd = f"""
            SELECT id, ime, lastnik from portfelj
            WHERE id = {id}
            """
        self.cur.execute(cmd)
        portfelj = Portfelj.from_dict(self.cur.fetchone())
        return portfelj
    
    def dobi_transakcijo(self, id):
        cmd = f"""
            SELECT id, kolicina, cas, portfelj, kriptovaluta from transakcija
            WHERE id = {id}
            """
        self.cur.execute(cmd)
        transakcija = Transakcija.from_dict(self.cur.fetchone())

    def dobi_transakcije_v_portfelju(self, id, kriptovaluta=None):
        cmd = f"""
            SELECT id, kolicina, cas, portfelj, kriptovaluta from transakcija
            WHERE portfelj = {id} 
            """
        if kriptovaluta is not None:
            cmd += f"""
                AND kriptovaluta = {kriptovaluta}    
                """
        self.cur.execute(cmd)
        transakcije = [Transakcija.from_dict(t) for t in self.cur.fetchall()]
        return transakcije

    def dobi_uporabnikove_transakcije(self, uporabnisko_ime, kriptovaluta=None):
        cmd = f"""
            SELECT t.id, t.kolicina, t.cas, t.portfelj, t.kriptovaluta 
            from transakcija t
            JOIN portfelj ON t.portfelj = portfelj.id
            JOIN uporabnik ON lastnik = uporabnik.uporabnisko_ime 
            WHERE lastnik = '{uporabnisko_ime}'
            """
        if kriptovaluta is not None:
            cmd += f"""
                AND kriptovaluta = {kriptovaluta}    
                """
        self.cur.execute(cmd)
        transakcije = [Transakcija.from_dict(t) for t in self.cur.fetchall()]
        return transakcije

    def dobi_kriptovaluto(self, id):
        cmd = f"""
            SELECT id, kratica, ime, zadnja_cena from kriptovaluta
            WHERE id = {id}
            """
        self.cur.execute(cmd)
        kriptovaluta = Kriptovaluta.from_dict(self.cur.fetchone())
        return kriptovaluta
    
    def dobi_kriptovaluto_po_kratici(self, kratica):
        cmd = f"""
            SELECT id, kratica, ime, zadnja_cena from kriptovaluta
            WHERE kratica = {kratica}
            """
        self.cur.execute(cmd)
        kriptovaluta = Kriptovaluta.from_dict(self.cur.fetchone())
        return kriptovaluta

    def dobi_kriptovalute(self):
        cmd = f"""
            SELECT id, kratica, tip, ime, zadnja_cena from kriptovaluta
            """
        self.cur.execute(cmd)
        kriptovalute = [Kriptovaluta.from_dict(s) for s in self.cur.fetchall()]
        return kriptovalute

    def dobi_kolicino_kriptovalut_v_portfelju(self, id):
        cmd = f"""
            SELECT kriptovaluta, sum(t.kolicina)
            FROM transakcija t
            JOIN portfelj p ON t.portfelj = p.id
            GROUP BY kriptovaluta, p.id
            HAVING p.id = {id}
            """
        self.cur.execute(cmd)
        kolicine = dict(self.cur.fetchall())
        return kolicine

    def posodobi_ceno_kriptovalute(self, id, cena):
        cmd = f"""
            UPDATE kriptovaluta
            SET zadnja_cena = {cena}
            WHERE id = {id}
            """
        self.cur.execute(cmd)
        self.conn.commit()