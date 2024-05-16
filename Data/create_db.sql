CREATE TABLE Uporabnik(
    uporabnisko_ime TEXT PRIMARY KEY,
    ime TEXT NOT NULL,
    priimek TEXT NOT NULL,
    geslo TEXT NOT NULL 
);

CREATE TABLE Portfelj(
    id SERIAL PRIMARY KEY,
    ime TEXT NOT NULL,
    lastnik TEXT NOT NULL REFERENCES Uporabnik(uporabnisko_ime)
);

CREATE TABLE Sredstvo(
    id SERIAL PRIMARY KEY,
    kratica TEXT NOT NULL,
    tip TEXT NOT NULL,
    ime TEXT NOT NULL,
    zadnja_cena FLOAT NOT NULL
);

CREATE TABLE Transakcija(
    id SERIAL PRIMARY KEY,
    kolicina FLOAT NOT NULL,
    vrednost FLOAT NOT NULL,
    cas TIMESTAMP NOT NULL,
    portfelj INTEGER NOT NULL REFERENCES Portfelj(id),
    sredstvo INTEGER NOT NULL REFERENCES Sredstvo(id)
);

CREATE TABLE ZgodovinaCen(
    sredstvo INTEGER NOT NULL REFERENCES Sredstvo(id),
    cas TIMESTAMP NOT NULL,
    cena FLOAT NOT NULL
);