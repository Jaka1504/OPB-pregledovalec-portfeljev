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

@dataclass
class PortfeljDto:
    id : int = field(default=0)
    lastnik : str = field(default="")
    ime : str = field(default="")
    vrednost : float = field(default="")
    kriptovalute : dict = field(default=dict())

@dataclass_json
@dataclass
class Kriptovaluta:
    id : int = field(default=0)
    kratica : str = field(default="")
    ime : str = field(default="")
    zadnja_cena : float = field(default=0.)

@dataclass_json
@dataclass
class Transakcija:
    id : int = field(default=0)
    kolicina : float = field(default=0.)
    cas : datetime = field(default=datetime.now())
    kriptovaluta : int = field(default=0)
    portfelj : int = field(default=0)

@dataclass_json
@dataclass
class CenaKriptovalute:
    kriptovaluta : int = field(default=0)
    cas : datetime = field(default=datetime.now())
    cena : float = field(default=0.)

@dataclass_json
@dataclass
class VrednostPortfelja:
    portfelj : int = field(default=0)
    cas : datetime = field(default=datetime.now())
    vrednost : float = field(default=0.)