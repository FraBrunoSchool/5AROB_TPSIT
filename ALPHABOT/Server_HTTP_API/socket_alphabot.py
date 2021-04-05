import re
import threading
from datetime import datetime
import static.Config as c
import requests
import RPi.GPIO as GPIO
import time
from static.AlphaBot import AlphaBot

alphabot = AlphaBot()
alphabot.stop()
COMANDO_SENSORI = c.STATO_RISORSA_STOP


def main():
    esec_path = threading.Thread(target=esecuzione_percorso)
    ril_ost = threading.Thread(target=rilevazione_ostacoli)
    """mutex_path = threading.Lock()
    mutex_ost = threading.Lock()
    mutex_ost.acquire()"""
    esec_path.start()
    ril_ost.start()
    esec_path.join()
    esec_path.join()
    alphabot.stop()


def rilevazione_ostacoli():
    global COMANDO_SENSORI
    DR = 16
    DL = 19

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(DR, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(DL, GPIO.IN, GPIO.PUD_UP)

    stato_prec = c.STATO_INIZIALE
    while True:
        # print(stato_prec)
        DR_status = GPIO.input(DR)
        DL_status = GPIO.input(DL)
        # print(f"DR_status: {DR_status} - DL_status: {DL_status}")
        if DL_status == 1 and DR_status == 1 and stato_prec != c.STATO_LIBERO:
            # tutto libero
            stato_prec = c.STATO_LIBERO
            COMANDO_SENSORI = c.STATO_RISORSA_AVANTI
            # print("Cambio: Davanti libero")
            invio_reports(stato_prec)
        if DL_status == 0 and DR_status == 0 and stato_prec != c.STATO_OCCUPATO:
            # ostacolo davanti
            stato_prec = c.STATO_OCCUPATO
            COMANDO_SENSORI = c.STATO_RISORSA_VAI_DX
            # print("Cambio: Davanti occupato")
            invio_reports(stato_prec)
        if DL_status == 1 and DR_status == 0 and stato_prec != c.STATO_LIBERO_SX:
            # ostacolo davanti
            stato_prec = c.STATO_LIBERO_SX
            COMANDO_SENSORI = c.STATO_RISORSA_VAI_SX
            # print("Cambio: sx_libero")
            invio_reports(stato_prec)
        if DL_status == 0 and DR_status == 1 and stato_prec != c.STATO_LIBERO_DX:
            # ostacolo davanti
            stato_prec = c.STATO_LIBERO_DX
            COMANDO_SENSORI = c.STATO_RISORSA_VAI_DX
            # print("Cambio: dx_libero")
            invio_reports(stato_prec)
        time.sleep(1)


def invio_reports(stato):
    URL = f"http://{c.WEB_SERVER_IP}:{c.WEB_SERVER_PORT}{c.WEB_SERVER_ROUTE_REPORTS}"
    PARAMS = {'date': f'{datetime.now()}', 'pos': f'{stato}'}
    r = requests.get(url=URL, params=PARAMS)


def esecuzione_percorso():
    global COMANDO_SENSORI
    while True:
        start = input("Inserisci punto di partenza")
        end = input("Inserisci il punto di arrivo")
        URL = f"http://{c.WEB_SERVER_IP}:{c.WEB_SERVER_PORT}{c.WEB_SERVER_ROUTE_PATH}"
        PARAMS = {'end': end, 'start': start}
        r = requests.get(url=URL, params=PARAMS)
        percorso = r.json()
        percorso = percorso[0]['percorso']

        if percorso not in ("Tra le due località inserite non esiste un percorso", "Località non valide"):
            comandi = split_istruzioni(percorso)
            print(comandi)
            for el in comandi:
                print(f"{el[0]} di {el[1]}")
                for t in range(el[1]):
                    istruction(alphabot, el[0])
                    time.sleep(1)
                    if COMANDO_SENSORI == c.STATO_RISORSA_VAI_DX:
                        istruction(alphabot, "R")
                        time.sleep(1)
                    elif COMANDO_SENSORI == c.STATO_RISORSA_VAI_SX:
                        istruction(alphabot, "L")
                        time.sleep(1)
                alphabot.stop()
        else:
            print(percorso)


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
