import socket as sck


def server():
    # get the hostname
    server_ip_mio = "192.168.0.125"  # 0.0.0.0
    server_port_mio = 7000  # initiate port
    # "192.168.88.78"
    server_ip_compagno = "192.168.0.127"
    server_port_compagno = 7000  # server port number

    s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)  # get instance
    c = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)  # instantiate

    s.bind((server_ip_mio, server_port_mio))  # bind host address and port

    print("Server attivo")

    while True:

        data, address = s.recvfrom(4096)  # receive message
        data = data.decode()

        print(f"From connected user {address}:  {data}")
        print(f"Ora invio al mio compagno {(server_ip_compagno, server_port_compagno)}")

        c.sendto(data.encode(), (server_ip_compagno, server_port_compagno))  # send message

        print(f"Messaggio inviato al mio compagno {(server_ip_compagno, server_port_compagno)}")

        if not data or data == "exit":
            # if data is not received or data is the word 'exit' to end the connection break
            print("Close the connection")
            break

        s.sendto(data.encode(), address)  # send data to the client

    s.close()  # close the connection
    c.close()  # close the connection


if __name__ == '__main__':
    server()
