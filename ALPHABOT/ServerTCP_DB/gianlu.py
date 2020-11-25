import socket as sck
import Classi.Config as conf

def client():
    print("creo istanza")
    c = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  # instantiate

    c.connect((conf.SERVER_IP, conf.SERVER_PORT))
    print("connect")


if __name__ == '__main__':
    client()