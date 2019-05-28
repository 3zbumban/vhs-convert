# echo_client.py
import socket
import settings

def client():
  host = settings.IP_PC    
  port = 12345                   # The same port as used by the server
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((host, port))
  s.sendall(b'q')
  data = s.recv(1024)
  s.close()
  print('Received', repr(data))

if __name__ == "__main__":
  client()