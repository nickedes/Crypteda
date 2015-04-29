from encrypt import pad, to_hex, encrypt
from decrypt import rmpad, to_str, decrypt

plain = open("plain.txt").read()
key = input("Enter Key: ")

print("\n-------------------- Encryption ----------------------\n")

inp = to_hex(pad(plain))
key = to_hex(pad(key))[0]

ct = []
for block in inp:
    ct.append(encrypt(block, key))

encrypted_text = ""
for block in ct:
    encrypted_text += to_str(block)

print("\n")
print("Encrypted Text: ", encrypted_text)
print("\n")

print("\n-------------------- Decryption ----------------------\n")

dt = []
for block in ct:
    dt.append(decrypt(block, key))
    print()

print("\n---------------------- Result ------------------------\n")

final = ""
for block in dt:
    final += to_str(block)

print("Decrypted Text: ", rmpad(final))
