import time
from datetime import datetime
import schedule

from Data.modeli import CenaKriptovalute
from Data.database import Repo
from Data.api import Api


def posodobi_cene():
    print(f"\n\n{datetime.now()} Začenjam posodobitev cen.")
    repo = Repo()
    api = Api()
    kriptovalute = repo.dobi_kriptovalute()
    print(f"{datetime.now()} Pobral id-je kriptovalut iz baze.")
    ids = [kripto.id for kripto in kriptovalute]
    kriptovalute, cas = api.dobi_cene_kriptovalut(ids)
    print(f"{datetime.now()} Dobil podatke preko API-ja.")
    for i, id in enumerate(ids):
        kripto = kriptovalute[i]
        # try:
        cenaKriptovalute = CenaKriptovalute(
            kriptovaluta = id,
            cas = cas,
            cena = kripto.zadnja_cena
        )
        repo.posodobi_ceno_kriptovalute(id, kripto.zadnja_cena, kripto.trend24h, kripto.trend7d)
        repo.dodaj_ceno_kriptovalute(cenaKriptovalute)
        if (i + 1) % 100 != 0:
            print(f"{datetime.now()} Posodobil {i + 1} / {len(kriptovalute)}", end="\r")
        else:
            print(f"{datetime.now()} Posodobil {i + 1} / {len(kriptovalute)}", end="\n")
        # except:
        #     passN

    print(f"{datetime.now()} Končano posodabljanje cen.\n\n")
    print("=====================================================")


def test_task():
    print(f"{datetime.now()} Klicana testna funkcija")


schedule.every().hour.at(":00").do(posodobi_cene)


while True:
    schedule.run_pending()
    time.sleep(1)


    