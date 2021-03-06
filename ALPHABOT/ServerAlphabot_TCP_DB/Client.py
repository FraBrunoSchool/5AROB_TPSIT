import re
import socket as sck
import time
import Classi.Config as conf
from Classi.AlphaBot import AlphaBot
from Classi.Log import Log


# 0.0,B50R90F600L90F400
# B 50  R 90    F 600   L 90    F 400
# [(b, 50), ]s


def client():
    c = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  # instantiate
    c.connect((conf.SERVER_IP, conf.SERVER_PORT))
    address = c.getsockname()
    ip = ""
    for i in address[0].split("."): ip += str(i)
    ip += "_" + str(address[1])
    log = Log(f"{conf.PATH_LOG}log_Client_{ip}.txt")
    log.i("Creazione Server")
    log.i("connect")

    log.i("Enter 'exit' to end the connection")
    msg = input("->")  # take input
    alphabot = AlphaBot()
    while True:
        try:
            c.sendall(msg.encode())  # send message
        except:
            log.e(f"failed")

        data = c.recv(conf.BUFFER_SIZE).decode()  # receive response
        log.i(f"Received from server: {data}")  # show response

        data = (data.split(","))[1]
        lista_potenze = re.split('B|R|F|L', data)
        lista_potenze.pop(0)
        regex = ''
        for index, el in enumerate(lista_potenze):
            if index == len(lista_potenze) - 1:
                regex += el
            else:
                regex += el + '|'
        lista_direzioni = re.split(regex, data)
        lista_direzioni.pop(-1)
        comandi = []
        for index, el in enumerate(lista_potenze): comandi.append((lista_direzioni[index], int(el)))
        print(comandi)
        for el in comandi:
            log.i(f"{el[0]} di {el[1]}")
            istruction(alphabot, el[0])
            time.sleep(el[1])
        alphabot.stop()

        msg = input("->")  # again take input

        if msg == "exit":
            c.sendall(msg.encode())  # send message
            log.w("Close the connection")
            break

    c.close()  # close the connection


def istruction(alphabot, command):
    switcher = {
        "F": alphabot.forward,
        "B": alphabot.backward,
        "R": alphabot.right,
        "L": alphabot.left
    }
    switcher[command]()


if __name__ == '__main__':
    client()
