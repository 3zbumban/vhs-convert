# echo_server.py
import socket
import settings


def server():
  host = settings.IP_PC        # Symbolic name meaning all available interfaces
  port = 12345     # Arbitrary non-privileged port
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((host, port))
  s.listen(1)
  conn, addr = s.accept()
  # print('Connected by', addr)
  while True:
      data = conn.recv(1024)
      if not data: break
      if data.decode() == "q":
        return True
        print("quit", addr)
      print(data.decode())
      conn.sendall(data)
  conn.close()

if __name__ == "__main__":
  server()