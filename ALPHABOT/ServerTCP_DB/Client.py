import socket as sck
import Classi.Config as conf


def client():
    print("creo istanza")
    c = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  # instantiate

    c.connect((conf.SERVER_IP, conf.SERVER_PORT))
    print("connect")

    print("Enter 'exit' to end the connection")
    msg = input("->")  # take input

    while True:
        try:
            c.sendall(msg.encode())  # send message
        except:
            print(f"failed")

        data = c.recv(conf.BUFFER_SIZE).decode()  # receive response
        print(f"Received from server: {data}")  # show response

        msg = input("->")  # again take input

        if msg == "exit":
            c.sendall(msg.encode())  # send message
            print("Close the connection")
            break

    c.close()  # close the connection


if __name__ == '__main__':
    client()