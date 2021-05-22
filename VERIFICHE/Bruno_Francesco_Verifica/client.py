from datetime import datetime
import requests


def main():
    # eseguo un while true per il menù in modo che me lo mostra sempre
    while True:
        # elenco le opzioni
        print("Scegli l'opzione: \n"
              "\t0. Esci\n"
              "\t1. grandezza_id\n"
              "\t2. stazione_id\n"
              "\t3. inserimento\n"
              "\t4. valori min avg e max\n")
        # input per far scegliere l'opzione
        option = input("Inserisci l'opzione: ")
        # se è 0 esco dal ciclo
        if option == '0': break
        # avvio il mio switch e stampo il suo return
        print(switch(option))


# funzione switch che è l'equivalente dello switch case in c
def switch(option):
    # dizionario con le opzioni
    switcher = {
        # dopo i due punti ci sono  le mie funzioni che ho creato
        "1": grandezza_id,
        "2": stazione_id,
        "3": inserimento,
        "4": valori
    }
    # avvio la funzione dentro lo switch
    return switcher[option]()


def grandezza_id():
    # url a cui devo fare la get
    URL = 'http://127.0.0.1:5000/api/v1/resources/grandezza/id'
    nome_grandezza = input("Inserisci il nome della grandezza: ")
    # qui salvo in un dizionario i parametri che devo passare al server api
    PARAMS = {'nome_grandezza': nome_grandezza}
    # eseguo la get
    r = requests.get(url=URL, params=PARAMS)
    # raccolgo il risultato
    # .json per mettere sotto forma di json la stringa che mi arriva
    # [...] per selezionare il campo del json/dizionario che mi serve
    id = (r.json())['id_misurazione']
    return id


def stazione_id():
    # url a cui devo fare la get
    URL = 'http://127.0.0.1:5000/api/v1/resources/stazione/id'
    nome_stazione = input("Inserisci il nome della stazione: ")
    # qui salvo in un dizionario i parametri che devo passare al server api
    PARAMS = {'nome_stazione': nome_stazione}
    # eseguo la get
    r = requests.get(url=URL, params=PARAMS)
    # raccolgo il risultato
    # .json per mettere sotto forma di json la stringa che mi arriva
    # [...] per selezionare il campo del json/dizionario che mi serve
    id = (r.json())['id_stazione']
    return id


def inserimento():
    # eseguo due funzioni del menù per avere i due id in modo che non devo riscrivere tutto
    id_stazione = stazione_id()
    id_grandezza = grandezza_id()
    valore = input("Inserisci il valore della misurazione")
    # url a cui devo fare la get
    URL = 'http://127.0.0.1:5000/api/v1/resources/inserimento'
    # qui salvo in un dizionario i parametri che devo passare al server api
    PARAMS = {'valore': valore, 'id_grandezza': id_grandezza, 'id_stazione': id_stazione, 'data': datetime.now()}
    # eseguo la get
    r = requests.get(url=URL, params=PARAMS)
    # restituisco il risultato della richiesta get
    return (r.json())['inserimento']


def valori():
    # eseguo due funzioni del menù per avere i due id in modo che non devo riscrivere tutto
    id_stazione = stazione_id()
    id_grandezza = grandezza_id()
    # url a cui devo fare la get
    URL = 'http://127.0.0.1:5000/api/v1/resources/valori'
    # qui salvo in un dizionario i parametri che devo passare al server api
    PARAMS = {'id_grandezza': id_grandezza, 'id_stazione': id_stazione}
    # eseguo la get
    r = requests.get(url=URL, params=PARAMS)
    # restituisco il risultato della richiesta get
    return (r.json())['valori']



if __name__ == '__main__':
    main()
