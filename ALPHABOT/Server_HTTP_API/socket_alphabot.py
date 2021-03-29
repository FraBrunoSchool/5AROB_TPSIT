import re
import threading
from datetime import datetime

import requests
import RPi.GPIO as GPIO
import time


from static.AlphaBot import AlphaBot
alphabot = AlphaBot()
alphabot.stop()

def main():
    esec_path = threading.Thread(target=esecuzione_percorso)
    ril_ost = threading.Thread(target=rilevazione_ostacoli)
    esec_path.start()
    ril_ost.start()
    esec_path.join()
    esec_path.join()

def rilevazione_ostacoli():
    DR = 16
    DL = 19

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(DR, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(DL, GPIO.IN, GPIO.PUD_UP)

    stato_prec = "stop"
    while True:
        #print(stato_prec)
        DR_status = GPIO.input(DR)
        DL_status = GPIO.input(DL)
        #print(f"DR_status: {DR_status} - DL_status: {DL_status}")
        if DL_status == 1 and DR_status == 1 and stato_prec != "libero":
            # tutto libero
            stato_prec = "libero"
            #print("Cambio: Davanti libero")
            invio_reports(stato_prec)
        if DL_status == 0 and DR_status == 0 and stato_prec != "occupato":
            # ostacolo davanti
            stato_prec = "occupato"
            #print("Cambio: Davanti occupato")
            invio_reports(stato_prec)
        if DL_status == 1 and DR_status == 0 and stato_prec != "sx_libero":
            # ostacolo davanti
            stato_prec = "sx_libero"
            #print("Cambio: sx_libero")
            invio_reports(stato_prec)
        if DL_status == 0 and DR_status == 1 and stato_prec != "dx_libero":
            # ostacolo davanti
            stato_prec = "dx_libero"
            #print("Cambio: dx_libero")
            invio_reports(stato_prec)
        time.sleep(1)


def invio_reports(stato):
    URL = "http://192.168.0.30:5000/api/v1/reports"
    PARAMS = {'date': f'{datetime.now()}', 'pos': f'{stato}'}
    r = requests.get(url=URL, params=PARAMS)

def esecuzione_percorso():
    while True:
        start = input("Inserisci punto di partenza")
        end = input("Inserisci il punto di arrivo")
        URL = "http://192.168.0.30:5000/api/v1/resources/path"
        PARAMS = {'end': end, 'start': start}
        r = requests.get(url=URL, params=PARAMS)
        percorso = r.json()
        percorso = percorso[0]['percorso']

        if percorso not in ("Tra le due località inserite non esiste un percorso", "Località non valide"):
            comandi = split_istruzioni(percorso)
            print(comandi)
        else:
            print(percorso)

        for el in comandi:
            print(f"{el[0]} di {el[1]}")
            istruction(alphabot, el[0])
            time.sleep(el[1])
            alphabot.stop()


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
