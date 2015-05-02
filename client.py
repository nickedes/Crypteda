from encrypt import pad, to_hex, encrypt
from decrypt import rmpad, to_str, decrypt

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))

print s.recv(1024)
