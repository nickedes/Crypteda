from encrypt import pad, to_hex, encrypt
from decrypt import rmpad, to_str, decrypt

import socket,pickle             # Import socket module


def decryption(cipher, key):
    dt = []
    for block in cipher:
        dt.append(decrypt(block, key))
        print()
    return dt

key = 'Nikhil Mittal'

s = socket.socket()         # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))

while True:
    cipher_text = pickle.loads(s.recv(1024))
    print(cipher_text)
    decrypted_msg = decryption(cipher_text, key)
    print(decrypted_msg)
    # msg = input("enter message:")
    # s.send(msg)
