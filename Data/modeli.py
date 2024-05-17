from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime

@dataclass_json
@dataclass
class Uporabnik:
    uporabnisko_ime : str = field(default="")
    geslo : str = field(default="")
    ime : str = field(default="")
    priimek : str = field(default="")

@dataclass_json
@dataclass
class Portfelj:
    id : int = field(default=0)
    lastnik : str = field(default="")
    ime : str = field(default="")

@dataclass_json
@dataclass
class Sredstvo:
    id : int = field(default=0)
    kratica : str = field(default="")
    tip : str = field(default="")
    ime : str = field(default="")
    zadnja_cena : float = field(default=0.)

@dataclass_json
@dataclass
class Transakcija:
    id : int = field(default=0)
    kolicina : float = field(default=0.)
    vrednost : float = field(default=0.)
    cas : datetime = field(default=datetime.now())
    sredstvo : int = field(default=0)
    portfelj : int = field(default=0)

@dataclass_json
@dataclass
class ZgodovinaCen:
    sredstvo : int = field(default=0)
    cas : datetime = field(default=datetime.now())
    cena : float = field(default=0.)