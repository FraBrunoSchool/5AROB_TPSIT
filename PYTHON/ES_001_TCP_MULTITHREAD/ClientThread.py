import threading


class ClientThread(threading.Thread):

    def __init__(self, connection, address):
        threading.Thread.__init__(self)
        self.connection = connection
        self.address = address

    def run(self):
        while True:
            data = self.connection.recv(1024).decode()  # receive data
            print(f"from connected user {self.address}:  {data}")

            if not data or data == "exit":
                # if data is not received or data is the word 'exit' to end the connection break
                print(f"Close connection user {self.address}")
                self.connection.close()  # close the connection
                break

            self.connection.send(data.encode())  # send data to the client

        self.connection.close()