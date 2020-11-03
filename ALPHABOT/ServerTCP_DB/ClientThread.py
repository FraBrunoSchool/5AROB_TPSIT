import threading
import sqlite3


class ClientThread(threading.Thread):

    def __init__(self, connection, address, DB_nome):
        threading.Thread.__init__(self)
        self.Server_connection = connection
        self.Server_address = address
        self.DB_nome = DB_nome


    def run(self):
        while True:
            data = self.Server_connection.recv(1024).decode()  # receive data
            print(f"from connected user {self.Server_address}:  {data}")

            # controllo se finire connessione
            if not data or data == "exit":
                # if data is not received or data is the word 'exit' to end the connection break
                print(f"Close connection user {self.Server_address}")
                self.Server_connection.close()  # close the connection
                break
            localita = data.split(",")

            DB_connection = sqlite3.connect(self.DB_nome)
            DB_cursor = DB_connection.cursor()

            print(f'Query: SELECT id FROM luoghi WHERE nome="{localita[0]}"')
            for row in DB_cursor.execute(f'SELECT id FROM luoghi WHERE nome="{localita[0]}"'):
                id_localita_end = row
            print(f"Risultato query: {id_localita_end[0]}")

            print(f'Query: SELECT id FROM luoghi WHERE nome="{localita[1]}"')
            for row in DB_cursor.execute(f'SELECT id FROM luoghi WHERE nome="{localita[1]}"'):
                id_localita_start = row
            print(f"Risultato query: {id_localita_start[0]}")

            print(
                f'Query: SELECT id_percorso FROM inzio_fine WHERE id_end="{id_localita_end[0]}" AND id_start="{id_localita_start[0]}"')
            for row in DB_cursor.execute(f'SELECT id_percorso FROM inzio_fine WHERE id_end = "{id_localita_end[0]}" AND id_start = "{id_localita_start[0]}"'):
                id_percorso = row
            print(f"Risultato query: {id_percorso[0]}")

            print(f"Query: SELECT percorso FROM percorsi WHERE id = {id_percorso[0]}")
            for row in DB_cursor.execute(f'SELECT percorso FROM percorsi WHERE id = "{id_percorso[0]}"'):
                percorso = row
            print(f"Risultato query: {percorso[0]}")
            # elaborazione richiesta client

            DB_connection.close()

            self.Server_connection.send(percorso[0].encode())  # send data to the client

        self.Server_connection.close()
