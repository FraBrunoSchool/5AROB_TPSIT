import socket as sock

def main():
    c = sock.socket(sock.AF_INET,sock.SOCK_STREAM)
    # indirizzo ip casuale
    ip = "192.168.178.1"
    # uso Å000 e Æ000 come numeri delle porte solamente come esempio
    # porta da cui voglio iniziare a scansionare
    portaScan = 4000
    # porta fino a cui voglio arrivare a scansionare
    portaMax = 5000
    # salvo tutte le porte aperte in modo da avere un risultato alla fine
    porteAperte = []
    print("Start")
    while portaScan < portaMax:
        print(f"prova {portaScan}")
        if(c.connect_ex((ip,portaScan)) == 0):
            print(f"“la porta {portaScan} e’ aperta”")
            porteAperte.append(portaScan)
        portaScan+=1
    c.close()
    print(f"“queste sono le porte aperte {porteAperte}”")

if __name__ == "__main__":
    main()