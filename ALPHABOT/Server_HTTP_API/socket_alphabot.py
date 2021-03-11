import re
import requests


# from AlphaBot import AlphaBot


def main():
    while True:
        start = input("Inserisci punto di partenza")
        end = input("Inserisci il punto di arrivo")
        URL = "http://192.168.0.30:5000/api/v1/resources/path"
        PARAMS = {'end': end, 'start': start}
        r = requests.get(url=URL, params=PARAMS)
        percorso= r.json()
        percorso = percorso[0]['percorso']

        if percorso not in ("Tra le due località inserite non esiste un percorso", "Località non valide"):
            comandi = split_istruzioni(percorso)
            print(comandi)
        else:
            print(percorso)

        """for el in comandi:
            print(f"{el[0]} di {el[1]}")
            istruction(alphabot, el[0])
            time.sleep(el[1])
            alphabot.stop()"""


def split_istruzioni(percorso):
    lista_potenze = re.split('B|R|F|L', percorso)
    # print(lista_potenze)
    lista_potenze.pop(0)
    regex = ''
    for index, el in enumerate(lista_potenze):
        if index == len(lista_potenze) - 1:
            regex += el
        else:
            regex += el + '|'
    lista_direzioni = re.split(regex, percorso)
    lista_direzioni.pop(-1)
    comandi = []
    for index, el in enumerate(lista_potenze): comandi.append((lista_direzioni[index], int(el)))
    return comandi


def istruction(alphabot, command):
    switcher = {
        "F": alphabot.forward,
        "B": alphabot.backward,
        "R": alphabot.right,
        "L": alphabot.left
    }
    switcher[command]()


if __name__ == '__main__':
    main()
