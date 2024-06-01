import requests
import time
from datetime import datetime
from Data.modeli import *

class Api:
    def __init__(self):
        self.base_url = "https://api.coinlore.net/api/"
        self.tformat = '%Y-%m-%d %H:%M:%S'

    def dobi_kriptovalute(self):
        '''
        Vrne seznam trenutnih prvih 2000 kriptovalut po tržni kapitalizaciji.
        '''
        kriptovalute = []
        cas = datetime.now()
        for i in range(20):
            print(f"Dobljenih prvih {(i+1) * 100} kriptovalut.")
            url = self.base_url + f"tickers/?start={i * 100}&limit=100"
            r = requests.get(url)
            data = r.json()
            kriptovalute += [Kriptovaluta.from_dict({
                'id': int(d['id']),
                'kratica': d['symbol'],
                'ime': d['name'],
                'zadnja_cena': float(d['price_usd']),
                'trend24h' : float(d['percent_change_24h']),
                'trend7d' : float(d['percent_change_7d'])
                }) for d in data['data']]
            time.sleep(1)
        return kriptovalute

    def dobi_cene_kriptovalut(self, ids : list):
        '''
        Vrne trenutne cene kriptovalut, katerih id-ji so v seznamu ids, in čas poizvedbe.
        '''
        cas = datetime.now().strftime(self.tformat)
        if not ids:
            return ([], cas)
        ids_string = ",".join(str(id) for id in ids)
        url = self.base_url + f"ticker/?id={ids_string}"
        r = requests.get(url)
        data = r.json()
        kriptovalute = [Kriptovaluta.from_dict({
                'id': int(d['id']),
                'kratica': d['symbol'],
                'ime': d['name'],
                'zadnja_cena': float(d['price_usd']),
                'trend24h' : float(d['percent_change_24h']),
                'trend7d' : float(d['percent_change_7d'])
                }) for d in data]
        return (kriptovalute, cas)
        
