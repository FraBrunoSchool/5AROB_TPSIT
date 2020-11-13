import threading
import sqlite3
import logging
import time


class ClientThread(threading.Thread):

    def __init__(self, connection, address, DB_nome):
        threading.Thread.__init__(self)
        self.Server_connection = connection
        self.Server_address = address
        self.DB_nome = DB_nome

    def run(self):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        f = open(f"log_{self.Server_address}.txt", "w")

        logging.info('Inizio ricezione/elaborazione dati')
        f.write(f'{time.strftime("%Y-%m-%d")} {time.strftime("%H:%M:%S")} - Inizio ricezione/elaborazione dati\n')

        while True:
            DB_connection = sqlite3.connect(self.DB_nome)
            DB_cursor = DB_connection.cursor()

            # carico lista località per controllo
            lista_localita = []
            for row in DB_cursor.execute('SELECT luoghi.nome FROM luoghi'): lista_localita.append(row[0])

            data = self.Server_connection.recv(1024).decode()  # receive data

            logging.info(f"from connected user {self.Server_address}:  {data}")
            f.write(f'{time.strftime("%Y-%m-%d")} {time.strftime("%H:%M:%S")} - '
                    f'from connected user {self.Server_address}:  {data}")\n')

            # controllo se finire connessione
            if not data or data == "exit":
                # if data is not received or data is the word 'exit' to end the connection break
                logging.info(f"Close connection user {self.Server_address}")
                f.write(
                    f'{time.strftime("%Y-%m-%d")} {time.strftime("%H:%M:%S")} - Close connection user {self.Server_address}")\n')
                self.Server_connection.close()  # close the connection
                break

            localita = data.split(",")

            if localita[0] in lista_localita and localita[1] in lista_localita:
                logging.info(f"from connected user {self.Server_address}:  valid data")
                f.write(f'{time.strftime("%Y-%m-%d")} {time.strftime("%H:%M:%S")} - '
                        f'from connected user {self.Server_address}:  valid data")\n')
            else:
                logging.error(
                    f"from connected user {self.Server_address}: 1.2,start or end not found re-enter end,start")
                f.write(f'{time.strftime("%Y-%m-%d")} {time.strftime("%H:%M:%S")} - '
                        f'from connected user {self.Server_address}:  1.2,start or end not found re-enter end,start")\n')
                self.Server_connection.send(f"1.2,start or end not found re-enter end,start".encode())
                # chiusura database
                DB_connection.close()
                continue
            try:
                logging.info(
                    f'SELECT percorsi.percorso FROM percorsi WHERE percorsi.id = (SELECT inizio_fine.id_percorso '
                    f'FROM inizio_fine WHERE inizio_fine.id_end = (SELECT luoghi.id FROM luoghi '
                    f'WHERE luoghi.nome = "{localita[0]}") AND inizio_fine.id_start = '
                    f'(SELECT luoghi.id FROM luoghi WHERE luoghi.nome = "{localita[1]}"));')
                f.write(
                    f'{time.strftime("%Y-%m-%d")} {time.strftime("%H:%M:%S")} - SELECT percorsi.percorso FROM percorsi'
                    f' WHERE percorsi.id = (SELECT inizio_fine.id_percorso FROM inizio_fine WHERE inizio_fine.id_end = '
                    f'(SELECT luoghi.id FROM luoghi WHERE luoghi.nome = "{localita[0]}") AND inizio_fine.id_start = '
                    f'(SELECT luoghi.id FROM luoghi WHERE luoghi.nome = "{localita[1]}"));\n')
                percorso = []
                for row in DB_cursor.execute(f'SELECT percorsi.percorso FROM percorsi WHERE percorsi.id = '
                                             f'(SELECT inizio_fine.id_percorso FROM inizio_fine WHERE inizio_fine.id_end = '
                                             f'(SELECT luoghi.id FROM luoghi WHERE luoghi.nome = "{localita[0]}") '
                                             f'AND inizio_fine.id_start = (SELECT luoghi.id FROM luoghi '
                                             f'WHERE luoghi.nome = "{localita[1]}"));'):
                    percorso = row

                percorso = str(percorso[0]).upper()
                logging.info(f"Risultato query: {percorso}")
                f.write(f'{time.strftime("%Y-%m-%d")} {time.strftime("%H:%M:%S")} - Risultato query: {percorso}\n')
            except:
                logging.error(
                    f"from connected user {self.Server_address}: 1.1,path not found re-enter end,start")
                f.write(f'{time.strftime("%Y-%m-%d")} {time.strftime("%H:%M:%S")} - '
                        f'from connected user {self.Server_address}:  1.1,path not found re-enter end,start")\n')
                self.Server_connection.send(f"1.1,path not found re-enter end,start".encode())
                # chiusura database
                DB_connection.close()
                continue

            # chiusura database
            DB_connection.close()

            logging.info(f"For the connected user {self.Server_address}:  0.0,{percorso}")
            f.write(
                f'{time.strftime("%Y-%m-%d")} {time.strftime("%H:%M:%S")} - For the connected user {self.Server_address}:  0.0,{percorso}')
            self.Server_connection.send(f"0.0,{percorso}".encode())  # send data to the client

        self.Server_connection.close()
        f.close()
