from encrypt import pad, to_hex, encrypt
from decrypt import rmpad, to_str, decrypt

import socket               # Import socket module


def decryption(cipher, key):
    dt = []
    for block in cipher:
        dt.append(decrypt(block, key))
        print()
    final = ""
    for block in dt:
        final += to_str(block)
    return rmpad(final)

key = 'Nikhil Mittal'

s = socket.socket()         # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))

while True:
    cipher_text = s.recv(1024)
    decrypted_msg = decryption(cipher_text, key)
    print(decrypted_msg)
    msg = input("enter message:")
    s.send(msg)
