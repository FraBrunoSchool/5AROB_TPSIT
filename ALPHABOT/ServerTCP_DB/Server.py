import logging
import socket as sck
from ClientThread import ClientThread


def server():
    # get the hostname
    host = "192.168.178.42"
    port = 6000  # initiate port

    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  # get instance
    s.bind((host, port))  # bind host address and port
    s.listen()  # number of client can listen simultaneously

    client_thread = []
    client_address = []
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info("Server in ascolto")
    while True:
        conn, address = s.accept()  # accept new connection
        logging.info(f"New connection from: {address}")
        cl = ClientThread(conn, address, "percorsi.db")
        cl.start()
        client_thread.append(cl)
        client_address.append(address)

    print("chiudo i thread")
    for t in client_thread:
        t.join()


if __name__ == '__main__':
    server()
