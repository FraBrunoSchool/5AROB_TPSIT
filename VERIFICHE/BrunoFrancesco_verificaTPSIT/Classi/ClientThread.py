import threading
import sqlite3
import Classi.Config as conf
from Classi.Log import Log


class ClientThread(threading.Thread):

    def __init__(self, connection, address, DB_nome, countClient):
        threading.Thread.__init__(self)
        self.Server_connection = connection
        self.Server_address = address
        self.DB_nome = DB_nome
        self.num_client = countClient
        ip = ""
        for i in self.Server_address[0].split("."): ip += str(i)
        ip += "_" + str(self.Server_address[1])
        self.log = Log(f"{conf.PATH_LOG}log_Server_{ip}.txt")

    def run(self):

        # connessione al database e carico le operazioni per solo questo client
        db_connection = sqlite3.connect(self.DB_nome)
        db_cursor = db_connection.cursor()
        self.log.i(f"SELECT operation FROM operations WHERE client = {self.num_client}")
        lista_operazioni = []
        for row in db_cursor.execute(f"SELECT operation FROM operations WHERE client = {self.num_client}"):
            lista_operazioni.append(row[0])

        self.log.i('thread started, start data transmission with server')
        operazioneCorrente = None
        while True:
            # ricezione dati dal client
            data = self.Server_connection.recv(conf.BUFFER_SIZE).decode()  # receive data
            # al primo giro ricevo start
            if data != "exit" and data != "start" and data != "error":
                self.log.i(f"{operazioneCorrente} = {data} from {self.Server_address[0]} - {self.Server_address[1]}")
            else:
                if data == "error":
                    # error
                    self.log.e(f"{operazioneCorrente} = ERROR from {self.Server_address[0]} - {self.Server_address[1]}")
                else:
                    # uscita
                    self.log.i(f"from connected user {self.Server_address}:  {data}")

            # controllo se finire connessione
            if not data or data == "exit":
                # if data is not received or data is the word 'exit' to end the connection break
                self.log.i(f"Close connection user {self.Server_address}")
                self.Server_connection.close()  # close the connection
                break

            # provo a prendere la prossima operazione
            try:
                operazioneCorrente = lista_operazioni.pop(0)
            except:
                # se non ci sono più operazioni mando exit
                operazioneCorrente = "exit"
                self.log.i(f"there are no more operations")

            self.log.i(f"For the connected user {self.Server_address}:  {operazioneCorrente}")
            #
            self.Server_connection.send(f"{operazioneCorrente}".encode())  # send data to the client

        self.Server_connection.close()
