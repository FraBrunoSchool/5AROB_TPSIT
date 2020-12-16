import socket as sck


def server():
    # get the hostname
    server_ip_mio = "192.168.88.85"  # 0.0.0.0
    server_port_mio = 7000  # initiate port
    # "192.168.88.78"
    server_ip_compagno = "192.168.88.83"
    server_port_compagno = 7000  # server port number

    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  # get instance
    c = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  # instantiate

    s.bind((server_ip_mio, server_port_mio))  # bind host address and port

    while True:

        s.listen()
        print("Server attivo")

        conn, address = s.accept()
        print(f"onnection from: {address}")

        data = conn.recv(1024).decode()  # receive message

        print(f"From connected user {address}:  {data}")
        print(f"Ora invio al mio compagno {(server_ip_compagno, server_port_compagno)}")

        c.connect((server_ip_compagno, server_port_compagno))  # connect to the server
        c.sendall(data.encode())  # send message

        print(f"Messaggio inviato al mio compagno {(server_ip_compagno, server_port_compagno)}")

        if not data or data == "exit":
            # if data is not received or data is the word 'exit' to end the connection break
            print("Close the connection")
            break

        conn.sendall(data.encode())  # send data to the client

    conn.close()
    c.close()



if __name__ == '__main__':
    server()
