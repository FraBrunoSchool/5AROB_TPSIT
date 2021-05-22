# -------------------
# Badoino Matteo
# Bernardi Gianluca
# Bruno Francesco
# -------------------

import time
import requests


def main():
    s = requests.Session()
    URL = "http://127.0.0.1:5000/server/inizializzazione"
    PARAMS = {'msg': 'start'}
    r = s.get(url=URL, params=PARAMS)
    print(f"Inizializzazione fatta, sono {r.text}")
    # ------------------------------------------------
    while True:
        URL = "http://127.0.0.1:5000/server/richiesta"
        PARAMS = {'msg': 'richiesta'}
        r = s.get(url=URL, params=PARAMS)
        operazione = (r.json())[0]['operazione']
        print(f"Operazione {operazione}")
        if operazione == 'end':
            break
        URL = "http://127.0.0.1:5000/server/risultato"
        PARAMS = {'risultato': eval(operazione)}
        r = s.get(url=URL, params=PARAMS)
        print(r.text)



if __name__ == '__main__':
    main()
