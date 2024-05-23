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

CREATE TABLE Kriptovaluta(
    id INTEGER PRIMARY KEY,
    kratica TEXT NOT NULL,
    ime TEXT NOT NULL,
    zadnja_cena FLOAT NOT NULL
);

CREATE TABLE Transakcija(
    id SERIAL PRIMARY KEY,
    kolicina FLOAT NOT NULL,
    cas TIMESTAMP NOT NULL,
    portfelj INTEGER NOT NULL REFERENCES Portfelj(id),
    kriptovaluta INTEGER NOT NULL REFERENCES Kriptovaluta(id)
);

CREATE TABLE CenaKriptovalute(
    kriptovaluta INTEGER NOT NULL REFERENCES Kriptovaluta(id),
    cas TIMESTAMP NOT NULL,
    cena FLOAT NOT NULL
);

CREATE TABLE VrednostPorfelja(
    portfelj INTEGER NOT NULL REFERENCES Portfelj(id),
    cas TIMESTAMP NOT NULL,
    vrednost FLOAT NOT NULL
);