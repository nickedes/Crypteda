from encrypt import pad, to_hex, encrypt
from decrypt import to_str
import socket ,pickle             # Import socket module


def encryption(plain, key):
    inp = to_hex(pad(plain))
    key = to_hex(pad(key))[0]

    ct = []
    for block in inp:
        ct.append(encrypt(block, key))
    return ct

key = 'Nikhil Mittal'

s = socket.socket()         # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
    c, addr = s.accept()     # Establish connection with client.
    print('Got connection from', addr)
    msg = input("enter message:")
    cipher_text = encryption(msg, key)
    c.send(pickle.dumps(cipher_text))
    # print(c.recv(1024))
