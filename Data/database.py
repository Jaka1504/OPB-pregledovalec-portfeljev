import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

from Data.modeli import *
import Data.auth_public as auth



DB_PORT = 5432

class Repo:
    def __init__(self): 
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def dodaj_uporabnika(self, uporabnik : Uporabnik):
        """
        Doda uporabnika v tabelo Uporabnik.
        """
        cmd = """
            INSERT into uporabnik(uporabnisko_ime, ime, priimek, geslo)
            VALUES (%s, %s, %s, %s) 
            """
        data = (uporabnik.uporabnisko_ime, uporabnik.ime, uporabnik.priimek, uporabnik.geslo)
        self.cur.execute(cmd, data)
        self.conn.commit()

    def dodaj_portfelj(self, portfelj : Portfelj):
        """
        Doda portfelj v tabelo Portfelj.
        """
        cmd = """
            INSERT into portfelj(ime, lastnik, vlozek, gotovina)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """
        data = (portfelj.ime, portfelj.lastnik, portfelj.vlozek, portfelj.gotovina)
        self.cur.execute(cmd, data)
        portfelj.id = self.cur.fetchone()[0]
        self.conn.commit()

    def dodaj_kriptovaluto(self, kripto : Kriptovaluta):
        """
        Doda kriptovaluto v tabelo Kriptovaluta.
        """
        cmd = """
            INSERT into kriptovaluta(id, kratica, ime, zadnja_cena, trend24h, trend7d)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
        data = (kripto.id, kripto.kratica,  kripto.ime, kripto.zadnja_cena, kripto.trend24h, kripto.trend7d)
        self.cur.execute(cmd, data)
        self.conn.commit()

    def dodaj_transakcijo(self, transakcija : Transakcija):
        """
        Doda transakcijo v tabelo Transakcija.
        """
        cmd = """
            INSERT into transakcija(kolicina, cas, portfelj, kriptovaluta)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """
        data = (transakcija.kolicina, transakcija.cas, transakcija.portfelj, transakcija.kriptovaluta)
        self.cur.execute(cmd, data)
        transakcija.id = self.cur.fetchone()[0]
        self.conn.commit()

    def dobi_uporabnike(self):
        """
        Vrne seznam vseh uporabnikov iz tabele Uporabnik.
        """
        cmd = """
            SELECT uporabnisko_ime, geslo, ime, priimek from uporabnik
            """
        self.cur.execute(cmd)
        uporabniki = [Uporabnik.from_dict(u) for u in self.cur.fetchall()]
        return uporabniki

    def dobi_uporabnika(self, uporabnisko_ime):
        """
        Vrne uporabnika z uporabniškim imenov uporabnisko_ime iz tabele Uporabnik.
        """
        cmd = f"""
            SELECT uporabnisko_ime, geslo, ime, priimek from uporabnik
            WHERE uporabnisko_ime = '{uporabnisko_ime}'
            """
        self.cur.execute(cmd)
        uporabnik = Uporabnik.from_dict(self.cur.fetchone())
        return uporabnik

    def dobi_uporabnikove_portfelje(self, uporabnisko_ime):
        """
        Vrne seznam vseh portfeljev uporabnika z uporabniškim imenom uporabnisko_ime iz tabele Portfelj.
        """
        cmd = f"""
            SELECT id, ime, lastnik, vlozek, gotovina from portfelj 
            WHERE lastnik = '{uporabnisko_ime}'
            """
        self.cur.execute(cmd)
        portfelji = [Portfelj.from_dict(p) for p in self.cur.fetchall()]
        return portfelji

    def dobi_portfelj(self, id):
        """
        Vrne portfelj z id-jem id iz tabele Portfelj.
        """
        cmd = f"""
            SELECT id, ime, lastnik, vlozek, gotovina from portfelj
            WHERE id = {id}
            """
        self.cur.execute(cmd)
        portfelj = Portfelj.from_dict(self.cur.fetchone())
        return portfelj
    
    def dobi_transakcijo(self, id):
        """
        Vrne transakcijo z id-jem id iz tabele Transakcija.
        """
        cmd = f"""
            SELECT id, kolicina, cas, portfelj, kriptovaluta from transakcija
            WHERE id = {id}
            """
        self.cur.execute(cmd)
        transakcija = Transakcija.from_dict(self.cur.fetchone())

    def dobi_transakcije_v_portfelju(self, id, kriptovaluta=None):
        """
        Če je kriptovaluta=None, vrne seznam vseh transakcij v portfelju z id-jem id iz tabele Transakcija, 
        sicer vrne seznam vseh transakcij v portfelju z id-jem id in kriptovaluto kriptovaluta.
        """
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
        """
        Če je kriptovaluta=None, vrne seznam vseh transakcij uporabnika z uporabniškim imenom uporabnisko_ime iz tabele Transakcija, 
        sicer vrne seznam vseh transakcij uporabnika z uporabniškim imenom uporabnisko_ime in kriptovaluto kriptovaluta.
        """
        cmd = f"""
            SELECT t.id, t.kolicina, t.cas, t.portfelj, t.kriptovaluta 
            from transakcija t
            JOIN portfelj ON t.portfelj = portfelj.id
            JOIN uporabnik ON lastnik = uporabnik.uporabnisko_ime 
            WHERE lastnik = '{uporabnisko_ime}'
            """
        if kriptovaluta is not None:
            cmd += f"""
                AND t.kriptovaluta = {kriptovaluta}    
                """
        self.cur.execute(cmd)
        transakcije = [Transakcija.from_dict(t) for t in self.cur.fetchall()]
        return transakcije

    def dobi_transakcije_v_portfeljuDTO(self, id, kriptovaluta=None):
        """
        Če je kriptovaluta=None, vrne seznam vseh transakcij v portfelju z id-jem id iz tabele Transakcija, 
        sicer vrne seznam vseh transakcij v portfelju z id-jem id in kriptovaluto kriptovaluta.
        Transakcije so objekti TransakcijaDto() iz Data.modeli.
        """
        cmd = f"""
            SELECT t.id, t.kolicina, t.cas, t.portfelj, t.kriptovaluta, c.cena 
            from transakcija t
            JOIN cenakriptovalute c ON t.cas = c.cas AND t.kriptovaluta = c.kriptovaluta
            WHERE portfelj = {id} 
            """
        if kriptovaluta is not None:
            cmd += f"""
                AND t.kriptovaluta = {kriptovaluta}    
                """
        self.cur.execute(cmd)
        transakcije = [TransakcijaDto.from_dict(t) for t in self.cur.fetchall()]
        return transakcije

    def dobi_uporabnikove_transakcijeDTO(self, uporabnisko_ime, kriptovaluta=None):
        """
        Če je kriptovaluta=None, vrne seznam vseh transakcij uporabnika z uporabniškim imenom uporabnisko_ime iz tabele Transakcija, 
        sicer vrne seznam vseh transakcij uporabnika z uporabniškim imenom uporabnisko_ime in kriptovaluto kriptovaluta.
        Transakcije so objekti TransakcijaDto() iz Data.modeli.
        """
        cmd = f"""
            SELECT t.id, t.kolicina, t.cas, t.portfelj, t.kriptovaluta, c.cena 
            from transakcija t
            JOIN cenakriptovalute c ON t.cas = c.cas AND t.kriptovaluta = c.kriptovaluta
            JOIN portfelj ON t.portfelj = portfelj.id
            JOIN uporabnik ON lastnik = uporabnik.uporabnisko_ime 
            WHERE lastnik = '{uporabnisko_ime}'
            """
        if kriptovaluta is not None:
            cmd += f"""
                AND t.kriptovaluta = {kriptovaluta}    
                """
        self.cur.execute(cmd)
        transakcije = [TransakcijaDto.from_dict(t) for t in self.cur.fetchall()]
        return transakcije

    def dobi_kriptovaluto(self, id):
        """
        Vrne kriptovaluto z id-jem id iz tabele Kriptovaluta. 
        """
        cmd = f"""
            SELECT id, kratica, ime, zadnja_cena, trend24h, trend7d from kriptovaluta
            WHERE id = {id}
            """
        self.cur.execute(cmd)
        kriptovaluta = Kriptovaluta.from_dict(self.cur.fetchone())
        return kriptovaluta
    
    def dobi_kriptovaluto_po_kratici(self, kratica):
        """
        Vrne kriptovaluto s kratico kratica iz tabele Kriptovaluta.
        """
        cmd = f"""
            SELECT id, kratica, ime, zadnja_cena, trend24h, trend7d from kriptovaluta
            WHERE kratica = '{kratica}'
            """
        self.cur.execute(cmd)
        kriptovaluta = Kriptovaluta.from_dict(self.cur.fetchone())
        return kriptovaluta


    def dobi_kriptovalute(self):
        """
        Vrne seznam vseh kriptovalut iz tabele Kriptovaluta.
        """
        cmd = f"""
            SELECT id, kratica, ime, zadnja_cena, trend24h, trend7d from kriptovaluta
            """
        self.cur.execute(cmd)
        kriptovalute = [Kriptovaluta.from_dict(s) for s in self.cur.fetchall()]
        return kriptovalute

    def dobi_kolicino_kriptovalut_v_portfelju(self, id):
        """
        Vrne slovar, katerega ključi so id-ji kriptovalut v portfelju z id-jem id in vrednosti so količine le-teh kriptovalut.
        """
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

    def posodobi_ceno_kriptovalute(self, id, cena, trend24h, trend7d):
        """
        Kriptovaluti z id-jem id iz tabele Kriptovaluta v stolpec zadnja_cena vstavi vrednost cena.
        """
        cmd = f"""
            UPDATE kriptovaluta
            SET zadnja_cena = {cena}, trend24h = {trend24h}, trend7d = {trend7d}
            WHERE id = {id}
            """
        self.cur.execute(cmd)
        self.conn.commit()

    def dodaj_ceno_kriptovalute(self, ck : CenaKriptovalute):
        """
        Doda ceno kriptovalute ob določenem času v tabelo CenaKriptovalute.
        """
        cmd = """
            INSERT into cenakriptovalute(kriptovaluta, cas, cena)
            VALUES (%s, %s, %s)
            """
        data = (ck.kriptovaluta, ck.cas, ck.cena)
        self.cur.execute(cmd, data)
        self.conn.commit()

    def dodaj_vrednost_porfelja(self, vp : VrednostPortfelja):
        """
        Doda vrednost portfelja ob določenem času v tabelo VrednostPortfelja.
        """
        cmd = """
            INSERT into vrednostportfelja(portfelj, cas, vrednost)
            VALUES (%s, %s, %s)
            """
        data = (vp.portfelj, vp.cas, vp.vrednost)
        self.cur.execute(cmd, data)
        self.conn.commit()

    def dobi_zgodovino_cen_kriptovalute(self, id):
        """
        Vrne par seznamov časov in cen kriptovalute z danim id-jem.
        """
        cmd = """
            SELECT cas, cena
            FROM cenakriptovalute
            WHERE kriptovaluta = %s
            """
        data = (str(id), )
        self.cur.execute(cmd, data)
        casi = []
        cene = []
        for cas, cena in self.cur.fetchall():
            casi.append(datetime.strftime(cas, '%Y-%m-%d %H:%M:%S'))
            cene.append(cena)
        return (casi, cene)
    
    def dodaj_vlozek_portfelju(self, id, vlozek):
        """
        Posodobi, tj. prišteje, vložek vlozek portfelju z id-jem id.
        """
        portfelj = self.dobi_portfelj(id)
        cmd = f"""
            UPDATE portfelj
            SET vlozek = {vlozek + portfelj.vlozek}, gotovina = {vlozek + portfelj.gotovina}
            WHERE id = {id}
            """
        self.cur.execute(cmd)
        self.conn.commit()

    def posodobi_gotovino_v_portfelju(self, id, gotovina):
        """Posodobi, tj. prišteje oz. odšteje, gotovino iz portfelja z id-jem id."""
        portfelj = self.dobi_portfelj(id)
        cmd = f"""
            UPDATE portfelj
            SET gotovina = {gotovina + portfelj.gotovina}
            WHERE id = {id}
            """
        self.cur.execute(cmd)
        self.conn.commit()
