import time
from datetime import datetime
import schedule

from Data.modeli import CenaKriptovalute
from Data.database import Repo


def posodobi_cene():
    repo = Repo()
    kriptovalute = repo.dobi_kriptovalute()
    for i, kripto in enumerate(kriptovalute):
        try:
            cenaKriptovalute = CenaKriptovalute(
                kriptovaluta = kripto.id,
                cas = datetime.now(),
                cena = kripto.zadnja_cena
            )
            repo.posodobi_ceno_kriptovalute(kripto.id, kripto.zadnja_cena, kripto.trend24h, kripto.trend7d)
            repo.dodaj_ceno_kriptovalute(cenaKriptovalute)
            if (i + 1) % 100 != 0:
                print(f"{datetime.now()} Posodobil {i} / {len(kriptovalute)}", end="\r")
            else:
                print(f"{datetime.now()} Posodobil {i} / {len(kriptovalute)}", end="\n")
        except:
            pass

    print(f"{datetime.now()} Posodobil cene")


def test_task():
    print(f"{datetime.now()} Klicana testna funkcija")


schedule.every().hour.at(":00").do(posodobi_cene)


while True:
    schedule.run_pending()
    time.sleep(1)


    