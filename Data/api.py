import requests
import time
from datetime import datetime
from modeli import *

class Api:
    def __init__(self):
        self.base_url = "https://api.coinlore.net/api/"
        self.tformat = '%Y-%m-%d %H:%M:%S'

    def dobi_kriptovalute(self):
        '''
        Vrne seznam trenutnih prvih 2000 kriptovalut po tržni kapitalizaciji.
        '''
        kriptovalute = []
        cas = datetime.datetime.now()
        for i in range(20):
            url = self.base_url + f"tickers/?start={i * 100}?limit=100"
            r = requests.get(url)
            data = r.json()
            kriptovalute += [Kriptovaluta.from_dict({
                'id': int(d['id']),
                'kratica': d['symbol'],
                'ime': d['name'],
                'zadnja_cena': float(d['price_usd'])
                }) for d in data['data']]
            time.sleep(1)
        return kriptovalute

    def dobi_cene_kriptovalut(self, ids : list(int)):
        '''
        Vrne trenutne cene kriptovalut, katerih id-ji so v seznamu ids, in čas poizvedbe.
        '''
        cas = datetime.now().strftime(self.tformat)
        ids_string = ",".join(str(id) for id in ids)
        url = self.base_url + f"ticker/?id={ids_string}"
        r = requests.get(url)
        data = r.json()
        kriptovalute = [Kriptovaluta.from_dict({
                'id': int(d['id']),
                'kratica': d['symbol'],
                'ime': d['name'],
                'zadnja_cena': float(d['price_usd'])
                }) for d in data]
        return [kriptovalute, cas]
        
