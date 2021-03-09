import socket as sck

c = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  # instantiate
c.connect(('192.168.0.30', 5000))
msg = f"GET http://127.0.0.1:5000/api/v1/resources/books/author?author=Liu%20Cixin HTTP/1.1\r\n" \
      f"Host: http://127.0.0.1:5000/api/v1/resources/books/author?author=Liu%20Cixin\r\n" \
      f"Content-Length: 0\r\n" \
      f"Content-Type: application/x-www-form-urlencoded\r\n" \
      f"\r\n" \
      f" "

c.sendall(msg.encode())
data = " "
while data != "":
    print(data)
    data = (c.recv(8192)).decode()
c.close()