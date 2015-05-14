from encrypt import pad, to_hex, encrypt
import socket
import pickle


def encryption(plain, key):
    inp = to_hex(pad(plain))
    key = to_hex(pad(key))[0]

    ct = []
    for block in inp:
        ct.append(encrypt(block, key))
    return ct

key = 'nikhil'

s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind((host, port)) 

s.listen(5)
while True:
    c, addr = s.accept()
    print('Got connection from', addr)
    msg = input("enter message:")
    cipher_text = encryption(msg, key)
    c.send(pickle.dumps(cipher_text))
