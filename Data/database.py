import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

from modeli import *
import auth_public as auth



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
            SELECT id, kolicina, vrednost, cas, portfelj, sredstvo from transakcija
            WHERE id = {id}
            """
        self.cur.execute(cmd)
        transakcija = Transakcija.from_dict(self.cur.fetchone())

    def dobi_transakcije_v_portfelju(self, id, sredstvo=None):
        cmd = f"""
            SELECT id, kolicina, vrednost, cas, portfelj, sredstvo from transakcija
            WHERE portfelj = {id} 
            """
        if sredstvo is not None:
            cmd += f"""
                AND sredstvo = {sredstvo}    
                """
        self.cur.execute(cmd)
        transakcije = [Transakcija.from_dict(t) for t in self.cur.fetchall()]
        return transakcije

    def dobi_uporabnikove_transakcije(self, uporabnisko_ime, sredstvo=None):
        cmd = f"""
            SELECT t.id, t.kolicina, t.vrednost, t.cas, t.portfelj, t.sredstvo 
            from transakcija t
            JOIN portfelj ON t.portfelj = portfelj.id
            JOIN uporabnik ON lastnik = uporabnik.uporabnisko_ime 
            WHERE lastnik = '{uporabnisko_ime}'
            """
        if sredstvo is not None:
            cmd += f"""
                AND sredstvo = {sredstvo}    
                """
        self.cur.execute(cmd)
        transakcije = [Transakcija.from_dict(t) for t in self.cur.fetchall()]
        return transakcije

    def dobi_sredstvo(self, id):
        cmd = f"""
            SELECT id, kratica, tip, ime, zadnja_cena from sredstvo
            WHERE id = {id}
            """
        self.cur.execute(cmd)
        sredstvo = Sredstvo.from_dict(self.cur.fetchone())
        return sredstvo

    def dobi_sredstva(self):
        cmd = f"""
            SELECT id, kratica, tip, ime, zadnja_cena from sredstvo
            """
        self.cur.execute(cmd)
        sredstva = [Sredstvo.from_dict(s) for s in self.cur.fetchall()]
        return sredstva

    def dobi_kolicino_sredstev_v_portfelju(self, id):
        cmd = f"""
            SELECT sredstvo, sum(t.kolicina)
            FROM transakcija t
            JOIN portfelj p ON t.portfelj = p.id
            GROUP BY sredstvo, p.id
            HAVING p.id = {id}
            """
        self.cur.execute(cmd)
        kolicine = dict(self.cur.fetchall())
        return kolicine

    def posodobi_ceno_sredstva(self, id, cena):
        cmd = f"""
            UPDATE sredstvo
            SET zadnja_cena = {cena}
            WHERE id = {id}
            """
        self.cur.execute(cmd)
        self.conn.commit()