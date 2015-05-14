from encrypt import pad, to_hex
from decrypt import rmpad, to_str, decrypt

import socket
import pickle


def decryption(cipher, key):
    dt = []
    key = to_hex(pad(key))[0]

    for block in cipher:
        dt.append(decrypt(block, key))
    final = ""
    for block in dt:
        final += to_str(block)
    return rmpad(final)

key = 'nikhil'

s = socket.socket()
host = socket.gethostname()
port = 12345

s.connect((host, port))

while True:
    cipher_text = pickle.loads(s.recv(1024))
    print(cipher_text)
    decrypted_msg = decryption(cipher_text, key)
    print(decrypted_msg)
