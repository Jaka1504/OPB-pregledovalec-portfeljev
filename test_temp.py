from Data.database import Repo
import plotly.express as px
import pandas as pd
import datetime as dt

from Services.kriptovalute_service import KriptovaluteService

repo = Repo()
k_service = KriptovaluteService()

graf = k_service.ustvari_graf_zgodovine_cen(90)

print(graf[:100])


