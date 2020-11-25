import logging
import socket as sck
from Classi.ClientThread import ClientThread
import Classi.Config as conf


def server():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  # get instance
    s.bind((conf.SERVER_IP, conf.SERVER_PORT))  # bind host address and port
    s.listen()  # number of client can listen simultaneously

    countClient = 1
    client_thread = []
    client_address = []
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info("Server in ascolto")
    while True:
        conn, address = s.accept()  # accept new connection
        logging.info(f"New connection from: {address}")
        cl = ClientThread(conn, address, f"{conf.PATH_DATA}/operations.db", countClient)
        cl.start()
        client_thread.append(cl)
        client_address.append(address)
        countClient += 1

    print("chiudo i thread")
    for t in client_thread:
        t.join()


if __name__ == '__main__':
    server()
