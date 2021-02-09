import socket as sck

lista_tentativi = {
    "Best": "asdf",
    "fraBruno": "qwerty"
}


def client():
    c = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  # instantiate
    c.connect(('127.0.0.1', 5000))
    print("connesso")

    for utente in lista_tentativi.items():
        print(utente)
        body = f"username={utente[0]}&password={utente[1]}"
        msg = f"POST http://127.0.0.1:5000/login HTTP/1.1\r\n" \
              f"Host: http://127.0.0.1:5000/login.html\r\n" \
              f"Content-Length: {len(body)}\r\n" \
              f"Content-Type: application/x-www-form-urlencoded\r\n" \
              f"\r\n" \
              f"{body}"

        c.sendall(msg.encode())
        data = (c.recv(8192)).decode()
        while data:
            print(data)
            data = (c.recv(8192)).decode()


if __name__ == '__main__':
    client()
