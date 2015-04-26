from encrypt import pad, to_hex, encrypt
from decrypt import rmpad, to_str, decrypt

plain = "Waking Up With Stories of You to Tell Nobody"
key = "Key length > 16?"

print("Plain Text: ", plain)
print("Key: ", key)

print("\n-------------------- Encryption ----------------------\n")

inp = to_hex(pad(plain))
key = to_hex(pad(key))[0]

ct = []
for block in inp:
    ct.append(encrypt(block, key))
    print()

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
