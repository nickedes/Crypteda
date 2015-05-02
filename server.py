from encrypt import pad, to_hex, encrypt
from decrypt import rmpad, to_str, decrypt

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
    c, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    msg = raw_input("enter plaintext:")
    c.send(msg)
