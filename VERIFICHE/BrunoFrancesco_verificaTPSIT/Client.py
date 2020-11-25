import socket as sck
import Classi.Config as conf
from Classi.Log import Log


def client():
    c = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  # instantiate
    c.connect((conf.SERVER_IP, conf.SERVER_PORT))
    address = c.getsockname()
    ip = ""
    for i in address[0].split("."): ip += str(i)
    ip += "_" + str(address[1])
    log = Log(f"{conf.PATH_LOG}log_Client_{ip}.txt")
    # creo istanza socket
    log.i("creo istanza")


    print(c.getsockname())
    msg = "start"  # take input

    while True:
        # mando il risultato, al primo giro è start
        c.sendall(msg.encode())  # send message

        data = c.recv(conf.BUFFER_SIZE).decode()  # receive response
        log.i(f"Received from server: {data}")  # show response

        # se il server mi manda exit perchè non ci sono più operazioni chiudo
        if data == "exit":
            c.sendall("exit".encode())  # send message
            log.i("Close the connection")
            break

        # controllo se è possibile fare eval
        try:
            msg = str(eval(data))  # again take input
            log.i(f"Risultato di {data} = {msg}")
        except:
            # mando error se non va
            msg = "error"
            log.e(f"{data} = ERROR from {conf.SERVER_IP} - {conf.SERVER_PORT}")

    c.close()  # close the connection


if __name__ == '__main__':
    client()
