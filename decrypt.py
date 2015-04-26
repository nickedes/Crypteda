from tables import *
from encrypt import gen


def inv_substi(s, inv_sbox):
    substi = []
    i = 0
    for k in range(len(s)):
        substi.append([])

    for k in range(len(s)):
        for i in range(len(s[k])):
            if len(s[k][i]) == 1:
                s[k][i] = '0' + s[k][i]
            substi[k].append(
                inv_sbox[int(s[k][i][0], 16)][int(s[k][i][1], 16)])
    return substi


def multiply(y, x):

    if y == 9:
        return mul_9[x]
    elif y == 11:
        return mul_11[x]
    elif y == 13:
        return mul_13[x]
    elif y == 14:
        return mul_14[x]


def inv_mixcolumns(s):

    fixed_matrix = [['0e', '0b', '0d', '09'], ['09', '0e', '0b', '0d'], [
        '0d', '09', '0e', '0b'], ['0b', '0d', '09', '0e']]

    for k in range(len(s)):
        for j in range(len(s[k])):
            s[k][j] = int(s[k][j], 16)

    for k in range(len(fixed_matrix)):
        for j in range(len(fixed_matrix[k])):
            fixed_matrix[k][j] = int(fixed_matrix[k][j], 16)

    c = [[0 for row in range(len(s))] for col in range(len(fixed_matrix))]

    for i in range(len(s)):
        for j in range(len(fixed_matrix)):
            for k in range(len(s)):
                c[i][j] ^= int(multiply(fixed_matrix[i][k], s[k][j]), 16)

    for k in range(len(c)):
        for j in range(len(c[k])):
            c[k][j] = hex(c[k][j])[2:]
    return c


def inv_shiftrows(s):
    shifted_s = []

    for i in range(len(s)):
        shifted_s.append(s[i][len(s) - i:] + s[i][:len(s) - i])

    return shifted_s


def rotword(word):
    # ['fa','bb','13','cd'] -> ['bb','13','cd','fa']
    return word[1:] + word[:1]


def sub(word):
    # ['fa','bb','13','cd'] -> sbox values
    for i in range(len(word)):
        if len(word[i]) == 1:
            word[i] = '0' + word[i]
        word[i] = sbox[int(word[i][0], 16)][int(word[i][1], 16)]
    return word


def rcon(i):
    rcon_i = [0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
    return rcon_i[i]


def word_to_key(words):
    key = []
    for i in range(len(words)):
        key.append([])
    for i in range(len(words)):
        for j in range(len(words[i])):
            key[i].append(words[j][i])
    return key


def add_round_key(state, key):
    for i in range(len(key)):
        for j in range(len(key[i])):

            key[i][j] = hex(
                int(key[i][j], 16) ^ int(state[i][j], 16))[2:]
    return key


def decrypt(c, key):
    print("Input Matrix:", c)
    print()
    all_key = gen(key)
    key_no = 40

    last_key = word_to_key([all_key[key_no], all_key[key_no + 1],
                            all_key[key_no + 2], all_key[key_no + 3]])
    c = inv_substi(inv_shiftrows(add_round_key(c, last_key)), inv_sbox)
    print("Round 1:", c)

    round = 2
    while key_no > 4:
        key_no -= 4
        key = word_to_key([all_key[key_no], all_key[key_no + 1],
                           all_key[key_no + 2], all_key[key_no + 3]])
        c = inv_substi(inv_shiftrows(inv_mixcolumns(add_round_key(c, key))), inv_sbox)
        print("Round %d:" % round, c)
        round += 1

    key_no -= 4
    key = word_to_key([all_key[key_no], all_key[key_no + 1],
                       all_key[key_no + 2], all_key[key_no + 3]])
    decrypted_text = add_round_key(c, key)

    print()
    print("Round 11 (decrypted):", decrypted_text)
    return decrypted_text


def to_str(l):
    s = ""
    for i in l:
        for j in i:
            s += chr(int(j, 16))
    return s


def rmpad(s):
    """ Remove padding """
    end = ord(s[-1])
    return s[0:-1 * end]
